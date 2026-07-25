import json
from pathlib import Path

import grequests
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version, InvalidVersion

DEPR_PACKAGES_PATH = Path(__file__).parent / "deprecated_pypi_packages.json"


def load_curated_deprecated() -> dict[str, dict]:
    with open(DEPR_PACKAGES_PATH) as f:
        raw = json.load(f)
    return {canonicalize_name(name): info for name, info in raw.items()}


DEPR_LIST = load_curated_deprecated()


def fetch(dependencies: list[str]) -> dict:
    urls = [f"https://pypi.org/pypi/{dep}/json" for dep in dependencies]
    res = grequests.map(grequests.get(url) for url in urls)
    return {dep: r.json() for dep, r in zip(dependencies, res)}


def get_yanked(requirement: Requirement, pypi_data: dict) -> tuple[str, str] | None:
    """ Returns (source, reason) where source is "depr_package" or "yanked".
        Returns None if the requirement isn't flagged by either check."""

    depr_package = DEPR_LIST.get(canonicalize_name(requirement.name))
    if depr_package is not None:
        return "depr_package", depr_package["reason"]

    resolved_version = resolve_version(requirement, pypi_data)
    if resolved_version is None:
        return None

    release_files = pypi_data.get("releases", {}).get(resolved_version) or []
    yanked_file = next((f for f in release_files if f.get("yanked")), None)
    if yanked_file is None:
        return None

    yanked_reason = yanked_file.get("yanked_reason") or "No reason given"
    return "yanked", yanked_reason


def resolve_version(requirement: Requirement, pypi_data: dict) -> str | None:
    if not pypi_data or "releases" not in pypi_data:
        return None

    by_version: dict[Version, str] = {}
    for v_str in pypi_data["releases"].keys():
        try:
            v = Version(v_str)
        except InvalidVersion:
            continue
        if not (v.is_prerelease or v.is_devrelease):
            by_version[v] = v_str

    stable_v = list(requirement.specifier.filter(by_version.keys(), prereleases=False))

    if not stable_v:
        return None

    return by_version[max(stable_v)]

