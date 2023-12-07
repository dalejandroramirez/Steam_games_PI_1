from fastapi import APIRouter

from os import path
import ast

import pandas as pd 

router = APIRouter()

@router.get("/user_for_genre/{user_id}")
def user_for_genre(genres: str):
  """ Debe retornar el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento del juego\n. 
      Args:
        genre (str): Genero del juego.
    """
  try:
    
    path_endpoint_02 = path.join('data','clear','02_user_for_genre_data.csv.gz')
    
    consulta_02 = pd.read_csv(path_endpoint_02,index_col=['index'])
      
    user_max = consulta_02.loc[genres].nombre
    
    dic_years = ast.literal_eval(consulta_02.loc[genres].year)

    dic_years['Horas_Jugadas']  = dic_years.pop('playtime_forever')

    return ({f"Usuario con más horas jugadas para Género {genres}" : user_max ,"Horas Jugadas" : dic_years['Horas_Jugadas']}) 


  except Exception as e:
    return {f'Upps, el genero: {genres} no se encuntra en nuestra lista...'}
