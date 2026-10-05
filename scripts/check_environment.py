"""Check the isolated environment without training or contacting an API."""

import importlib
import json
import platform
import sys
from importlib.metadata import version


def main() -> None:
    packages = {
        "scikit-learn": "sklearn",
        "pandas": "pandas",
        "streamlit": "streamlit",
        "joblib": "joblib",
        "pytest": "pytest",
    }
    for module in packages.values():
        importlib.import_module(module)
    print(json.dumps({
        "python": platform.python_version(),
        "system": platform.system(),
        "architecture": platform.machine(),
        "isolated_environment": sys.prefix != sys.base_prefix,
        "packages": {package: version(package) for package in packages},
    }, indent=2))
    if sys.prefix == sys.base_prefix:
        raise SystemExit("Run this check with the project's .venv Python.")


if __name__ == "__main__":
    main()
