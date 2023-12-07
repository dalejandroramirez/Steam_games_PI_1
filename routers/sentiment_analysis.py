from fastapi import APIRouter

from os import path
import pandas as pd 

router = APIRouter()

@router.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
  """Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.\n

  Args:
      (int): Año de lanzamiento del juego.
  """
  try:
    path_endpoint_5 = path.join('data','clear','05_sentyment_analysis.csv.gz')
    table_3 = pd.read_csv(path_endpoint_5)
    
    table_3 = table_3[table_3['release_year'] == year]
    return({f"Negative = {table_3.iloc[0,1]}, Neutral = {table_3.iloc[0,2]}, Positive= {table_3.iloc[0,3]}"})  
  
  except Exception as e:
    return(f'Upps... Ocurrio el siguiente error... {e}')