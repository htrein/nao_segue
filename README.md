This small Streamlit app helps you find Instagram accounts you follow that don't follow you back.

How to use
1. Export your Instagram data and include only Followers and Following. Make sure to set the Data/Date range to "All time" so the export includes your entire history.
2. Download and unzip the archive.
3. Open the folder `connections/followers_and_following/` and locate `followers_1.html` and `following.html`.
4. Run the app and upload those two files.

Run locally
```bash
python3 -m pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

Then open http://localhost:8501 in your browser.
