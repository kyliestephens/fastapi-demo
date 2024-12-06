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
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        cur.close()
        db.close()
        return(json_data)
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()   
    query = """
    SELECT
        s.title,
        s.album,
        s.artist,
        s.year,
        s.file AS file,
        s.image AS image,
        g.genre AS genre  # Use 'g' for genre from genres table
    FROM songs s
    JOIN genres g ON s.genre = g.genreid  # Use 's' for songs and 'g' for genres
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]  # Get column names for headers
        results = cur.fetchall()  # Fetch all results
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))  # Combine headers with values to form a dictionary
        cur.close()
        db.close()
        return json_data  # FastAPI will return this as JSON
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}



# FastAPI endpoint to get songs
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


