# YouTube transcription topic modeling for Polish language (Airflow ETL)

Apache Airflow-based data processing workflow designed for daily ETL operations on text data.

The project consists of a Directed Acyclic Graph (DAG) that orchestrates the execution of four main tasks: 
- monitoring selected channel for uploads,
- downloading transcription of new content,
- processing transcription,
- loading extracted data into a BigQuery database.

The text processing is desinged to extract the following information:
- topics 
- sentiment
- readability

## DAG Overview

The DAG ensures that the tasks are executed in the correct order. This guarantees that the data is fetched, transformed, and loaded sequentially.

As the process is operates on a daily schedule, it is possible, that no new video was uploaded at that time. Be that the case, the first task returns none

![DAG](https://github.com/MichalMSlusarski/Transcription-LDA-with-Airflow/blob/main/DAG.png)

Upon successful completion of the "load_text_task," an email notification is sent using the send_email_func function, which includes the loaded data as part of the email message.

The project allows for customization, such as modifying the data retrieval, transformation, and loading functions to adapt to specific data sources and destination systems.

### Obtaining data

### Topic modeling

Upon receiving the downloaded transcription, the processing module begins rudimentary data cleanup. As we are working with a quite cumbersome language - Polish, a thorough lemmatization must be performed. For any modern text sourced from the internet, a pre-trained spaCy model -```pl_core_news_sm``` seems to be doing remarkably well.

The doc2bow method converts the list of tokens into a bag-of-words representation, which is a list of tuples where each tuple represents a word's ID and its frequency in the document. The resulting corpus is a list of such bag-of-words representations.

The LdaModel function trains an LDA model on the corpus. It takes the corpus, the number of topics to be extracted (num_topics), the dictionary mapping, and the number of passes as input parameters. The model learns the underlying topic distribution based on the given corpus.

```python
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
```

### Sentiment analysis

For sentiment analysis I used one of rare pre-trained sentiment analysis models, specifically designed for the Polish language. The appropriate function splits the text into individual sentences, applies the sentiment analysis model to each sentence, and collects the sentiment scores. It then calculates the average sentiment score by summing the scores of all sentences and dividing it by the total number of sentences. The resulting sentiment score is rounded to five decimal places and returned by the function.

### Readability index

The Gunning-Fog formula is used to calculate readability index. It's one of the very few methods easily and reliably applicable to the Polish language. The index provides a numerical value that represents the number of years of formal education required to understand the text. A higher index value indicates a more complex and difficult text, while a lower index value suggests a simpler and easier-to-understand text. I used the implementation from the ```textstat``` library.

## Credits

Apart from the large libraries, this project benefits from a very small package called SentimentPL: https://github.com/philvec/sentimentPL (~10★)
