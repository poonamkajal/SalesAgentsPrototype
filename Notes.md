# Notes

## Create a new app

1. Create a new folder
2. Add the following files: `.env, requirements.txt, app.py`
3. Add API key to `.env` file: `GROQ_API_KEY=your-api-key`
3. Add list of dependencies to requirements.txt
```
streamlit 
langchain 
langchain-core 
langchain-community 
langchain-groq 
python-dotenv
```

4.Open a terminal/powershell or gitbash and change directory to your new folder:
`cd new-directory-name` 
5. Create a new virtual environment:
`python -m venv .venv`
6. Activate virtual environment:
Windows:`.\.venv\bin\activate` Mac: `source .\.venv\Scripts\activate`
7. Install dependencies: `pip install -r requirements.txt`
8. Start building your app!
9. Run the app: `python app.py` or `streamlit run app.py`