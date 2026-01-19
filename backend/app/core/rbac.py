import yaml
from pathlib import Path

class RBAC:
    def __init__(self, path="config/rbac.yaml"):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"RBAC file not found: {path}")

        with open(path, "r") as f:
            self.config = yaml.safe_load(f)

    def allowed_departments(self, role: str) -> list[str]:
        roles = self.config.get("roles", {})

        if role not in roles:
            raise ValueError(f"Unknown role: {role}")

        return roles[role]["allowed_departments"]
