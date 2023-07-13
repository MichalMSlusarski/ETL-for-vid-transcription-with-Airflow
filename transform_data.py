import pandas as pd
import re
import spacy
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from sentimentpl.models import SentimentPLModel

def set_stopwords(path='polish_stopwords.txt') -> list:
    with open(path, 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()
    
    return stopwords

def clean_text(text: str, stopwords: list) -> str:
    
    nlp = spacy.load("pl_core_news_sm")
    text_cleaned = ''

    text = re.sub(r'[^a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]', '', text)

    tokens = text.split()
    tokens = " ".join([i for i in text.lower().split()])
    tokens = nlp(tokens)

    clean_tokens = []

    for word in tokens:
        if word.lemma_ not in stopwords:
            clean_tokens.append(word.lemma_)

    text_cleaned = ' '.join(clean_tokens)
    text_cleaned = str(text_cleaned)

    return text_cleaned

def get_topics(text_cleaned: str, num_topics=5, num_words=3) -> list:

    tokens = simple_preprocess(text_cleaned)
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    topics = []
    for topic_id in range(num_topics):
        topic_words = lda_model.show_topic(topic_id, topn=num_words)
        topic = [(word, weight) for word, weight in topic_words]
        topics.extend(topic)

    return topics

def get_keywords(topics: list) -> list:
    keywords = []
    keywords = [word for word, _ in topics]

    keywords.sort()
    return keywords

def get_unique_keywords(keywords: list) -> str:
    key_set = set(keywords)
    unique_keywords = ', '.join(key_set)

    return unique_keywords

def get_sentiment(text: str) -> float:
    model = SentimentPLModel(from_pretrained='latest')

    sentence_sentiments = []
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        value = model(sentence).item()
        sentence_sentiments.append(value)

    sentiment = sum(sentence_sentiments) / len(sentences)
    round(sentiment, 5)

    return sentiment

def get_readability(text: str) -> float:
    textstat.set_lang('pl')
    readability = textstat.gunning_fog(text)

    return readability

def reformat_topics(topics: list) -> str:
    topics_str = ' + '.join(f"(\"{word}\",{value})" for word, value in topics)

    return topics_str

def reformat_keywords(keywords: list) -> str:
    keywords_string = ', '.join(keywords)

    return keywords_string
  
def process(data: dict) -> dict:
    text = data.get('transcription')
    char_count = len(text)
    text_cleaned = clean_text(text)
    topics = get_topics(text_cleaned)
    keywords = get_keywords(topics)
    sentiment = get_sentiment(text)
    readability = get_readability(text)
    unique_keywords = get_unique_keywords(keywords)
    topics = reformat_topics(topics)
    keywords = reformat_keywords(keywords)

    new_row = {
        "id" : data.get("id"),
        "upload_time" : data.get("upload_time"),
        "title" : data.get("title"),
        "channel_name" : data.get("channel_name"),
        'text_clean': text_cleaned,
        'char_count': char_count,
        'unique_keywords': unique_keywords,
        'sentiment': sentiment,
        'readability': readability
    }

    return new_row
