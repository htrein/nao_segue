import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

st.title("👥 Quem eu sigo que não me segue de volta")

st.subheader("📖 Como exportar seus arquivos do Instagram")

st.markdown("""
1. Acesse **Configurações** no Instagram  
2. Vá em **Central de contas**  
3. Clique em **Suas informações e permissões**  
4. Escolha **Exportar suas informações**  
5. Clique em **Criar exportação**  
6. Selecione **Exportar para dispositivo**  
7. Em **Personalizar informações**, marque apenas **Seguidores e seguindo**  
8. Clique em **Iniciar exportação**  
9. Aguarde a confirmação por email e faça o download do arquivo `.zip`  

Depois de baixar:  
- **Descompacte** o arquivo `.zip`  
- Entre no diretório: `connections/followers_and_following/`  
- Lá estarão os arquivos:  
  - `followers_1.html`  
  - `following.html`  

👉 Faça upload desses dois arquivos abaixo:
""")

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

