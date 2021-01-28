web:gunicorn app:app
web:gunicorn twitoff:APP -t -120
web:python3 -m download spacy
web:python3 -m spacy download en_core_web_sm && sh setup.sh && streamlit