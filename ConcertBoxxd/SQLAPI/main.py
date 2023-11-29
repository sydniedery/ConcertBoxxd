import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Imports from our models.py file
from models import Base, ConcertsCreate, Concerts, ConcertsRead, SongCreate, SongRead, Songs, Concert_Songs, Concert_SongsCreate,  Concert_SongsRead

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# because we are hosting both Blazor and FastAPI on the same server (localhost), we need to enable CORS 
# to allow the Blazor client to make requests to the FastAPI server
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # set to * here to allow all origins because Blazor does not have a set origin port for all users. 
						 # Ideally, you would set this to the port that Blazor is running on (e.g. http://localhost:7134 for me)
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Set up our local database session
SQLALCHEMY_DATABASE_URL = "sqlite:///./easydb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This binds our ORM class models
Base.metadata.create_all(bind=engine)

# This function will serve as a Dependency Inversion for our db connection at our FastAPI endpoints.
# Each endpoint function will have this connection passed in as a parameter using the Depends() function.
# This is similar to Blazor's @inject directive for components.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
      
# GET requests
#@app.get("/Songs/{concertID}")
#async def get_songs(concertID: str, db: Session = Depends(get_db)):
#    db_songs = db.query(Concerts).options(joinedload(Concerts.songs)).all()
#    return db_songs

@app.get("/Songs/Count")
async def get_songcount(db: Session = Depends(get_db)):
    return db.query(Songs).count()

@app.get("/Concerts/Count")
async def get_concertcount(db: Session = Depends(get_db)):
    return db.query(Concerts).count()

@app.get("/Songs")
async def get_all_songs(db: Session = Depends(get_db)):
    song_list = db.query(Songs).all()
    
    # Here, I'm using a simple list comprehension to create the JSON response. There's a bit more overhead if we 
    # want to use a Pydantic model for the list in conjunction with the PokemonRead model.
    return [{"ID": song.ID, "name": song.Name} for song in song_list]

@app.get("/Concerts")
async def get_shows(db: Session = Depends(get_db)):
    show_list = db.query(Concerts).all()
    return [{"ID": concert.ID, "Mbid": concert.Mbid, "Date": concert.Date, "Artist": concert.Artist, "Tour" : concert.Tour, "City" : concert.City, "State": concert.State, "Venue": concert.Venue} for concert in show_list]

