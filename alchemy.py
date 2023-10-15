# from dbus import SessionBus
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(repr(user_table.c.id))
# Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False)
print(repr(user_table.c.name))
# Column('name', String(length=30), table=<user_account>)
print(repr(user_table.c.keys()))
# ['id', 'name', 'fullname']

metadata_obj.create_all(engine)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

print(repr(Base.metadata))


# from typing import List
# from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]
    
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    user: Mapped[User] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
sandy = User(name="sandy", fullname="Sandy Cheeks")

print('Creating tables from Base metadata')
Base.metadata.create_all(engine)

from sqlalchemy.orm import Session

squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
spongebob = User(name="spongebob", fullname="Spongebob Squarepants")
sandy = User(name="sandy", fullname="Sandy Cheeks")
patrick = User(name="patrick", fullname="Patrick Star")
print(repr(squidward))
print(repr(squidward.id))

session = Session(engine)
session.add(squidward)
session.add(krabs)
session.add(spongebob)
session.add(sandy)
session.add(patrick)
session.new
session.flush()

print(repr(krabs.id))

some_squidward = session.get(User, 1)
print(some_squidward)
print(some_squidward is squidward)
print(repr(sandy.id))
session.commit()
print(some_squidward)

from sqlalchemy import select
sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
# print(repr(sandy))

stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)
        print(type(row))