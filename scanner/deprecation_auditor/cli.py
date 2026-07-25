import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from packaging.requirements import Requirement

from .dependency_checker.manifest_parser import parse_manifest
from .dependency_checker.pypi_checker import fetch, get_yanked
from .models import AuditResult, Detection, to_dict


def check_deps(deps: dict[str, Requirement]) -> list[Detection]:
    pypi_data = fetch(list(deps.keys()))

    detections = []
    for name, requirement in deps.items():
        result = get_yanked(requirement, pypi_data[name])
        if result is None:
            continue
        source, reason, version = result

        detections.append(Detection(
                        package=name,
                        version=version,
                        depr_status=source,
                        src=reason,
                        usages=[],))
    return detections


def git_commit_sha(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main():
    if len(sys.argv) != 3:
        print(
            "usage: python -m deprecation_auditor.cli <path to requirements.txt> <repo owner/name>",
            file=sys.stderr,
        )
        return 1

    manifest_path = Path(sys.argv[1])
    repo_info = sys.argv[2]

    deps = parse_manifest(manifest_path.read_text())
    detections = check_deps(deps)

    audit_result = AuditResult(
                audit_id=str(uuid.uuid4()),
                repo=repo_info,
                commit_sha=git_commit_sha(manifest_path.resolve().parent),
                audit_time=datetime.now(timezone.utc).isoformat(),
                detections=detections,)

    print(json.dumps(to_dict(audit_result)))
    return 0


if __name__ == "__main__":
    res = main()
    sys.exit(res)