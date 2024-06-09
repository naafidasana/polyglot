from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..db import database, schemas, crud
from .. import oauth2


router = APIRouter(
    tags=["Translations"],
    prefix="/projects/{project_id}/sentences/{sentence_id}/translations"
)


# Create translation
@router.post("/", response_model=schemas.Translation)
def create_translation(project_id: int, sentence_id: int, translation: schemas.TranslationCreate, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    db_project = crud.get_project(db=db, project_id=project_id)

    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such project with id `{project_id}`."
        )

    if not (user.is_admin or user.username in [annotator.username for annotator in db_project.annotators]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User `{user.username} is is not authorized to access project with id `{project_id}`."
        )

    db_sentence = crud.get_project_sentence(
        db=db, project_id=project_id, sentence_id=sentence_id)

    if db_sentence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such sentence with id `{sentence_id}` found in project with id `{project_id}`."
        )

    return crud.create_translation(db=db, sentence_id=sentence_id, translation=translation)


@router.get("/{translation_id}", response_model=schemas.Translation)
def get_translation(project_id: int, src_sentence_id: int, translation_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    db_project_sentence = crud.get_project_sentence(
        db=db, project_id=project_id, src_sentence_id=src_sentence_id)

    if db_project_sentence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such sentence with id `{src_sentence_id}` found in project with id `{project_id}`."
        )

    return crud.get_translation(db=db, src_sentence_id=src_sentence_id, translation_id=translation_id)
