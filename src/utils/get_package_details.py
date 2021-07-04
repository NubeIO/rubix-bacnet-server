import os
import toml


class PackageDetails:

    @staticmethod
    def load(cwd=None) -> dict:
        if not cwd:
            cwd = os.getcwd()
        file = "pyproject.toml"
        path = f"{cwd}/{file}"
        cfg = toml.load(path)
        main = cfg.get("tool", {}).get("poetry")
        name = main.get("name")
        version = main.get("version")
        description = main.get("description")

        return {
            "name": name,
            "version": version,
            "description": description,
        }
