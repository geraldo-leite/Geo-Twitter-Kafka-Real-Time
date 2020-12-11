FROM python:3

RUN pip install pykafka && pip install spacy && pip install tweepy && pip install Flask && python -m spacy download pt_core_news_sm

COPY . /app

WORKDIR /app

CMD python tweet_pln.py
