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
    name = Column(String(255))

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class PersonRole(Base):
    __tablename__ = "person_roles"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id", name="person_roles_person", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", name="person_roles_role", ondelete="CASCADE"))
    project_id = Column(Integer, ForeignKey("projects.id", name="person_roles_project", ondelete="CASCADE"))

    person = relationship("Person")
    role = relationship("Role")
    project = relationship("Project")

Base.metadata.create_all(engine)

role1 = Role(name="leader")
role2 = Role(name="assistant leader")
role3 = Role(name="vice leader")
project = Project(name="project")
leader_person = Person(name="leader person")
al_person = Person(name="assistant leader")
vl_person1 = Person(name="vice leader1")
vl_person2 = Person(name="vice leader2")
session.add_all((role1, role2, role3, project, leader_person, al_person, vl_person1, vl_person2))
session.flush()

leader_pr = PersonRole(person=leader_person, role=role1, project=project)
al_pr = PersonRole(person=al_person, role=role2, project=project)
vl_pr1 = PersonRole(person=vl_person1, role=role3, project=project)
vl_pr2 = PersonRole(person=vl_person2, role=role3, project=project)
session.add_all((leader_pr, al_pr, vl_pr1, vl_pr2))
session.flush()
session.commit()
