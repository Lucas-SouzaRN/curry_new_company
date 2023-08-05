# LIBRARIES
from haversine import haversine 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title ="Visão Restaurantes", layout = "wide")  # comoando para expandir o grafico 


#-------------------------------------------------------
#             Funções
#------------------------------------------------------- 
def avg_std_time_on_traffic(df1):

    aux3 = df1.loc[:, ["Time_taken(min)", "City","Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).agg({"Time_taken(min)": ["mean", "std"]})

    aux3.columns = ["media_tempo", "std_tempo"]
    aux3 = aux3.reset_index()

    fig = px.sunburst(aux3, path=["City", "Road_traffic_density"], values="media_tempo", color="std_tempo", color_continuous_scale="RdBu", color_continuous_midpoint=np.mean(aux3["std_tempo"]))
    return fig 



def avg_std_time_graph(df1):
  
    aux1 = df1.loc[:, ["Time_taken(min)", "City"]].groupby("City").agg({"Time_taken(min)": ["mean", "std"]})

    aux1.columns = ["media_tempo", "std_tempo"]

    aux1 = aux1.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar ( name="Control", x=aux1["City"], y=aux1["media_tempo"], error_y=dict( type ="data", array=aux1["std_tempo"])))
    # esse error_y= é o desvrio padrçao, que bota  a barrinha 

    fig.update_layout(barmode="group")

    return fig



def media_std_time_delivery(df1, festival, op):
    
    # o que muda de um para outro é a operação então passo o DF1 que vai sofrer as opreções e um parametro OP # se for a média faz como tava na coluna 3 se for std faz como tava na coluna 4
# vamos colocar outro parametro na função, pois nas colunas 3 e 4 era com o festival, nas proximas colunas são sem o festival. Tbm temos que mudar no filtro e colocar igual ao parametro 
     
                
               # Está função calcula o tempo medio e o desvido padra do tempo de entrega.
               # Paramentros: 
                  #  input: 
                    #    - df: DataFrame com os dados necessários para o calculo
                     #   - op: Tipo de operção que precisa ser calculado
                      #      "media_tempo": calcula o tempo médio
                     #       "std_tempo": calcula o desvio padrão
                   # Output:
                        #- df: DataFrame com 2 colunas e uma linha
                
                
    aux4 = df1.loc[:, ["Time_taken(min)","Festival"]].groupby("Festival").agg({"Time_taken(min)": ["mean", "std"]})

    aux4.columns = ["media_tempo", "std_tempo"]

    aux4 = aux4.reset_index()    # precisa resetar o index antes 

    linahs_selec = aux4 ["Festival"] == festival
    aux4 = np.round(aux4.loc[linahs_selec, op], 2)  # o comando np.round(2) é para dizer quantos numeros quero após a virgula # tive que colocar o parametro OP no cular de MEDIA_TEMPO

    return aux4 




def distance(df1, fig):
# na coluna 1 da Distribuição de Tempo o codigo é muito parecido, entçao vamos aproveityyar essa função acrescentando mais um parametro e utilizando if/else
# e a Fig vai ser igual a Treu ou False, no if retorna o valor da média e no else retorna uma figura 
    if fig == False:
        colunas = ["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"]
    
        df1["distancia"]=df1.loc[:, colunas].apply ( lambda x: 
                               haversine((x["Restaurant_latitude"], x["Restaurant_longitude"]), 
                                         (x["Delivery_location_latitude"], x["Delivery_location_longitude"])), axis=1)
    
        media_distancia =np.round( df1["distancia"].mean(), 2) # O comando NP.ROUND(valor que vc quer , quantos numeros depois da virgula  ).é um redutor
        return media_distancia
   
    else:
        colunas = ["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"]
    
        df1["distancia"]=df1.loc[:, colunas].apply ( lambda x: 
                               haversine((x["Restaurant_latitude"], x["Restaurant_longitude"]), 
                                         (x["Delivery_location_latitude"], x["Delivery_location_longitude"])), axis=1)
    
        media_distancia = df1.loc[:, ["City", "distancia"]].groupby("City").mean().reset_index()
        fig = go.Figure(data =[go.Pie(labels=media_distancia["City"], values = media_distancia["distancia"], pull = [0, 0.1, 0])]) 
        return fig 




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



#------------------------------------
# IMPORT DATASET
#------------------------------------
df = pd.read_csv( "train.csv")

#Limpando o codigo 
df1 = clean_code(df)



# ================================================
#              BARRA LATERAL
# ================================================
st.header("Marketplace - Visão Restaurantes")

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
linhas_selec = df1["Order_Date"] < date_slider # Vai fazer com que a data que colocar o date_slider vai assumir esse valor 
df1=df1.loc[linhas_selec,:]

# FILTROS  de transito #
linhas_selec=df1["Road_traffic_density"].isin(traffic_options)  # .isin() passa uma lista e verifica se oq eu vc passou está dentro dessa lista 
df1= df1.loc[linhas_selec,:]                                      # o usuario vais passar a lista e escolher as opções, isso filtra as opções que ele escolheu 


# ================================================
#              layout no STREAMLIT
# ================================================

# PRIMEIRO VAI FAZER OS 4 CONTAINERS COMO TEM NO DASHBOARD
# SEGUNDO: FAZER AS COLUNAS

tab1, tab2, tab3=st.tabs(["Visão Gerencial", "__", "__"])

with tab1:
    with st.container():
        st.markdown("## Overal Metrics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            
            delivery_unique= entreagdores_unicos = len(df1.loc[:,"Delivery_person_ID" ]. unique())   # SEMPRE GUARDAR EM UMA VARIAVEL
            col1.metric("Entregadores Únicos", delivery_unique)

        with col2:
            
            media_distancia = distance(df1, fig = False ) # A primeira chamda da função Distance e passar o fig = false 
            
            col2.metric(" O Distancia Média das entregas", media_distancia)

        with col3:
            

            aux4 = media_std_time_delivery(df1, "Yes", "media_tempo")       # como acrescentamos o parametro festival, boto o Yes pq essa seleção é com Festival
            col3.metric("Tempo Médio de Entrega com Festival", aux4)
            


           # linahs_selec = aux4 ["Festival"] == "Yes"  #v a coluna 3 é o tempo de entrega quando tem o festival
          #  aux4 = aux4.loc[linhas_selec, "media_tempo"]                                                                                                                        # Não quero todas as colunas quero apenas o tempo médio. Então vou colocar a coluna que quero : media_tempo 

        
        with col4:
            
            

            aux4 = media_std_time_delivery(df1, "Yes", "std_tempo")

            col4.metric("Desvio Padrão Médio de Entrega com Festival", aux4)


            
        with col5:  
            
            aux4 = media_std_time_delivery(df1, "No", "media_tempo")
            col5.metric("Tempo Médio de Entrega com Festival", aux4)

            
        with col6:
            
            aux4 = media_std_time_delivery(df1, "No", "std_tempo")
            col6.metric("Desvio Padrão Médio de Entrega com Festival", aux4)
        
                    

    with st.container():
        st.markdown("## Tempo Médio de Entrega por Cidade")
        col1, col2 = st.columns (2)
        with col1:
            fig = avg_std_time_graph(df1) 
        
            st.plotly_chart( fig)

        with col2:
            st.markdown("##### Distribuição da Distancia")
            aux2 = df1.loc[:, ["Time_taken(min)", "City","Type_of_order"]].groupby(["City", "Type_of_order"]).agg({"Time_taken(min)": ["mean", "std"]})

            aux2.columns = ["media_tempo", "std_tempo"]

            aux2 = aux2.reset_index()

            st.dataframe(aux2)

            # nao precisa criar uma função por ser só um agrupamento/ selecionando colunas 

      

    with st.container():
        st.markdown("## Distribuição do Tempo")   # PERGUNTAR PQ NÃO TÁ SAINDO O GRAFICO#

        col1, col2 = st.columns (2)
        with col1:
           
            fig = distance (df1, fig = True)
            st.plotly_chart(fig)



        with col2: 
             
            
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart( fig)
      

  

    