@app.get("/Concerts/Songs/{concertID}")
async def get_songs(concertID: int, db: Session = Depends(get_db)):
    try:
        # Assuming that concertID is the ID of the concert for which you want to get songs
        db_songs = db.query(Songs).join(Concert_Songs).filter(Concert_Songs.Concert_ID == concertID).all()
        logging.debug(f"Retrieved songs: {db_songs}")
        return db_songs
    except Exception as e:
        logging.error(f"Error getting songs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.get("/Concerts/{concertID}")
async def get_concert(concertID: int, db: Session = Depends(get_db)):
    try:
        # Assuming that concertID is the ID of the concert for which you want to get songs
        concert = db.query(Concerts).filter(Concerts.ID == concertID).first()
        logging.debug(f"Retrieved songs: {concert}")
        return concert
    except Exception as e:
        logging.error(f"Error getting concert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.get("/Songs/{songID}")
async def get_song(songID: int, db: Session = Depends(get_db)):
    try:
        # Assuming that concertID is the ID of the concert for which you want to get songs
        song = db.query(Songs).filter(Songs.ID == songID).first()
        logging.debug(f"Retrieved songs: {song}")
        return song
    except Exception as e:
        logging.error(f"Error getting song: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

#POST request
# POST request
@app.post("/Concerts")
async def add_concert(concert_create: ConcertsCreate, db: Session = Depends(get_db)):
    # Check if the concert already exists in the database
    if db.query(Concerts).filter(Concerts.ID == concert_create.ID).first() is not None:
        raise HTTPException(status_code=400, detail="Concert already exists")

    # Create a new Concert object using the ConcertsCreate model
    new_concert = Concerts(
        ID=concert_create.ID,
        Mbid=concert_create.Mbid,
        Date=concert_create.Date,
        Artist=concert_create.Artist,
        Tour=concert_create.Tour,
        City=concert_create.City,
        State=concert_create.State,
        Venue=concert_create.Venue
    )

    # Add the new Concert object to the database
    db.add(new_concert)
    db.commit()
    db.refresh(new_concert)

    # Return the new Concert object using the ConcertsRead model
    return new_concert

@app.post("/Songs")
async def add_song(song: SongCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Songs).filter(Songs.ID == song.ID).first() is not None:
        raise HTTPException(status_code=400, detail="Song already exists")

    # Create a new Pokemon object using the PokemonCreate model
    new_song = Songs(ID=song.ID, Name=song.Name)

    # Add the new Pokemon object to the database
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    # Return the new Pokemon object using the PokemonRead model
    return new_song

@app.post("/Concerts/Songs")
async def add_concert_song(info: Concert_SongsCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concert_Songs).filter((Concert_Songs.Concert_ID == info.Concert_ID)&(Concert_Songs.Song_ID == info.Song_ID)).first() is not None:
        raise HTTPException(status_code=400, detail="Song already exists")

    # Create a new Pokemon object using the PokemonCreate model
    new_song = Concert_Songs(Concert_ID=info.Concert_ID, Song_ID=info.Song_ID)

    # Add the new Pokemon object to the database
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    # Return the new Pokemon object using the PokemonRead model
    return new_song


# PUT request
@app.put("/Songs/{id}")
async def update_song(id: int, song: SongCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Songs).filter(Songs.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Song not found")

    # Update the Pokemon object in the database
    db.query(Songs).filter(Songs.ID == id).update({Songs.Name: song.Name})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Songs).filter(Songs.ID == id).first()

@app.put("/Concerts/{id}")
async def update_concert(id: int, concert: ConcertsCreate, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Date: concert.Date, Concerts.Mbid: concert.Mbid, Concerts.Artist: concert.Artist, Concerts.Tour: concert.Tour, Concerts.City: concert.City, Concerts.State: concert.State, Concerts.Venue: concert.Venue})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

    
# PATCH requests
@app.patch("/Songs/{id}/Name")
async def update_song_name(id: int, name: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Songs).filter(Songs.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Song not found")

    # Update the Pokemon object in the database
    db.query(Songs).filter(Songs.ID == id).update({Songs.Name: name})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Songs).filter(Songs.ID == id).first()

#patch concert date
@app.patch("/Concerts/{id}/Date")
async def update_concert_date(id: int, date: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Date: date})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

@app.patch("/Concerts/{id}/Mbid")
async def update_mbid(id: int, mbid: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Mbid: mbid})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

#patch concert artist
@app.patch("/Concerts/{id}/Artist")
async def update_concert_artist(id: int, artist: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Artist: artist})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

@app.patch("/Concerts/{id}/Tour")
async def update_concert_tour(id: int, tour: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Tour: tour})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

@app.patch("/Concerts/{id}/State")
async def update_concert_state(id: int, state: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.State: state})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

@app.patch("/Concerts/{id}/Venue")
async def update_concert_venue(id: int, venue: str, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Update the Pokemon object in the database
    db.query(Concerts).filter(Concerts.ID == id).update({Concerts.Venue: venue})
    db.commit()

    # Return the updated Pokemon object using the PokemonRead model
    return db.query(Concerts).filter(Concerts.ID == id).first()

# DELETE request
@app.delete("/Songs/{id}")
async def delete_song(id: int, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Songs).filter(Songs.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Song not found")

    # Delete the Pokemon object from the database
    db.query(Songs).filter(Songs.ID == id).delete()
    db.commit()

    # Return a success message
    return {"message": "Song deleted"}

@app.delete("/Concerts/{id}")
async def delete_concert(id: int, db: Session = Depends(get_db)):
    # Check if the pokemon already exists in the database
    if db.query(Concerts).filter(Concerts.ID == id).first() is None:
        raise HTTPException(status_code=404, detail="Concert not found")

    # Delete the Pokemon object from the database
    db.query(Concerts).filter(Concerts.ID == id).delete()
    db.commit()

    # Return a success message
    return {"message": "Concert deleted"}
