from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """Users table"""

    __tablename__ = "users"
    username = Column(String, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True, default=0)
    is_admin = Column(Boolean, nullable=False, default=False)

    project = relationship("Project", secondary="roles",
                           back_populates="annotators")


class Sentence(Base):
    """Sentences table"""

    __tablename__ = "sentences"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    language_iso = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))


class Translation(Base):
    """Translations table"""

    __tablename__ = "translations"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    language_iso = Column(String)
    src_sentence_id = Column(Integer, ForeignKey("sentences.id"))
    annotator_username = Column(String, ForeignKey("users.username"))


class Recording(Base):
    """Recordings table"""

    __tablename__ = "recordings"
    id = Column(Integer, primary_key=True)
    audio_file_path = Column(String)
    language_iso = Column(String)
    src_sentence_id = Column(Integer, ForeignKey("sentences.id"))
    annotator_username = Column(String, ForeignKey("users.username"))


class Project(Base):
    """Projects table"""

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    p_type = Column(String)

    annotators = relationship(
        "User", secondary="roles", back_populates="project")


class Role(Base):
    """Roles table"""

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey("users.username"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(String, nullable=False)
