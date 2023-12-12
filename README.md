# Steam Games

<p align="center">
  <img width="50%" src="images/01_logo_steam.jpeg" alt="Interfaz de Usuario">
</p>
Este proyecto interactua con una base de datos de la plataforma steam. Podras encontrar información sobre:

- El año con mayor tiempo jugado por el genero dado.
- Usuario con mayor tiempo de juego por año de lanzamiento de juego.
- Recomendación de juegos.
- Analisis de sentimientos sobre comentarios de usuarios.
- Recomendación de juegos con un modelo entrenado.
- Analisis descriptivo con información cuantitativa de los datos.

**NOTA**: También puedes usar las funciones accediendo al enlace [Documentación](https://proyecto-1-2019.onrender.com/docs) que corresponde a la API deployada en Render.

## Contenido

1. [Introducción](#introducción)
2. [Configuración](#configuración)
3. [Uso](#uso)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Contribución](#contribución)
6. [Licencia](#licencia)

## Introducción

Breve introducción al proyecto, explicando su propósito y contexto en ML Ops.

## Configuración
- Para poder replicar este proyecto deberas clonar el repositorio, luego crear un entorno virtual ya sea un entorno de python, docker ó anacondas. Instalas los requerimientos necesario para en el archivo requirements.txt.

- El archivo principal se llama main.py en el encontraras las funciones que realizamos en este proyecto, ademas, encontraras en la carpeta **03_Endpoints**  explicación detallada de la construcción de cada función.


## Uso
Dentro del entorno de ejecución de fastapi encontraras los endpoints requeridos para este proyecto:
:
* `/play_time_genre`: Calcula el año con mayor tiempo jugado por el genero dado.

* `/user_for_genre`: Dado un genero. Debe retornar el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento del juego.

* `/user_recommned`: Dado un año, devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

* `/user_not_recommend`: Dado un año, devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.

* `/sentiment_Analysis`: Dado un año de lanzamiento, devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento


* `/recomendacion_juego`: Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

**NOTA**: También puedes usar las funciones accediendo al enlace https://proyecto-1-2019.onrender.com/docs, que corresponde a la API deployada en Render.


# Estructura del Proyecto
En este repositorio podras encontrar la siguiente estructura.
- **data**: Encontraras dos carpetas, raw y clear. En la carpeta raw se encuetra la data cruda y sin tratamientos inciales, mientras que en la carpeta clear encontraras la data tratada para poder trabajar con ella de manera eficiente, ademas de tener las tablas requeridas para cada consulta.
- **01_Transforamción**: Encontraras las transformaciones preliminares que realizamos en la base de  datos para la correcta manipulación de los archivos. Ademas una carpeta llamanda **funciones_aux**, esta carpeta fue diseñada para ser un modulo de python lo que permitirá escalabilidad del nootbook en caso de necesitar creación de nuevas consultas.
- **02_Eda**
- **03_Endpoints** : En esta carpeta encontraras cada una de las funciones que se realizaron en este proyecto, en diferentes nootbook, ademas de la creación de la tabla consulta,  se realiza una explicación detallada del analisis de cada función asi como un ejemplo ilustrativo de la respuesta de cada endpoint.
- **routers** En esta carpeta encontraras las funciones ya listas para ser consumidas por la api.
- **main.py**  Este es el archivo principal en el que se encuentra condensado toda la lógica que sera consumida por la API.


# Contacto
Daniel Alejandro Ramírez Gómez.

- LinkedIn: [dalejandro.ramirez.dev](https://www.linkedin.com/in/daniel-alejandro-ram%C3%ADrez-g%C3%B3mez-704616229/)

- Correo electrónico: dalejandro.ramirez.dev@gmail.com

# Tecnologías utilizadas
Python | Pandas | Matplotlib | Seaborn | Scikit-Learn | nltk | FastAPI | Render | Jinja2 

```bash
pip install -r requirements.txt
