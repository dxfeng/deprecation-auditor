import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .manifest_parser import parse_manifest
from .pypi_checker import check_deps
from ..ast_scanner.repo_ast_traversal import find_audited_dep, get_files_as_ast
from ..models import AuditResult, to_dict
from ..integration.pr_reader import post_comment

def git_commit_sha(repo_root: Path) -> str:
    github_sha = os.environ.get("GITHUB_SHA")
    if github_sha:
        return github_sha
    
    # for local testing before I put it into a docker action
    try:
        result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

def perform_audit(args:list):
    """
        args -> ["manifest_path", "repo_root", "repo_info", "github_token"]
    """


    manifest_path = Path(args[0])
    repo_root = args[1]
    repo_info = args[2]
    github_token = args[3]


    deps = parse_manifest(manifest_path.read_text())
    detections = check_deps(deps)

    dep_loc = find_audited_dep(get_files_as_ast(repo_root), detections)

    for detection in detections:
        detection.usages = dep_loc.get(detection.package, [])

    audit_result = AuditResult(
                audit_id=str(uuid.uuid4()),
                repo=repo_info,
                commit_sha=git_commit_sha(manifest_path.resolve().parent),
                audit_time=datetime.now(timezone.utc).isoformat(),
                detections=detections)

    #print(json.dumps(to_dict(audit_result)))
    post_comment(audit_result, repo_info, github_token)