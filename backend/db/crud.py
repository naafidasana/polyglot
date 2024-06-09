from sqlalchemy.orm import Session
from . import models, schemas
from ..utils import hash_password


# User CRUD Operations

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username, email=user.email,
        gender=user.gender, age=user.age,
        hashed_password=hashed_password, is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, username: str, user: schemas.UserUpdate):
    db_user = get_user(db=db, username=username)
    if db_user:
        for attr, value in user.model_dump().items():
            if value is not None:
                setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
    else:
        raise ValueError(f"User `{username}` does not exist.")

    return db_user


def delete_user(db: Session, username: str):
    db_user = get_user(db=db, username=username)
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise ValueError(f"User `{username}` does not exist.")

    return db_user


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Project CRUD Operations

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db=db, project_id=project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    else:
        raise ValueError(f"No such project with id `{project_id}`.")

    return db_project


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.name == project_name).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


# Sentence CRUD Operations

def create_sentence(db: Session, sentence: schemas.SentenceCreate, project_id: int):
    db_sentence = models.Sentence(
        **sentence.model_dump(), project_id=project_id)
    db.add(db_sentence)
    db.commit()
    db.refresh(db_sentence)

    return db_sentence


def delete_sentence(db: Session, sentence_id: int):
    db_sentence = get_sentence(db=db, sentence_id=sentence_id)
    if db_sentence:
        db.delete(db_sentence)
        db.commit()
    else:
        raise ValueError(f"No such sentence with id `{sentence_id}`.")

    return db_sentence


def get_sentence(db: Session, sentence_id: int):
    return db.query(models.Sentence).filter(models.Sentence.id == sentence_id).first()


def get_project_sentence(db: Session, project_id: int, src_sentence_id: int):
    return db.query(models.Sentence).filter(models.Sentence.project_id == project_id).filter(models.Sentence.id == src_sentence_id).first()


def get_sentences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sentence).offset(skip).limit(limit).all()


def get_project_sentences(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Sentence).filter(models.Sentence.project_id == project_id).offset(skip).limit(limit).all()


# Translation CRUD Operations

def create_translation(db: Session, src_sentence_id: int, translation: schemas.TranslationCreate):
    db_translation = models.Translation(
        **translation.model_dump(), src_sentence_id=src_sentence_id)
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)

    return db_translation


def delete_translation(db: Session, translation_id: int):
    db_translation = get_translation(db=db, translation_id=translation_id)
    if db_translation:
        db.delete(db_translation)
        db.commit()
    else:
        raise ValueError(f"No such translation with id `{translation_id}`.")

    return db_translation


def get_translation(db: Session, src_sentence_id: int, translation_id: int):
    return db.query(models.Translation).filter(models.Translation.src_sentence_id == src_sentence_id).filter(models.Translation.id == translation_id).first()


def get_translations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Translation).offset(skip).limit(limit).all()


# Recording CRUD Operations

def create_recording(db: Session, recording: schemas.RecordingCreate):
    db_recording = models.Recording(**recording.model_dump())
    db.add(db_recording)
    db.commit()
    db.refresh(db_recording)

    return db_recording


def delete_recording(db: Session, recording_id: int):
    db_recording = get_recording(db=db, recording_id=recording_id)
    if db_recording:
        db.delete(db_recording)
        db.commit()
    else:
        raise ValueError(f"No such recording with id `{recording_id}`.")

    return db_recording


def get_recording(db: Session, recording_id: int):
    return db.query(models.Recording).filter(models.Recording.id == recording_id).first()


def get_recordings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recording).offset(skip).limit(limit).all()


# Role CRUD Operations

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role(db=db, role_id=role_id)
    if db_role:
        db.delete(db_role)
        db.commit()
    else:
        raise ValueError(f"No such role with id `{role_id}`.")

    return db_role


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()
