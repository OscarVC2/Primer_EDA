import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

applicationdb = pd.read_csv(r'/Users/oscarandresvalladarescardona/Desktop/Data Science Bootcamp/Proyecto EDA/archive (1)/application_data.csv')
previousappdb = pd.read_csv(r'/Users/oscarandresvalladarescardona/Desktop/Data Science Bootcamp/Proyecto EDA/archive (1)/previous_application.csv')
columns_descriptiondb = pd.read_excel('/Users/oscarandresvalladarescardona/Desktop/Data Science Bootcamp/Proyecto EDA/archive (1)/columns_description.xlsx')

options =st.sidebar.selectbox("Selecciona una pagina", ("Home", "Datos de Application", "Datos de Previous Data", "Dashboard"))
if options == "Home":

    st.title("Credit Database")
    image = Image.open(r"/Users/oscarandresvalladarescardona/Desktop/Data Science Bootcamp/Proyecto EDA/archive (1)/2666312.jpeg")
    st.image(image)

    with st.beta_expander("Resumen"):
        st.write("""Introducción 
        
Este caso de estudio tiene como objetivo dar una idea de la aplicación de EDA en un escenario empresarial real. En este caso de estudio, desarrollaremos una comprensión básica de la analítica de riesgos en los servicios bancarios y financieros y comprenderemos cómo se utilizan los datos para minimizar el riesgo de perder dinero mientras prestamos a los clientes.

Comprensión empresarial
Las empresas proveedoras de préstamos tienen dificultades para otorgar préstamos a las personas debido a su historial crediticio insuficiente o inexistente. Por eso, algunos consumidores lo utilizan como una ventaja al convertirse en morosos. Supongamos que trabajamos para una empresa de financiación al consumo que se especializa en prestar varios tipos de préstamos a clientes urbanos. Tendremos que utilizar EDA para analizar los patrones presentes en los datos. Esto garantizará que los solicitantes capaces de reembolsar el préstamo no sean rechazados.

Cuando la empresa recibe una solicitud de préstamo, la empresa debe decidir la aprobación del préstamo en función del perfil del solicitante. Hay dos tipos de riesgos asociados con la decisión del banco:
Si es probable que el solicitante reembolse el préstamo, no aprobar el préstamo da como resultado una pérdida de negocio para la empresa.
Si no es probable que el solicitante reembolse el préstamo, es decir, es probable que incumpla, la aprobación del préstamo puede generar una pérdida financiera para la empresa.
Los datos que se proporcionan a continuación contienen la información sobre la solicitud de préstamo en el momento de solicitar el préstamo. Contiene dos tipos de escenarios:
El cliente con dificultades de pago: tuvo un atraso de más de X días en al menos una de las primeras Y cuotas del préstamo en nuestra muestra,
Todos los demás casos: Todos los demás casos en los que el pago se paga a tiempo.
Cuando un cliente solicita un préstamo, existen cuatro tipos de decisiones que podría tomar el cliente / empresa):

Aprobado: la empresa ha aprobado la solicitud de préstamo

Cancelada: el cliente canceló la aplicación en algún momento durante la aprobación. O el cliente cambió de opinión sobre el préstamo o, en algunos casos, debido a un mayor riesgo del cliente, recibió peores precios que no quería.

Rechazado: La empresa había rechazado el préstamo (porque el cliente no cumple con sus requisitos, etc.).

Oferta no utilizada: el cliente ha cancelado el préstamo pero en diferentes etapas del proceso.

En este caso de estudio, usaremos EDA para comprender cómo los atributos del consumidor y los atributos del préstamo influyen en la tendencia al incumplimiento.

Objetivos de negocios
Este caso de estudio tiene como objetivo identificar patrones que indiquen si un cliente tiene dificultades para pagar sus cuotas que pueden ser utilizadas para tomar acciones como denegar el préstamo, reducir el monto del préstamo, prestar (a solicitantes de riesgo) a una tasa de interés más alta, etc. Esto garantizará que los consumidores capaces de devolver el préstamo no sean rechazados. La identificación de estos solicitantes mediante EDA es el objetivo de este estudio de caso.
En otras palabras, la empresa quiere comprender los factores impulsores (o variables impulsoras) detrás del incumplimiento del préstamo, es decir, las variables que son fuertes indicadores del incumplimiento. La empresa puede utilizar este conocimiento para su cartera y evaluación de riesgos.

Comprensión de datos

Este conjunto de datos tiene 3 archivos como se explica a continuación:
'application_data.csv' contiene toda la información del cliente en el momento de la aplicación.
Los datos se refieren a si un cliente tiene dificultades de pago.
'previous_application.csv' contiene información sobre los datos de préstamos anteriores del cliente. Contiene los datos de si la solicitud anterior había sido aprobada, cancelada, rechazada o oferta no utilizada.
'column_description.csv' es un diccionario de datos que describe el significado de las variables.""")
    st.write(columns_descriptiondb[columns_descriptiondb.columns[1:4]])

