import pandas as pd 
from fastapi import FastAPI
from os import path


app = FastAPI()

@app.get('/play_time_genres/{genero}')
def play_time_genres(genero: str):
  """Calcula el año con mayor tiempo jugado por el genero dado
  Returns:
      dic: diccionario con el año con mayor tiempo jugado
  """  
  genero = genero.capitalize()
  path_endpoint_1 = path.join('data','clear','01_play_time_genre_data.csv.gz')
  try:
    tabla1 = pd.read_csv(path_endpoint_1, compression='gzip')
    year_max =tabla1[tabla1['genres'].str.contains(genero)][['release_year','playtime_forever']].groupby('release_year').sum().idxmax().iloc[0]
    return {'Año': str(year_max)}
  
  except ValueError as e :
    return {f'Upps, el genero: {genero} no se encuntra en nuestra lista'}
  


# def UserForGenre( genero : str ):
#   """"
#   el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
#   """


# def UsersNotRecommend( año : int ): 
#   """Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
#   Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
#   """
#   pass

# def sentiment_analysis( año : int ): 
#   """Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
#   """
#   pass


# @app.get('/endpoint2/{genre}')
# def user_for_genre(genre: str):
#     path_endpoint_2 = path.join('data','clear','02_user_for_genre_data.csv.gz')
#     table_2 = pd.read_csv(path_endpoint_2)

#     # Filtro la tabla para quedarme únicamente con registros que contengan el género deseado
#     genre_filter = table_2[table_2['genres'].str.contains(genre)]

#     # Usuarios con la suma de su tiempo de juego 
#     df_sum_play_time = genre_filter.groupby(['user_id'])['playtime_forever'].sum()

#     # Usuario con más horas jugadas en total
#     if not df_sum_play_time.empty:
#         user_max_time = df_sum_play_time.idxmax()
#     else:
#         return {'message': 'No existe usuario que haya jugado este juego'}

#     # Filtrar solo por los registros del usuario con mayor tiempo de juego
#     user_filter = genre_filter[genre_filter['user_id'] == user_max_time][['release_year', 'playtime_forever']]

#     # Sumamos las horas jugadas del usuario por año
#     user_filter_sum = user_filter.groupby('release_year').sum().reset_index()

#     target = user_filter_sum.rename(columns={'release_year': 'year', 'playtime_forever': 'total_horas'}).to_dict(orient='records')
#     return {f"Usuario con más horas jugadas para Género {genre}": user_max_time, "Horas jugadas": target}
