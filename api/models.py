from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    reservations = relationship("Reservation", back_populates="user")

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, index=True)
    name_room = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="name_room")

class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    date_reservation = Column(Date, nullable=False)
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)

    user = relationship("User", back_populates="reservations")
    name_room = relationship("Room", back_populates="reservations")