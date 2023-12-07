from fastapi import APIRouter

from os import path
import pandas as pd 

from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk.corpus import stopwords


router = APIRouter()

@router.get('/recomendacion_juego/{item_id}')
def recomendacion_juego(item_id :int):
  """ Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

  Args:
      id (int): Es el indicie de un juego que tuvi reviews y se encuentra en steam
  Returns:
      list : Retorna una lista con el top 5 de juegos mas similares por palabras. 
  """
  path_endpoint_6 = path.join('data','clear','06_recomendacion_juego.csv.gz')
  df= pd.read_csv(path_endpoint_6)
  
  try:
    nombre_juego = df.set_index('steam_id').loc[item_id].values[0].split(',')[0]

    df['correlacion'] = 0
    if item_id in df['steam_id']:
      text_1 = df[df['steam_id'] == item_id]['features'].iloc[0]
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
