"""Notes for Backend Stack: Bringing Pydantic, SqlAlchemy, and Services together."""

# Be sure to run: `python3 -m pip install -r requirements.txt`

from typing import Self, Type


# ========================
# Pydantic Data Models

from pydantic import BaseModel, field_validator

class User(BaseModel):
    pid: int
    first_name: str
    last_name: str

    @field_validator('pid')
    def pid_must_be_9_digits(cls, value: int):
        if(len(str(value)) != 9):
            # his way:
        # if value < 100000000 or value > 999999999:
            raise ValueError("Please enter a 9 digit PID")
        # TODO: Raise ValueError if pid is not 9 digits
        return value


# ========================
# SqlAlchemy / Entity Layer

from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
session_factory = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    ...


class UserEntity(Base):
    __tablename__ = "users"

    pid: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    # TODO: Define from_model and to_model methods
    @classmethod
    def from_model(cls: Type[Self], user: User) -> Self:
        return UserEntity(pid=user.pid, first_name=user.first_name, last_name=user.last_name)
    
    # TODO: Define an *instance method* to convert a UserEntity into a Pydantic User Model
    # named to_model
    @classmethod
    def to_model(self) -> User:
        return User(pid=self.pid, first_name=self.first_name, last_name=self.last_name)
    
Base.metadata.create_all(engine)


Base.metadata.create_all(engine)


# ================================
# Service / "Business Logic" Layer

class UserService:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def register(self, user: User) -> User:
        # TODO: Persist the `user` object: create entity, add to session
        user_entity: UserEntity = UserEntity.from_model(user) # create entity
        self._session.add(user_entity) # add to session
        self._session.commit() 
        return user_entity.to_model()

    def get(self, pid: int) -> User:
        user = self._session.get(UserEntity, pid)
        if user:
            return user.to_model()
        else:
            raise ValueError(f"No user found with PID: {pid}")


# =========================
# Demo
# 1. Construct a User
    # a_user = User(pid=730330121, first_name="Ella", last_name="Parker")
# 2. Construct a UserService(session_factory()) named user_service
user_service = UserService(session_factory())
# 3. Register your User object using the service
# user_service.register(a_user)
# 4. Use the get method of your service to fetch the user from database
print(user_service.get(730330121))