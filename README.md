# twitoff-22
Flask web application to compare twitter users.

## Changes I made:

- add SQLite database to Heroku keys

- changed all imports to include directory name:
  from .models import * -> from twitoff.models import *

- Procfile:
  web gunicorn --chdir twitoff __init__:APP

- in requirements.txt:
  add https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
  set thinc==7.4.0
  set blis==0.4.1

- in twitter.py:
  import en_core_web_sm
  nlp = en_core_web_sm.load()
