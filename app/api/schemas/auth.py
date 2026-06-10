from pydantic import BaseModel, ConfigDict, Field, EmailStr


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class RegisterResponse(BaseModel):
    user_id: str
    username: str


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class LoginResponse(BaseModel):
    user_id: str
    username: str


class LoginJWTResponse(LoginResponse):
    access_token: str


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    username: str
