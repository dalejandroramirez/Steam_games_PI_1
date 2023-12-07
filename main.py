from os import path
from fastapi import FastAPI
from routers import play_time_genre
from routers import user_for_genre


import pandas as pd 
import ast

from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk.corpus import stopwords


app = FastAPI()

app.include_router(play_time_genre.router, tags=["Play Time Genres"])

app.include_router(user_for_genre.router, tags=["User For Genres"])

  
#Endpoint 03
@app.get('/user_reviews_recommend/{year}')
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

#Endpoint 04
@app.get('/user_not_reviews_recommend/{year}')
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
      return(f'Lamento que para el año {year} no te podemos recomendar intenta entre 2010 y 2015')
    
    return [diccionario_resultado]
  except Exception as e:
    return(f'Upps... Ocurrio el siguiente error... {e}')

#Endpoint 05
@app.get('/sentiment_analysis/{year}')
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

#Endpoint06
@app.get('/recomendacion_juego/{id}')
def recomendacion_juego(id :int):
  """ Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

  Args:
      id (int): Es el indicie de un juego que tuvi reviews y se encuentra en steam
  Returns:
      list : Retorna una lista con el top 5 de juegos mas similares por palabras. 
  """
  path_endpoint_6 = path.join('data','clear','06_recomendacion_juego.csv.gz')
  df= pd.read_csv(path_endpoint_6).sample(10000)
  
  
  try:
    nombre_juego = df.set_index('steam_id').loc[id].values[0].split(',')[0]

    df['correlacion'] = 0
    if id in df['steam_id']:
      text_1 = df[df['steam_id'] == id]['features'].iloc[0]
    else:
      return('Ups... No tenemos este id. Intenta nuevamente.')
    nltk.download('stopwords')
    
    #Eliminaremos las stopwords
    stop_words_steams = ['op','based','co','first']
    stop = list(stopwords.words('english'))
    stop += stop_words_steams

    def score_ml(text):
      data_corpus = [text_1, text]  
      tf = TfidfVectorizer(stop_words=stop)

      tf_idf_matrix_df =tf.fit_transform(data_corpus)
      
      return(linear_kernel(tf_idf_matrix_df,tf_idf_matrix_df)[0,1])

    df['correlacion'] = df['features'].apply(score_ml)
    
    df= df.sort_values('correlacion',ascending=False)[1:6]
    
    df['features'] = df['features'].apply(lambda x: x.split(',')[0])
    
    texto=df['features'].values
    
    return {'Juego': nombre_juego ,'Similares':list(texto)}
    return list(texto)
  
  except Exception as e:
    return(f'Upps Al parecer al parecer la muestra no tiene este juego, intenta nuevamente')
      
  
@app.get('/recomendacion_juego_v2/{item_id}')
def recomendacion_juego_v2(item_id :int):
  """ Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

  Args:
      id (int): Es el indicie de un juego que tuvi reviews y se encuentra en steam
  Returns:
      list : Retorna una lista con el top 5 de juegos mas similares por palabras. 
  """
  try:
    path_endpoint_06 = path.join('data','clear','06_recomendacion_juego_v2.csv.gz')
    consulta_06 = pd.read_csv(path_endpoint_06)
    nombre_juego = consulta_06.set_index('item_id').loc[item_id].values[0].split(',')[0]

    #Eliminaremos las stopwords
    nltk.download('stopwords')
    
    stop_words_steams = ['aaaaaa', 'ab', 'abbey','abe', 'abramenko']
    stop = list(stopwords.words('english'))
    stop += stop_words_steams


    tf = TfidfVectorizer(stop_words=stop, token_pattern=r'\b[a-zA-Z]\w+\b' )

    data_vector = tf.fit_transform(consulta_06['features'])

    data_vector_df = pd.DataFrame(data_vector.toarray(), index=consulta_06['item_id'], columns = tf.get_feature_names_out())
      
    vector_similitud_coseno = cosine_similarity(data_vector_df.values)

    cos_sim_df = pd.DataFrame(vector_similitud_coseno, index=data_vector_df.index, columns=data_vector_df.index)

    ##top5
    juegos_similares = cos_sim_df.loc[item_id].nlargest(6)

    top5 = juegos_similares.iloc[1:6]

    resultado = consulta_06.set_index('item_id').loc[top5.index]['features'].apply(lambda x: x.split(',')[0]).values
    
    
    return {'Juego':nombre_juego,'Similares':list(resultado)}
  except KeyError as e:
    
    return(f'Upps... al parecer este juego no  lo tenemos.')
