import streamlit as st
from PIL import Image

# essa função vai juntar as 3 paginas, e tem que buscar os arqwuivos dentro dae uma pagina page
st.set_page_config(
    page_title="Home"
    
)

 

#image_path = "\\Users\\Cliente\\Documents\\Repos\\ftc_programacao_python\\dataset\\" 
image = Image.open( "curry.png")
st.sidebar.image( image, width = 200)

st.sidebar.markdown("# Cury Company")                       # 1# = fonte de um titulo  com # é a maior fonte 
st.sidebar.markdown("## Fastest Delivery in Town ")        # 2# = fonte de um subtitulo  
st.sidebar.markdown("""___""")                             # cria uma linha horizontal para separar


st.write ("# Curry Company Growth Dashboard") # titulo


# IR NA MONITORIA SABER O PQ QUE NÃO DEU CERTO E PERGUNTAR DO EMOJI TMB 
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dsos entregadores e restauranrtes.
        
        ### Como utilizar esse Growth Dashboard?
       - Visão Empresa:
           - Visão Gerencial: Métricas gerais de comportamento 
           - Visão Tática: Indicadores semanais de Crescimento 
           - Visão Geografica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento 
    - Visào Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
""")
