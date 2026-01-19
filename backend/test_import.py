from app.core.rbac import RBAC

rbac = RBAC("config/rbac.yaml")
print(rbac.allowed_departments("c_level"))
