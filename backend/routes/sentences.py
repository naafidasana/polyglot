from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..db import database, schemas, crud
from .. import oauth2


router = APIRouter(
    tags=["Sentences"],
    prefix="/projects/{project_id}/sentences"
)


# Create sentences
@router.post("/", response_model=list[schemas.Sentence])
def create_sentence(project_id: int, sentences: list[schemas.SentenceCreate], db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    # Only admins can create sentences
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User `{user.username}` does not have the necessary privileges."
        )

    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such project with id `{project_id}`."
        )

    try:
        assert type(sentences) == list

    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Expects object of type `list`. Got `{type(sentences)} instead.`"
        )

    created_sentences = []
    for sentence in sentences:
        created_sentences.append(crud.create_sentence(
            db=db, sentence=sentence, project_id=project_id))

    return created_sentences


# Get sentence
@router.get("/{sentence_id}", response_model=schemas.Sentence)
def get_sentence(project_id: int, sentence_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
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

    db_sentence = crud.get_sentence(db=db, sentence_id=sentence_id)

    if db_sentence is None or db_sentence.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such sentence with id `{sentence_id}` is associated with project with id `{project_id}`"
        )

    return db_sentence


# Get a set of sentences
@router.get("/", response_model=list[schemas.Sentence])
def get_sentences(project_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
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

    return crud.get_project_sentences(db=db, project_id=project_id, skip=skip, limit=limit)
