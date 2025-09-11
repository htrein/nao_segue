import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

st.title("👥 Quem eu sigo que não me segue de volta")

st.write("Faça upload dos dois arquivos exportados do Instagram:")

followers_file = st.file_uploader("Carregar **Followers**", type=["html"])
following_file = st.file_uploader("Carregar **Following**", type=["html"])

if followers_file and following_file:
    # Ler os arquivos
    followers_html = followers_file.read().decode("utf-8")
    following_html = following_file.read().decode("utf-8")

    # Extrair usernames
    followers = [a.text.strip() for a in BeautifulSoup(followers_html, "html.parser").find_all("a")]
    following = [a.text.strip() for a in BeautifulSoup(following_html, "html.parser").find_all("a")]

    # Quem você segue mas não te segue de volta
    not_following_back = [u for u in following if u not in followers]

    # Mostrar resultado
    df = pd.DataFrame(not_following_back, columns=["username"])
    st.subheader("🚫 Usuários que você segue mas não seguem de volta:")
    st.dataframe(df, use_container_width=True)

    # Botão para baixar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="nao_seguem_de_volta.csv",
        mime="text/csv"
    )
