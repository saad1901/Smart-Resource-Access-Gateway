from pydantic import Field, BaseModel

class UserIn(BaseModel):
    username     : str
    password     : str
    email        : str
    first_name   : str
    last_name    : str
    is_active    : bool
    is_staff     : bool
    is_superuser : bool