from fastapi import APIRouter

from os import path
import ast

import pandas as pd 


router = APIRouter()

@router.get("/users_not_recommend/{user_id}")
def user_reviews_not_recommend(year: int):
  """Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. 
    (reviews.recommend = False y comentarios negativos)\n
  Args:
      year (int): Año en el que se posteó el comentario.
  """
  try:
    path_endpoint_4 = path.join('data','clear','04_users_recommend_not_recommend.csv.gz')
    table_4 = pd.read_csv(path_endpoint_4)
    
    top_3 = table_4[['app_name','recommend']][table_4['year_posted']==year].groupby('app_name').sum().nlargest(3,'recommend').reset_index()
    
    diccionario_resultado = {f'Puesto{i+1}': juego for i, juego in enumerate(top_3['app_name'])}
    
    if len(diccionario_resultado) == 0:
      return(f'Lamento que para el año {year} no te podemos recomendar intenta entre 2011 y 2015')
    
    return [diccionario_resultado]
  except Exception as e:
    return(f'Upps... Ocurrio el siguiente error... {e}')