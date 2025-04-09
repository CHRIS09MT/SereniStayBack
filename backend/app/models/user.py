from pydantic import Field, EmailStr, field_validator
from typing import Literal, Optional, ClassVar
from passlib.context import CryptContext
from app.models.base_model import BaseEntity


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    

class User_Base(BaseEntity):
    first_name: str = Field(..., min_length=1, max_length=30)
    middle_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr = Field(..., min_length=1, max_length=40)
    role: Literal["Client", "Owner"] = Field(...)

    @field_validator("first_name")
    @classmethod
    def verify_first_name(cls, value):
        """
        Verifying that first_name only receives 1 argument
        """

        if " " in value:
            raise ValueError("first_name should contain only one word")
        return value
    

    @field_validator("middle_name")
    @classmethod
    def verify_second_name(cls, value):
        """
        Verifying that middle_name only receives 1 argument
        """

        if value is not None and " " in value:
            raise ValueError("middle_name should contain only one word")
        return value

class Create_User(User_Base):
    password: str = Field(..., min_length=8, max_length=60)

    
    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Returns the hashed password"""
        return pwd_context.hash(password)
    
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["hashed_password"] = data.pop("password")
        return data
    
class User(User_Base):
    hashed_password: str

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify if the entered password matches the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)
