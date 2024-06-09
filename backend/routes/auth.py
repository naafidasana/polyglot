from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import database, schemas, models, crud
from .. import utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Attempt sign in with provided credentials (username and password)
    db_user: models.User = crud.get_user(
        db=db, username=user_credentials.username)

    if not db_user:
        # No user with provided username
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email or password is incorrect."
        )

    # Verify password for fetched user
    if not utils.verify(plain_password=user_credentials.password, hashed_password=db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email or password is incorrect."
        )

    # Create and return access token
    access_token = oauth2.create_access_token(
        data={"username": db_user.username, "is_admin": db_user.is_admin}
    )

    return {"access_token": access_token, "token_type": "bearer"}
