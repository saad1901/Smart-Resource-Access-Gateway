from pydantic import BaseModel, Field
from datetime import datetime, time
from uuid import UUID

class UpiInBody(BaseModel):
    name : str
    upi_id : str
    nickname : str

class UpiOutBody(BaseModel):
    id : int
    name : str
    upi_id : str
    nickname : str
    
class EventOut(BaseModel):
    title : str
    max_participants : int
    status : str
    start_date : datetime | None = None
    address : str | None = None
    created_at : datetime
    slug : str
    tournament_time : time
    city : str
    prize_pool : int
    updated_at : datetime
    venue : str
    state : str
    tournament_format : str
    contact_email : str
    description : str
    registration_deadline : datetime
    country : str
    rules : str
    contact_phone : str
    category_id : int
    postal_code: str | None = None
    whatsapp_number : str
    min_participants : int
    is_featured : bool
    end_date : datetime
    entry_fee : float
    upi_id_id : int
    
    # class Config:
    #     orm_mode = True

class EventIn(BaseModel):
    title : str
    max_participants : int
    status : str
    start_date : datetime
    address : str
    created_at : datetime
    slug : str
    tournament_time : time
    city : str
    prize_pool : int
    updated_at : datetime
    venue : str
    state : str
    tournament_format : str
    contact_email : str
    description : str
    registration_deadline : datetime
    country : str
    rules : str
    contact_phone : str
    category_id : int
    postal_code: str
    whatsapp_number : str
    organizer_id : int
    min_participants : int
    is_featured : bool
    end_date : datetime
    entry_fee : float
    upi_id_id : int
  
class UserIn(BaseModel):
    username : str
    password : str

class UserAdd(BaseModel):
    username     : str
    password     : str
    email        : str
    first_name   : str
    last_name    : str 

class OrgOut(BaseModel):
    name : str
    add : str | None = None
    phone : str | None = None
    wp : str | None = None
    email : str | None = None

class OrgIn(BaseModel):
    name : str
    add : str | None = None
    phone : str | None = None
    wp : str | None = None
    email : str | None = None

class ParticipantOut(BaseModel):
    full_name : str
    registration_id : UUID
    status : str
    registration_date : datetime | None = None
    address : str | None = None
    email : str | None = None
    phone : str | None = None
    wp : str
    transaction_id : int | None = None
    tournament_id : int | None = None
    age : int | None = None