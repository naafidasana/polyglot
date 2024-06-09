from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..db import database, schemas, crud
from .. import oauth2


router = APIRouter(
    tags=["Projects"],
    prefix="/projects"
)


# Create project
@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    if not user.is_admin:
        # Only admins can create projects.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User `{user.username}` does not have the necessary privileges."
        )

    db_project = crud.get_project_by_name(db=db, project_name=project.name)

    if db_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is an already existing project with name `{project.name}`."
        )

    return crud.create_project(db=db, project=project)


# Get project
@router.get("/{project_id}/", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    db_project = crud.get_project(db=db, project_id=project_id)

    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such project with id `{project_id}`."
        )

    # Only admin or annotators of project can access the project
    if not user.is_admin or user.username not in [annotator.username for annotator in db_project.annotators]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User `{user.username}` does not have the necessary privileges."
        )

    return db_project


# Delete Project
@router.delete("/{project_id}/", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    # Only admins can delete projects
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User `{user.username}` does not have the necessary privileges."
        )

    try:
        db_project = crud.delete_project(db=db, project_id=project_id)

        return db_project

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No such project with id `{project_id}`."
        )