if options == "Datos de Application":
    st.write("La base de datos esta compuesta de la siguiente manera", applicationdb.shape)
    st.write("La base de datos cuenta con", len(applicationdb.select_dtypes(include = "object").columns), "datos categoricos")
    st.write("La base de datos cuenta con",len(applicationdb.select_dtypes(include=["int64","float64"]).columns), "variables numericas")
    st.write("A continuacion se presenta el resumen de aquellas columnas con datos numericos")
    st.write(applicationdb.describe())

    null_count = applicationdb.isnull().sum()
    null_percentage = round((applicationdb.isnull().sum() / applicationdb.shape[0]) * 100, 2)
    null_df = pd.DataFrame(
        {'column_name': applicationdb.columns, 'null_count': null_count, 'null_percentage': null_percentage})
    null_df.reset_index(drop=True, inplace=True)
    st.write("Luego de distinguir las variables numericas, se determino que variables contaban con mayor cantidad de valores nulos")
    st.write(null_df.sort_values(by = 'null_percentage', ascending = False))

    st.write("Luego se procede a eliminar aquellas variables cuyo porcentaje sea mayor al 40%")
    eliminar_columnas = null_df[null_df['null_percentage'] > 40].column_name.to_list()
    st.write("Se eliminan",len(eliminar_columnas), "columnas")
    applicationdb.drop(columns=eliminar_columnas, inplace=True)
    null_menor40 = null_df[null_df['null_percentage'] < 40]
    st.write(null_menor40.sort_values(by='null_percentage', ascending=False))

    st.write("La variable Occupation type tenia el mayor numero de valores desconocidos")
    applicationdb['OCCUPATION_TYPE'].fillna(value='Other', inplace=True)

    st.write("A continuacion se presenta el grafico de Occupation type luego de reemplazar valores desconocidos")
    st.write(plt.figure(figsize=(10, 5)), sns.countplot(data=applicationdb, x="OCCUPATION_TYPE"), plt.xticks(rotation=90), plt.show());

    st.write("A continuacion se presenta la variable Name Type Suite")
    st.write(plt.figure(figsize=(10, 5)), sns.countplot(data=applicationdb, x="NAME_TYPE_SUITE"), plt.xticks(rotation=90), plt.show());

    st.write("Luego se procede a verificar errores en otras columnas")
    st.write(applicationdb[applicationdb['CODE_GENDER'] == 'XNA'])

    applicationdb['CODE_GENDER'] = applicationdb['CODE_GENDER'].apply(lambda x: 'F' if x == 'XNA' else x)
    applicationdb['DAYS_BIRTH'] = applicationdb['DAYS_BIRTH'].apply(lambda x: -x if x < 0 else x)
    applicationdb['YEARS_BIRTH'] = applicationdb['DAYS_BIRTH'].apply(lambda x: round(x / 365))
    applicationdb['NAME_FAMILY_STATUS'] = applicationdb['NAME_FAMILY_STATUS'].apply(lambda x: 'Married' if x == 'Unknown' else x)
    applicationdb['DAYS_EMPLOYED'] = applicationdb['DAYS_EMPLOYED'].apply(lambda x: -x if x < 0 else x)
    applicationdb['YEARS_EMPLOYED'] = applicationdb['DAYS_EMPLOYED'].apply(lambda x: round(x / 365))
    applicationdb['DAYS_REGISTRATION'] = applicationdb['DAYS_REGISTRATION'].apply(lambda x: -x if x < 0 else x)
    applicationdb['YEARS_REGISTRATION'] = applicationdb['DAYS_REGISTRATION'].apply(lambda x: round(x / 365))
    applicationdb['DAYS_ID_PUBLISH'] = applicationdb['DAYS_ID_PUBLISH'].apply(lambda x: -x if x < 0 else x)
    applicationdb['DAYS_LAST_PHONE_CHANGE'] = applicationdb['DAYS_LAST_PHONE_CHANGE'].apply(lambda x: -x if x < 0 else x)

if options == "Datos de Previous Data":
    st.write("La base de datos esta compuesta de la siguiente manera", previousappdb.shape)
    st.write("La base de datos cuenta con", len(previousappdb.select_dtypes(include="object").columns),
             "datos categoricos")
    st.write("La base de datos cuenta con", len(previousappdb.select_dtypes(include=["int64", "float64"]).columns),
             "variables numericas")
    st.write("A continuacion se presenta el resumen de aquellas columnas con datos numericos")
    st.write(previousappdb.describe())

    null_count = previousappdb.isnull().sum()
    null_percentage = round((previousappdb.isnull().sum() / previousappdb.shape[0]) * 100, 2)
    null_df = pd.DataFrame(
        {'column_name': previousappdb.columns, 'null_count': null_count, 'null_percentage': null_percentage})
    null_df.reset_index(drop=True, inplace=True)
    st.write(
        "Luego de distinguir las variables numericas, se determino que variables contaban con mayor cantidad de valores nulos")
    st.write(null_df.sort_values(by='null_percentage', ascending=False))

    eliminar_columnas = null_df[null_df['null_percentage'] > 40].column_name.to_list()
    previousappdb.drop(columns=eliminar_columnas, inplace=True)
    null_menor40 = null_df[null_df['null_percentage'] < 40]
    null_menor40.sort_values(by='null_percentage', ascending=False)


if options == "Dashboard":
    import streamlit as st
    import streamlit.components.v1 as components
    htmfile = open('/Users/oscarandresvalladarescardona/Desktop/Data Science Bootcamp/Proyecto EDA/archive (1)/Dashboard.html', 'r', encoding = "utf-8")
    source_code=htmfile.read()
    components.html(source_code, height = 1016, width =1200)



