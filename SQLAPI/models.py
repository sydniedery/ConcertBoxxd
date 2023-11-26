from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Concerts(Base):
    __tablename__ = "Concert"
    ID = Column(Integer, primary_key=True, index=True, nullable=False) 
    Mbid = Column(String)
    Date = Column(String)
    Artist = Column(String)
    Tour = Column(String) 
    City = Column(String)
    State = Column(String) 
    Venue = Column(String)

    songs = relationship('Concert_Songs', back_populates='concert')

    def __repr__(self):
        return f"<Concerts(ID={self.ID}, Mbid ='{self.Mbid},Date='{self.Date}', Artist='{self.Artist}', Tour='{self.Tour}', City='{self.City}', State='{self.State}', Venue='{self.Venue}')>"

class ConcertsCreate(BaseModel):
    ID: int
    Mbid: str
    Date: str
    Artist: str
    Tour: str
    City: str
    State: str
    Venue: str
class ConcertsRead(ConcertsCreate):
    class Config:
        orm_mode = True

class Songs(Base):
    __tablename__ = "Song"
    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)

    concerts = relationship('Concert_Songs', back_populates='song')

    def __repr__(self):
        return f"<Songs(ID={self.ID}, Name='{self.Name}')>"

class SongCreate(BaseModel):
    ID: int
    Name: str

class SongRead(SongCreate):
    class Config:
        orm_mode = True

class Concert_Songs(Base):
    __tablename__ = "Concert_Song"
    Concert_ID = Column(ForeignKey('Concert.ID'), primary_key=True)
    Song_ID = Column(ForeignKey('Song.ID'), primary_key=True)

    concert = relationship('Concerts', back_populates='songs')
    song = relationship('Songs', back_populates='concerts')

    def __repr__(self):
        return f"<Concert_Songs(Concert_ID={self.Concert_ID}, Song_ID='{self.Song_ID}')>"

class Concert_SongsCreate(BaseModel):
    Concert_ID: int
    Song_ID: int


class Concert_SongsRead(Concert_SongsCreate):
    class Config:
        orm_mode = True
