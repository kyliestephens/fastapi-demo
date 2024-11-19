#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import mysql.connector
from mysql.connector import Error
import json
import os

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "uqj5uw"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DB
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# FastAPI endpoint to get songs
@app.get('/songs')
def get_songs():
    connection = get_db_connection()
    if connection is None:
        return {"Error": "Could not connect to the database"}
    
    query = """
        SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre 
        FROM songs
        JOIN genres ON songs.genre = genres.genreid;
    """
    
    try:
        cur = connection.cursor()  # Create cursor object here
        cur.execute(query)  # Execute the query
        headers = [x[0] for x in cur.description]  # Get column names from the cursor description
        results = cur.fetchall()  # Fetch all results
        
        # Convert results into a list of dictionaries
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        if connection.is_connected():
            connection.close()  # Make sure to close the connection



@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "API!"}

@app.get("/sum/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@app.get("/divide/{e}/{f}")
def divide(e: int, f: int):
    return {"answer": e / f}


