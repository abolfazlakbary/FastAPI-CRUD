from fastapi import FastAPI, HTTPException
import mysql.connector
from fastapi.openapi.models import Response
from pydantic import BaseModel
from Movie import Movie

mydb = mysql.connector.connect(host="localhost",user="root",password="",database="python")
mycursor = mydb.cursor()
app = FastAPI()

#root
@app.get("/")
async def root():
    return {"message":"welcome"}

#get all movies
@app.get("/movies")
def get_movies():
    sql = "SELECT * FROM movies"
    mycursor.execute(sql)
    movies = mycursor.fetchall()
    return movies

#get a single movie by id
@app.get("/movie/{movie_id}")
def get_movie(movie_id:int):
    sql = "SELECT * FROM movies WHERE id= %s"
    val = (movie_id,)
    mycursor.execute(sql, val)
    movie = mycursor.fetchall() #it returns an array of arrays / [[]]
    if len(movie) == 0:
        raise HTTPException(status_code=500, detail="Movie not found")
    return movie[0] #it returns an array / []

#get a single movie by title
@app.get("/movie_by_title/{movie_title}")
def get_movie_by_title(movie_title:str):
    sql = "SELECT * FROM movies WHERE title= %s"
    val = (movie_title,)
    mycursor.execute(sql, val)
    movie = mycursor.fetchall() #it returns an array of arrays / [[]]
    if len(movie) == 0:
        raise HTTPException(status_code=500, detail="Movie not found")
    return movie[0] #it returns an array / []

#create a movie
@app.post("/create_movie")
def create_movie(movie:Movie):
    sql = "INSERT INTO movies (title,year,storyline) VALUES (%s,%s,%s)"
    val = (movie.title, movie.year, movie.storyline)
    mycursor.execute(sql, val)
    mydb.commit() #Whenever you are adding a new item in database, use this command
    return movie

#update a movie
@app.post("/update_movie")
def update_movie(movie:Movie,movie_id:int):
    sql = "UPDATE movies SET title=%s , year=%s , storyline=%s WHERE id=%s"
    val = (movie.title, movie.year, movie.storyline, movie_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return movie

#delete a single movie
@app.delete("/movie/{movie_id}")
def delete_movie(movie_id:int):
    sql = "DELETE FROM movies WHERE id=%s"
    val = (movie_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message":"Movie has been deleted successfully"}

#uvicorn main:app --reload / Run the uvicorn server with this command