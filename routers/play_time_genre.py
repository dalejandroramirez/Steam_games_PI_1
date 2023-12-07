from fastapi import APIRouter
from os import path
import pandas as pd


router = APIRouter()

@router.get("/play_time_genres/{user_id}")
def play_time_genres(genero: str):
  """Calcula el año con mayor tiempo jugado por el genero dado\n.
  """  
  genero = genero.capitalize()
  path_endpoint_1 = path.join('data','clear','01_play_time_genre_data.csv.gz')
  try:
    tabla1 = pd.read_csv(path_endpoint_1, compression='gzip')
    year_max =tabla1[tabla1['genres'].str.contains(genero)][['release_year','playtime_forever']].groupby('release_year').sum().idxmax().iloc[0]
    return {f'Año de lanzamiento con más horas jugadas para Género {genero}': str(year_max)}
  
  except Exception as e :
    return {f'Upps, el genero: {genero} no se encuntra en nuestra lista...'}
 