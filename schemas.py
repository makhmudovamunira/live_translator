from pydantic import BaseModel



class Settings(BaseModel):
    authjwt_secret_key:str = '984817fc4c33253ee20977385e23ae5c572085812c13e36e3d8a4d584cc78a34'

class SignUpModel(BaseModel):
    username: str
    email:str
    password:str

    class Config:
        from_attributes  = True
        json_schema_extra = {
            'example': {
                "username":"test",
                "email": "a@gmail.com",
                "password": "password1234"
            }
        }

class LoginModel(BaseModel):
    username_or_email: str
    password: str

    class Config:
        from_attributes  = True
        json_schema_extra = {
            'example': {
                "username": "john",
                "password": "password1234",
            }
        }
