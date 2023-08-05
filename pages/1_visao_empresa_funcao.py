
# LIBRARIES
from haversine import haversine 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title ="Visão Empresa", layout = "wide")  # comoando para expandir o grafico 
# ----------------------------------------------
# FUNÇÕES                              # Criar uma função de limpeza de dados
                                       # e coloca todas alim,pezas identada 
                                       # o parametro tem que ser o mesmo df

# a função escreve e desenha um grafico 
# ----------------------------------------------
def country_maps(df1): 
    
    df_aux = df1.loc[:,["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]].groupby(["City", "Road_traffic_density"]).median().reset_index()
    
    
    map = folium.Map()
    
    for index,loc_info in df_aux.iterrows():
                        
        folium.Marker( [loc_info["Delivery_location_latitude"], loc_info["Delivery_location_longitude"]], popup=loc_info[["City", "Road_traffic_density"]] ).add_to(map)
    
        folium_static(map, width= 1024, height = 600 )        # função,  folium_static(), para conseguir mostrar o MAP
        return None 



def order_share_by_week(df1):
    
    df_aux1 =df1.loc[:, ["ID", "semana_ano"]].groupby(["semana_ano"]).count().reset_index()
    df_aux2 = df1.loc[:, ["Delivery_person_ID", "semana_ano"]].groupby(["semana_ano"]).nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how ="inner")
    df_aux["pedidos_delivery"] = df_aux["ID"] / df_aux["Delivery_person_ID"]
   
    e=px.line (df_aux, x ="semana_ano", y = "pedidos_delivery")
    return e 


def order_by_week(df1):  
    df1["semana_ano"] = df1["Order_Date"].dt.strftime("%U")
    df1_aux = df1.loc[:, ["ID", "semana_ano"]].groupby(["semana_ano"]).count().reset_index()


    d=px.line(df1_aux, x = "semana_ano", y = "ID")
    return d



def traffici_order_city(df1):
    
    df_aux = df1.loc[:, ["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
                       
    c=px.scatter(df_aux, x ="City", y = "Road_traffic_density", size ="ID", color = "City" )
    return c


def traffic_order_share(df1):
    st.markdown(" # Traffic Order Share")
    df_aux = df1.loc[:, ["Road_traffic_density", "ID"]].groupby(["Road_traffic_density"]).count().reset_index()
    
    
    df_aux = df_aux.loc[df_aux["Road_traffic_density"] != "Nan ", :]
    
    
    
    df_aux["porcentagem_ent"] = df_aux ["ID"] / df_aux["ID"].sum()
    
    
    
    b=px.pie(df_aux, values = "porcentagem_ent", names = "Road_traffic_density")
    
    return b
      


def order_metric(df1):
     
    colunas =["ID", "Order_Date"]
    df1_aux =df1.loc[:, colunas].groupby(["Order_Date"]).count().reset_index()
    
        # desenahs o gráfico de linhas
    a=px.bar(df1_aux, x = "Order_Date", y = "ID")
    
    return a
# A função order_metric(df1) faz: recebe o DF, executa o DFm gera uma figura/grafico e passa a figura pra mim

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
# -------------------------------------- INICVIO DA ESTRUTURA LOGICA DO CÓDIGO ---------------------------------------------------------------------
 

# IMPORT DATASET
df = pd.read_csv( "train.csv")

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# Limpando dados 
df1 = clean_code(df)




# ================================================
#              BARRA LATERAL
# ================================================
st.header("Marketplace - Visão Cliente")

#image_path = "curry.png"         # cria a variavel para botar o caminho/ onde está no seu PC  # tem que deixcar na mesma pasta # Importar o PIL nas biblios
image = Image.open("curry.png")    # para puxar a imagem do HD/PC precisar usar a biblioteca Image.open ( image_path = caminho / onde está no PC)
st.sidebar.image( image, width=120)  # (aceita a variavel image, tamanho da imagem na pagina )

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

# criar ABAS usa o .tabs
# guardar em 3 variaveis, onde cada um vai ser uma tab/aba
tab1, tab2, tab3=st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geografica"])

# With é uma clausulka reservadia do Pythpon, tudo que tiver identado dentro do With vai ficar dentro do tab. Como se fosse topicos 
with tab1:
    with st.container(): #como que se estivesse criando uma linha la na pagina web, e nessa linha vai ficar meu primeiro grafico
         # Order Metric
        a = order_metric(df1)  # Chamou a funnção  vai retornar o grafico/figura
        st.markdown("# Orders by Day")
        st.plotly_chart(a, use_container_width=True )
               
       
    with st.container():      # criou o espaço onde o grafico vai ficar, como se fosse outra linha 
        col1, col2 = st.columns (2)  # criando duas colunas  e guarda em variaveis e para fazer/botar as coisas na coluna tenho que usar o WITH 
        with col1:
            b = traffic_order_share(df1)
            st.plotly_chart(b, use_container_width=True )                          
                        
       
        with col2:
            st.markdown(" # Traffic Order City")
            c = traffici_order_city(df1)
            st.plotly_chart(c, use_container_width=True )
        
    
with tab2:
    with st.container():
        st.markdown(" # Order by Week")
        d =  order_by_week(df1)
        st.plotly_chart(d, use_container_width=True )

               
    with st.container(): 
        
        st.markdown(" # Order Share by Week")
        e = order_share_by_week(df1)
        st.plotly_chart(e, use_container_width=True )

                  
    
with tab3: 
    st.markdown(" # Country Maps")
    country_maps(df1)
    


    