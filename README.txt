Movie Recommender System
========================

Project Overview:
-----------------
This is a content-based movie recommender system built using Python.
It uses cosine similarity between movie feature vectors to suggest similar titles.

How to Run:
-----------
1. Create a virtual environment (optional but recommended):
   > python -m venv venv
   > venv\Scripts\activate        # On Windows
   > source venv/bin/activate     # On Linux/Mac

2. Install dependencies:
   > pip install -r requirements.txt

3. Run the application:
   > python app.py

Files Included:
---------------
- app.py               : Main application script
- movie_list.pkl       : Pickled list of movie titles
- similarity.pkl       : Pickled similarity matrix
- requirements.txt     : Python dependencies
- README.txt           : Project instructions

Notes:
------
- Python 3.8+ recommended
- Ensure all `.pkl` files are in the same directory as `app.py`
- This project uses Git LFS for large file tracking (on GitHub)


run in CMD:
direct to directory: cd path/Movie_recommrnder
to run app.py: python -m streamlit run app.py
