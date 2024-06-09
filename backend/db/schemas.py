from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    gender: Optional[str | None] = None
    age: Optional[int | None] = None
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str | None] = None


class User(UserBase):

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class SentenceBase(BaseModel):
    text: str
    language_iso: str


class SentenceCreate(SentenceBase):
    pass


class Sentence(SentenceBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


class TranslationBase(BaseModel):
    text: str
    language_iso: str


class TranslationCreate(TranslationBase):
    annotator_username: str


class Translation(TranslationBase):
    id: int

    class Config:
        from_attributes = True


class RecordingBase(BaseModel):
    audio_file_path: str
    language_iso: str


class RecordingCreate(RecordingBase):
    annotator_username: str


class Recording:
    id: int

    class Config:
        form_attributes = True


class ProjectBase(BaseModel):
    name: str
    p_type: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    annotators: list[User] = []

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    role: str
    username: str
    project_id: int


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str | None] = None
    is_admin: bool
