from memory_profiler import profile


import pandas as pd
import os

path_user = os.path.join('..','data','clear','users_items.csv.gz')
path_steam_games = os.path.join('..','data','clear','steam_games.csv.gz')

@profile
def user_for_genre(genre :str):
  
  path_endpoint_2 = os.path.join('..','data','clear','02_user_for_genre_data.csv.gz')
  table_2 = pd.read_csv(path_endpoint_2,compression='gzip')
  
  # path_endpoint_2 = os.path.join('..','data','clear','02_user_for_genre_data.csv.gz')
  # table_2 = pd.read_parquet('example2.parquet.gz')

  ## Filtro la tabla para quedarme unicamente con registros que contengan el genero deseado
  genre_filter = table_2[table_2['genres'].str.contains(genre)]
  
  ## usuario con mayor tiempo de juego acumulado
  df_sum_play_time =  genre_filter[['user_id','playtime_forever']].groupby(['user_id']).sum()
  
  # usuario con mas horas jugadas en total
  if len(df_sum_play_time) > 0:
    user_max_time = df_sum_play_time.idxmax().iloc[0]
  else:
    return ('No existe usuario que haya jugado este juego')
  
  ## Filtraremos solo por los registros del usuario con mayor tiempo de juego
  ## nos quedamos con el año de lanzamiento y el tiempo de juego
  user_filter = genre_filter.loc[genre_filter['user_id'] == user_max_time,['release_year','playtime_forever']]
  
  # Sumamos las horas jugadas del usuario por añoprofile
  user_filter_sum = user_filter.groupby('release_year').sum().reset_index()
  
  target = user_filter_sum.rename(columns={'release_year':'year'})[['year', 'playtime_forever']].to_dict(orient='records')
  
  return {f"Usuario con más horas jugadas para Género {genre}" : user_max_time, "Horas jugadas": target}


print(user_for_genre('Action')
)
