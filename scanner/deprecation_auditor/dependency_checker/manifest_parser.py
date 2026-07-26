import sys
from packaging.requirements import Requirement, InvalidRequirement


def parse_manifest(manifest_content: str) -> dict[str, Requirement]:
    """
    Limitation:
    skips line if it starts with "-". A line with a "-" may be an editable install or trigger another requirements file.
    """
    requirements = {}

    for raw_line in manifest_content.splitlines():
        line = raw_line
        if "#" in raw_line:
            line = raw_line[: raw_line.index("#")]
        line = line.strip()

        if line and not line.startswith("-"):
            try:
                requirement = Requirement(line)
                requirements[requirement.name] = requirement
            except InvalidRequirement:
                pass
            

    return requirements