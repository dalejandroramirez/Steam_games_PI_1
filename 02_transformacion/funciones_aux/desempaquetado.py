import gzip, ast
import pandas as pd

def desempaquetado_users_items(path_json):
  """ el archivo users_items contiene una columan con una lista de diccionarios que contiene información
      del usuario y el juego. Esta función desempaqueta este diccionario para convertir cada elemento de cada diccionario
      como un dataframe.
  Args:
      path_json (sty): ruta del archivo de entrada
  
  Returns:
      df: (dataframe) : Retorna la información como un dataframe
  """
  fila = []
  with gzip.open(path_json, 'rt', encoding='MacRoman') as archivo:
    for line in archivo.readlines():
      fila.append(ast.literal_eval(line)) # Retorna un objeto lista de forma literal
    
    df = pd.DataFrame(fila) ## leemos cada una de las filas
    
    ## desanidad el contenido de items y se agrega una nueva
    ## fila por cada elemento deitems y reseteamos los indices de la serie
    df = df.explode('items').reset_index()

    ## Eliminamos los indices pasados (repetidos)
    df = df.drop(columns="index")

    ## Concatenamos con user_id con todas las columans aplanadas del json.
    data_plana = pd.json_normalize(df['items'])[['playtime_forever','item_id']]
    df = pd.concat([df['user_id'], data_plana ], axis=1)
    
    
    return df
  
  
def desempaquetado_reviews(path_json):
  """ el archivo reviews contiene una columanma llamada reviews con una lista de diccionarios que contiene información
      del usuario y las reviews. Esta función desempaqueta este diccionario para convertir cada elemento de cada diccionario
      como un dataframe.
  Args:
      path_json (sty): ruta del archivo de entrada

  Returns:
      df: (dataframe) : Retorna la información como un dataframe
  """
  fila = []
  with gzip.open(path_json, 'rt', encoding='MacRoman') as archivo:
    for line in archivo.readlines():
      fila.append(ast.literal_eval(line)) # Retorna un objeto lista de forma literal
    
    df = pd.DataFrame(fila) ## leemos cada una de las filas
    
    ## desanidad el contenido de items y se agrega una nueva
    ## fila por cada elemento deitems y reseteamos los indices de la serie
    df = df.explode('reviews').reset_index()

    ## Eliminamos los indices pasados (repetidos)
    df = df.drop(columns="index")

    ## Concatenamos con user_id con todas las columans aplanadas del json.
    data_plana = pd.json_normalize(df['reviews'])
    df = pd.concat([df['user_id'], data_plana ], axis=1)
        
    return df