import grequests
from packaging.requirements import Requirement
from packaging.version import Version, InvalidVersion

def fetch(dependencies: list[str]) -> dict:
    urls = [f"https://pypi.org/pypi/{dep}/json" for dep in dependencies]
    res = grequests.map(grequests.get(url) for url in urls)
    return {dep: r.json() for dep, r in zip(dependencies, res)}


def get_yanked(requirement: Requirement, pypi_data: dict) -> str | None:
    resolved_version = resolve_version(requirement, pypi_data)
    if resolved_version is None:
        return None

    release_files = pypi_data.get("releases", {}).get(resolved_version)

    if not (release_files and any(f.get("yanked") for f in release_files)):
        return None
    
    return resolved_version


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

