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
  


# def sentiment_analysis( año : int ): 
#   """Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
#   """
#   pass


@app.get('/user_for_genre/{genre}')
def user_for_genre(genre: str):
    path_endpoint_2 = path.join('data','clear','02_user_for_genre_data.csv.gz')
    table_2 = pd.read_csv(path_endpoint_2)

    # Filtro la tabla para quedarme únicamente con registros que contengan el género deseado
    genre_filter = table_2[table_2['genres'].str.contains(genre)]

    # Usuarios con la suma de su tiempo de juego 
    df_sum_play_time = genre_filter.groupby(['user_id'])['playtime_forever'].sum()

    # Usuario con más horas jugadas en total
    if not df_sum_play_time.empty:
        user_max_time = df_sum_play_time.idxmax()
    else:
        return {'message': 'No existe usuario que haya jugado este juego'}

    # Filtrar solo por los registros del usuario con mayor tiempo de juego
    user_filter = genre_filter[genre_filter['user_id'] == user_max_time][['release_year', 'playtime_forever']]

    # Sumamos las horas jugadas del usuario por año
    user_filter_sum = user_filter.groupby('release_year').sum().reset_index()

    target = user_filter_sum.rename(columns={'release_year': 'year', 'playtime_forever': 'total_horas'}).to_dict(orient='records')
    return {f"Usuario con más horas jugadas para Género {genre}": user_max_time, "Horas jugadas": target}

@app.get('/user_reviews_recommend/{year}')
def user_reviews_recommend(year: int):
  path_endpoint_3 = path.join('data','clear','03_users_recommend.csv.gz')
  table_3 = pd.read_csv(path_endpoint_3)
  
  top_3 = table_3[['app_name','recommend']][table_3['year_posted']==year].groupby('app_name').sum().nlargest(3,'recommend').reset_index()
  
  diccionario_resultado = {f'Puesto{i+1}': juego for i, juego in enumerate(top_3['app_name'])}
  
  return [diccionario_resultado]


@app.get('/user_not_reviews_recommend/{year}')
def user_reviews_not_recommend(year: int):
  path_endpoint_4 = path.join('data','clear','04_users_recommend_not_recommend.csv.gz')
  table_4 = pd.read_csv(path_endpoint_4)
  
  top_3 = table_4[['app_name','recommend']][table_4['year_posted']==year].groupby('app_name').sum().nlargest(3,'recommend').reset_index()
  
  diccionario_resultado = {f'Puesto{i+1}': juego for i, juego in enumerate(top_3['app_name'])}
  
  if len(diccionario_resultado) == 0:
    return('Este año nadie recomendó')
  
  return [diccionario_resultado]

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
  path_endpoint_5 = path.join('data','clear','05_sentyment_analysis.csv.gz')
  table_3 = pd.read_csv(path_endpoint_5)
  
  table_3 = table_3[table_3['release_year'] == year]
  
  return({f"Negative = {table_3.iloc[0,1]}, Neutral = {table_3.iloc[0,2]}, Positive= {table_3.iloc[0,3]}"})  


def recomendacion_juego (): 
  """Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
Si es un sistema de recomendación user-item:"""
  pass



def recomendacion_usuario(): 
  """Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario."""
  pass