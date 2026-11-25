from app.models.user_role import UserRole


class UserRoleRepository:
    def __init__(self, session):
        self.session = session

    async def insert_user_id_role_id(self, user_id, role_id):
        user_role = UserRole(user_id=user_id, role_id=role_id)

        self.session.add(user_role)

        await self.session.flush()
        await self.session.refresh(user_role)

        return user_role
