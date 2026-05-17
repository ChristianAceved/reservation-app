from pydantic import BaseModel, EmailStr
from datetime import date, time

# Esquema que valida lo que el cliente nos ENVIA para crear un nuevo usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Esquema que valida lo que nosotros le DEVOLVEREMOS al cliente ( sin incluir llave para mas seguridad )
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

# Esquema para crear una nueva sala
class RoomCreate(BaseModel):
    name_room: str
    capacity: int

# Esquema para devolver la informacion de una sala al cliente
class RoomResponse(BaseModel):
    id: int
    name_room: str
    capacity: int

# Esquema para crear una nueva reserva
class ReservationCreate(BaseModel):
    user_id: int
    room_id: int
    date_reservation: date
    time_start: time
    time_end: time

# Esquema para devolver la informacion de una reserva al cliente
class ReservationResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_reservation: date
    time_start: time
    time_end: time

# Esquema para poder trabajar con JWT (Json Web Tokens) y devolver la informacion del token al cliente
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True