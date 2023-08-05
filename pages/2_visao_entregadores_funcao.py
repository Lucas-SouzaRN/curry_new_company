# LIBRARIES
from haversine import haversine 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title ="Visão Entregadores", layout = "wide")  # comoando para expandir o grafico 


#-------------------------------------------------------
#             Funções
#-------------------------------------------------------
def top_delivers (df1, top_asc ): # vou receber o DF1 que vai fazer uma uma seleção/agrupamento 
    
    df2 = df1.loc[:, ["Time_taken(min)", "City","Delivery_person_ID" ]].groupby(["City", "Delivery_person_ID"]).max().sort_values(["Time_taken(min)", "City"], ascending = top_asc).reset_index()
# COmo foi colocado a flag "top_asc" para a proveitar a função para as duas situações, temos que colocar ela no "ascending = top_asc" pois para cada situação ela vai mudar. Quando for True ou False
    
    df2_aux1 = df2.loc[df2["City"] == "Metropolitian", :].head(10)  # encontra os 10 maiores 
    df2_aux2 = df2.loc[df2["City"] == "Urban", :].head(10)
    df2_aux3 = df2.loc[df2["City"] == "Semi-Urban", :].head(10)

    df3= pd.concat([df2_aux1, df2_aux2, df2_aux3]).reset_index(drop = True)  # concatena

    return df3



def clean_code(df1):
    """ esta função tem a responsavbbilidade de limpar o DataFrame

        Tipos de limpoeza:
        1. Removação dos dados NaN
        2. Mudfanã do tipo de coluna de dados
        3. Removação dos espaços das variaveis de texto
        4. formatção da coluna de datas
        5. Limpeza da coluna tempo ( removação do texto da variavel numerica)

        input: Dataframe
        Output: Dataframe
      """
    # TIRANDO OS NaN 
    linhas_selec = df1 ["Delivery_person_Age"] != "NaN "
    df1 = df1.loc[linhas_selec,:].copy()
    
    linhas_selec3 =df1["Road_traffic_density"] != "NaN "
    df1 = df1.loc[linhas_selec3, :].copy()
    
    linhas_selec4 = df1["City"] != "NaN "
    df1 = df1.loc[linhas_selec4, :].copy()
    
    linhas_selec5 = df1["Festival"] != "NaN "
    df1 = df1.loc[linhas_selec5, :].copy()
    
    df1["Delivery_person_Age"] = df1["Delivery_person_Age"].astype(int)
    
    
    # CONVERTENDO DE TEXTO PARA NUMERO DECIAL (FLOAT)
    df1["Delivery_person_Ratings"] = df1["Delivery_person_Ratings"].astype(float)
    
    # CONVERTENDO DE TEXTO PARA DATA 
    df1["Order_Date"]=pd.to_datetime(df1 ["Order_Date"], format='%d-%m-%Y')
    
    # LIMPANDO OS NaN E CONVERTENDO DE TEXTO PARA NUMERO INTEIRO (INT)
    linhas_selec2 = (df1["multiple_deliveries"] != "NaN ")
    df1 =df1.loc[linhas_selec2, :].copy()
    df1["multiple_deliveries"] = df1["multiple_deliveries"].astype(int)
    
    # REMOVENDO OS ESPAÇOS 
    df1.loc[:, "ID" ] = df1.loc[:, "ID"].str.strip()
    df1.loc[:, "Road_traffic_density" ] = df1.loc[:, "Road_traffic_density"].str.strip()
    df1.loc[:, "Type_of_order" ] = df1.loc[:, "Type_of_order"].str.strip()
    df1.loc[:, "Type_of_vehicle" ] = df1.loc[:, "Type_of_vehicle"].str.strip()
    df1.loc[:, "City" ] = df1.loc[:, "City"].str.strip()
    df1.loc[:, "Festival"] = df1.loc[:, "Festival"].str.strip()
    
    # LIMPANDO A COLUNA TIME TAKEN
    df1["Time_taken(min)"] = df1["Time_taken(min)"].apply(lambda x: x.split( "(min) ")[1])
    df1["Time_taken(min)"] = df1["Time_taken(min)"].astype(int)
    
    return df1




# IMPORT DATASET
df = pd.read_csv( "train.csv")

# Limpando o dataset
df  = clean_code(df)


# ================================================
#              BARRA LATERAL
# ================================================
st.header("Marketplace - Visão Entregadores")

#image_path = "curry.png"         # cria a variavel para botar o caminho/ onde está no seu PC  # tem que deixcar na mesma pasta # Importar o PIL nas biblios
image = Image.open("curry.png")    # para puxar a imagem do HD/PC precisar usar a biblioteca Image.open ( image_path = caminho / onde está no PC)
st.sidebar.image( image, width=120)  # (aceita a variavel image, tamanho do arquivo)

st.sidebar.markdown("# Cury Company")                       # 1# = fonte de um titulo  com # é a maior fonte 
st.sidebar.markdown("## Fastest Delivery in Town ")        # 2# = fonte de um subtitulo  
st.sidebar.markdown("""___""")                             # cria uma linha horizontal para separar

st.sidebar.markdown( " ## Selecione um data limite")
date_slider =st.sidebar.slider(                             # guardar em um variavel
    " Até qual data:", 
    value=datetime(2022, 4, 13),                # esse value vai ser o valor que vai ser assumido se o usuario não mexer em nada e converter para formato data
    min_value=datetime (2022, 2, 11),           # colocar a data minima 
    max_value=datetime(2022, 4,6) ,             # colocar a data maxima 
    format = 'DD-MM-YYYY')                        # parametro que quero qeu apareça do filtro

