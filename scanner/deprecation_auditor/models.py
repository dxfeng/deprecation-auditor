from dataclasses import dataclass

@dataclass
class Usage:
    file:str
    line:int
    code:str

@dataclass
class Detection:
    package:str
    version:str
    depr_status:str
    src:str
    usages:list[Usage]


@dataclass
class AuditResult:
    audit_id:str
    repo:str
    commit_sha:str
    audit_time:str
    detections:list[Detection]

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif hasattr(obj, '__dataclass_fields__'):
        return {field: to_dict(getattr(obj, field)) for field in obj.__dataclass_fields__}
    else:
        return obj
