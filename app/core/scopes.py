from app.models.roles import RoleEnum

SCOPES = {
    RoleEnum.ADMIN: [
        # user management
        "user:create:employee",
        "user:create:manager",
        "user:create:customer",
        "user:update:any",
        "user:delete:any",
        # profile
        "profile:read:self",
        "profile:update:self",
        "profile:read:any",
        "profile:update:any",
        "category:create",
        "category:update",
        "product:create",
        "product:update",
    ],
    RoleEnum.MANAGER: [
        "user:create:employee",
        "user:create:customer",
        # profile: self only
        "profile:read:self",
        "profile:update:self",
        "category:create",
        "category:update",
        "product:create",
        "product:update",
    ],
    RoleEnum.EMPLOYEE: [
        "profile:read:self",
        "profile:update:self",
    ],
    RoleEnum.CUSTOMER: [
        "profile:read:self",
        "profile:update:self",
    ],
}
