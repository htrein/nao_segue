import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

st.title("👥 Who I Follow That Don't Follow Me Back")

st.subheader("📖 How to export your Instagram data")

st.markdown("""
1. Open **Settings** in the Instagram app or web
2. Go to **Accounts Center**
3. Click **Your information and permissions**
4. Choose **Download your information** (Export)
5. Click **Create export**
6. Select **Download to device**
7. Under **Customize information**, check only **Followers and Following**
8. Click **Start export**
9. Wait for the confirmation email and download the `.zip` file

After downloading:
- **Unzip** the `.zip` file
- Enter the folder: `connections/followers_and_following/`
- You should find these files:
  - `followers_1.html`
  - `following.html`

👉 Upload those two files below:
""")

followers_file = st.file_uploader("Upload Followers HTML file", type=["html"])
following_file = st.file_uploader("Upload Following HTML file", type=["html"])

if followers_file and following_file:
    # Read uploaded files
    followers_html = followers_file.read().decode("utf-8")
    following_html = following_file.read().decode("utf-8")

    # Extract usernames from href when possible (e.g. /username/). Normalize to lowercase.
    def extract_usernames(html):
        soup = BeautifulSoup(html, "html.parser")
        users = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # user profiles usually look like '/username/'
            if href.startswith("/") and not href.startswith("/p/") and not href.startswith("/explore"):
                username = href.strip("/").split("/")[0]
                if username:
                    users.add(username.lower())
        # fallback: if no usernames found via href, use visible text
        if not users:
            for a in soup.find_all("a"):
                txt = a.text.strip()
                if txt:
                    users.add(txt.lower())
        return sorted(users)

    followers = extract_usernames(followers_html)
    following = extract_usernames(following_html)

    # Users you follow who don't follow you back
    # Lowercasing already applied; use sets for efficiency
    followers_set = set(followers)
    not_following_back = [u for u in following if u not in followers_set]

    # Mostrar resultado
    df = pd.DataFrame(not_following_back, columns=["username"])
    st.subheader("🚫 Users you follow who don't follow you back:")
    st.dataframe(df, use_container_width=True)

    # Botão para baixar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
      label="📥 Download CSV",
        data=csv,
      file_name="not_following_back.csv",
        mime="text/csv"
    )