# QUERO DESCOBRIR A DATA MINIMA, ENTÃO EU COLOCO AQUI NO CODIGO O DF1 E VAI APARECEWR O BANCO DE DADOS NA PAGIONA WEB
#st.dataframe( df1 )


#st.header(date_slider)    comando para mostrar a data
st.sidebar.markdown("""___""")

traffic_options=st.sidebar.multiselect( " Quais as condições do trânsito:", ["Low", "Medium", "High", "Jam"], default = ["Low", "Medium", "High", "Jam"])
# o valor default é o valor assumido quando o usuario não digitar nada 
# guardar em um variavel
st.sidebar.markdown("""___""")
st.sidebar.markdown("### Powered by Comunidade DS")

# FILTROS  de DATA #
linhas_selec = df["Order_Date"] < date_slider # Vai fazer com que a data que colocar o date_slider vai assumir esse valor 
df1=df.loc[linhas_selec,:]

# FILTROS  de transito #
linhas_selec=df1["Road_traffic_density"].isin(traffic_options)  # .isin() passa uma lista e verifica se oq eu vc passou está dentro dessa lista 
df1= df.loc[linhas_selec,:]                                      # o usuario vais passar a lista e escolher as opções, isso filtra as opções que ele escolheu 


# ================================================
#              layout no STREAMLIT
# ================================================

tab1, tab2, tab3=st.tabs(["Visão Gerencial", "__", "__"])

with tab1:
    with st.container():
        st.markdown("# Overall Metrics")         # aqui vai ser como se fosse a primeira linha ( ela vai ser qubrada em 4 colunas)
        col1, col2, col3, col4 = st.columns(4, gap="large") # comando st.columns() para criar as colunas e o parametro gap = large para distancia enter ele 
                                                            # e depois declara as variaveis para cada coluna
        with col1:         # vamos colocar as informações/graficos para cada coluna 
            
            maior_idade = df1.loc[:,"Delivery_person_Age"].max()   # cria uma variavel para o resultado que vai receber a  maior idade
            col1.metric("Maior idade", maior_idade) # vai exibir como uma metrica então faz esse comando  
          
        
        with col2:
          
             menor_idade = df1.loc[:,"Delivery_person_Age"].min()
             col2.metric("Menor idade", menor_idade)

        with col3:
            
             melhor_veic = df1.loc[:,"Vehicle_condition"].max()
             col3.metric("Melhor Veículo", melhor_veic)

        with col4:
            
             pior_veic =  df1.loc[:,"Vehicle_condition"].min()
             col4.metric("Pior Veículo", pior_veic)
    
    with st.container():
         st.markdown("______________")
         st.markdown("# Avaliações")
         
         col1, col2 = st.columns(2)   # criando as colunas 
         with col1:
             st.markdown("#### Avaliação Média por Entregador")

             df_media_entregas_por_entregador = df_media_entregas_por_entregador =df1.loc[:, ["Delivery_person_ID", "Delivery_person_Ratings"]].groupby(["Delivery_person_ID"]).mean().reset_index()   # o resultado da consulta e coloquei em uma variável
             
             st.dataframe(df_media_entregas_por_entregador) # esse é o comando para exibvir DatFrame/dados

             
         with col2:
            st.markdown("### Avaliação Média por Trânsito")
            media_std_avaliacao_por_densidade = df1.loc[:, ["Delivery_person_Ratings", "Road_traffic_density"]].groupby(["Road_traffic_density"]).agg({"Delivery_person_Ratings": ["mean", "std"]})
             
            media_std_avaliacao_por_densidade.columns = ["entregas_media", "entregas_std"] # mudança nome da coluna

            media_std_avaliacao_por_densidade = media_std_avaliacao_por_densidade.reset_index()  # resetando o index

            st.dataframe(media_std_avaliacao_por_densidade)
             
             
            st.markdown("#### Avaliação Média por Clima")

            media_std_avaliacao_por_clima = df1.loc[:, ["Delivery_person_Ratings", "Weatherconditions"]].groupby(["Weatherconditions"]).agg({"Delivery_person_Ratings": ["mean", "std"]})

            media_std_avaliacao_por_clima.columns = ["entregas_media", "entregas_std"]
            media_std_avaliacao_por_clima=media_std_avaliacao_por_clima.reset_index()
            st.dataframe(media_std_avaliacao_por_clima)

    with st.container():
        st.markdown("______________")
        st.markdown("# Velocidade de Entrega")

        col1,col2 = st.columns(2)

        with col1:
            
            
            st.markdown("##### Top Entregadores mais Rápidos")

   # Os comandos das duas colunas fazem a mesma coisa, a única diferença é que a ordenação. Uma do mais lento e aoutra do amis rápido então o que mudamos na função é só o True ou False no ascending
# por isso foi colocado a flag "top_asc" pois dessa maneira posso usar o "top_delivers" para as duas situaçãos usando a mesma função
            
            df3 = top_delivers(df1, top_asc=True)   #df3 recebe top_delivers(df1)    
            st.dataframe(df3)

        with col2:
            
            st.markdown("##### Top Entregadores mais Lentos")
            df3 = top_delivers(df1, top_asc=False)   #df3 recebe top_delivers(df1)
            st.dataframe(df3) # exibe o DF

            
