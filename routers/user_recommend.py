from fastapi import APIRouter

from os import path
import ast

import pandas as pd 


router = APIRouter()

@router.get("/users_recommend/{user_id}")
def user_reviews_recommend(year: int):
  """ Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
      (reviews.recommend = True y comentarios positivos/neutrales)\n
  Args:
      year (int): Año de lanzamiento del juego 
  """
  try:
    path_endpoint_3 = path.join('data','clear','03_users_recommend.csv.gz')
    table_3 = pd.read_csv(path_endpoint_3)
    
    top_3 = table_3[['app_name','recommend']][table_3['year_posted']==year].groupby('app_name').sum().nlargest(3,'recommend').reset_index()
    
    diccionario_resultado = {f'Puesto{i+1}': juego for i, juego in enumerate(top_3['app_name'])}
    if len(diccionario_resultado) > 0:
      return [diccionario_resultado]
    else:
      return(f'Lamento que para el año {year} no te podemos recomendar intenta entre 2010 y 2015')
  
  except ValueError as e :
    return(f'Upps... Ocurrio el siguiente error... {e}')
