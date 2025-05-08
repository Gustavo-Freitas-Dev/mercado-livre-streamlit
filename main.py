import streamlit as st
from scraper import raspagem

st.set_page_config(page_title="Scraper Mercado Livre", layout="centered")
st.title("🛒 Scraper Mercado Livre")

produto = st.text_input("Digite o nome do produto para buscar:", "")
if st.button("🔍 Buscar"):
    with st.spinner("Buscando produtos..."):
        resultados = raspagem(produto)
        resultados = sorted(resultados, key=lambda x:x ["Preço númerico"])
        
        if resultados:
            for idx, item in enumerate(resultados, start=1):
                st.markdown(f"**{idx}. {item['Título']}**")
                st.write(f"💲 {item['Preço']}")
                st.markdown(f"[🔗 Acessar link]({item['Link']})")
                st.markdown("----")
        else:
            st.error("Nenhum resultado encontrado")        
