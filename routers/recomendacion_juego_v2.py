from fastapi import APIRouter

from os import path
import pandas as pd 

from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk.corpus import stopwords


router = APIRouter()

@router.get('/recomendacion_juego_v2/{item_id}')
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
    # nltk.download('stopwords')
    
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


