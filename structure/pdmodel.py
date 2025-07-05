from pydantic import BaseModel, Field
from datetime import datetime, time

class UpiInBody(BaseModel):
    name : str
    upi_id : str
    nickname : str
    
class EventOut(BaseModel):
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
    passwword : str