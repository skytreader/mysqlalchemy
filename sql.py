from sqlalchemy import Column, create_engine, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import os

"""
https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

host = os.environ.get("MYSQLALCHEMY_HOST", "localhost")

engine = create_engine("mysql://root:@%s:3306/mysqlalchemy" % host, echo=True)
session = sessionmaker(bind=engine)()
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class PersonRole(Base):
    __tablename__ = "person_roles"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id", name="person_roles_person", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", name="person_roles_role", ondelete="CASCADE"))
    project_id = Column(Integer, ForeignKey("projects.id", name="person_roles_project", ondelete="CASCADE"))

    person = relationship("Person")
    role = relationship("Role")
    project = relationship("Project")

role1 = Role(name="leader")
role2 = Role(name="assistant leader")
session.add_all((role1, role2))
