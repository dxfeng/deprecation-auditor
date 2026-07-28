import json
import os
import requests

from ..models import AuditResult, Detection, Usage

def build_comment(audit:AuditResult) -> str:
    comment_builder = []
    comment_builder.append(f"Audit performed on commit `{audit.commit_sha}` @ {audit.audit_time}\n\n")
    for detection in audit.detections:
        comment_builder.append(f"### {detection.package} ({detection.version}) - {detection.depr_status}\n")
        for usage in detection.usages:
            comment_builder.append(f"- {usage.file}:{usage.line} - `{usage.code}`\n")
    return "".join(comment_builder)


def read_pr_number() -> int | None:
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    # for local testing
    if not event_path:
        return None
        
    with open(event_path) as f:
        event = json.load(f)

    return event.get("pull_request", {}).get("number")

def post_comment(audit: AuditResult, repo_info: str, token: str):
    pr_number = read_pr_number()
    if pr_number is None:
        return

    body = build_comment(audit)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    res = requests.post(
        f"https://api.github.com/repos/{repo_info}/issues/{pr_number}/comments",
        headers=headers, json={"body": body}, timeout=10)

    # for debugging (but probably shouldnt ever happen?)

    res.raise_for_status()
