from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..db import database, schemas, crud


router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


# Create user
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db=db, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username `{user.username}` is already taken."
        )

    return crud.create_user(db=db, user=user)


# Get specific user
@router.get("/{username}/", response_model=schemas.User)
def get_user(username: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db=db, username=username)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User `{username}` not found."
        )

    return db_user


# Get set of users
@router.get("/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)

    return users


# Update user
@router.put("/{username}/", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, username: str, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.update_user(db=db, username=username, user=user)

        return db_user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User `{username}` not found."
        )


@router.delete("/{username}/", response_model=schemas.User)
def delete_user(username: str, db: Session = Depends(database.get_db)):
    try:
        db_user = crud.delete_user(db=db, username=username)

        return db_user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User `{username}` not found."
        )
