from typing import List
from sqlalchemy import Column, Enum, Integer, String, Boolean
from sqlalchemy.orm import relationship
from asisya_api.core.database import Base
from asisya_api.domain.role import Role


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    roles = Column(String)  # Roles stored as comma-separated string

    products = relationship("ProductEntity", back_populates="created_by_user", lazy="select")

    def get_roles(self) -> List[Role]:
        return [Role(role) for role in self.roles.split(",")]

    def set_roles(self, roles: List[Role]) -> None:
        self.roles = ",".join([role.value for role in roles])
