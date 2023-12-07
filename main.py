from os import path
from fastapi import FastAPI
from routers import play_time_genre
from routers import user_for_genre
from routers import user_recommend
from routers import user_not_recommend
from routers import sentiment_analysis
from routers import recomendacion_juego
from routers import recomendacion_juego_v2

import pandas as pd 
import ast

app = FastAPI()

app.include_router(play_time_genre.router, tags=["Play Time Genres"])

app.include_router(user_for_genre.router, tags=["User For Genres"])

app.include_router(user_recommend.router, tags=["Users Recommend"])

app.include_router(user_not_recommend.router, tags=["Users Not Recommend"])

app.include_router(sentiment_analysis.router, tags=["Sentiment Analysis"])

app.include_router(recomendacion_juego.router, tags=["Analisis de Recomendacion"])

app.include_router(recomendacion_juego_v2.router, tags=["Analisis de Recomendacion"])
