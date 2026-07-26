import json
from pathlib import Path

from packaging.utils import canonicalize_name

MODULE_NAME_OVERRIDES_PATH = Path(__file__).parent / "module_name_overrides.json"


def load_module_name_overrides() -> dict[str, str]:
    with open(MODULE_NAME_OVERRIDES_PATH) as f:
        raw = json.load(f)
    return {name: module for name, module in raw.items()}


MODULE_NAME_OVERRIDES = load_module_name_overrides()

def get_module_name(package_name: str) -> str:
    """
        Not always correct, and overrides only contains a dataset 
        of popular packages suggested to me by claude & gemini.
    """
    override = MODULE_NAME_OVERRIDES.get(canonicalize_name(package_name))
    if override is not None:
        return override
    return package_name.lower().replace("-", "_")