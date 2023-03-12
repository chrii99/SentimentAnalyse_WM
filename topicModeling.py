import re
import pandas as pd
from datetime import datetime
import numpy as np
from bertopic import BERTopic
import torch

import readData

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.dimensionality import BaseDimensionalityReduction

def setBERTopic() -> BERTopic:
    # Step 1 - Extract embeddings
    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") #multilingual version
    print("STEP 1")

    # Step 2 - Reduce dimensionality
    #umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
    # Fit BERTopic without actually performing any dimensionality reduction
    empty_dimensionality_model = BaseDimensionalityReduction()
    print("STEP 2")

    # Step 3 - Cluster reduced embeddings
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    print("STEP 3")

    # Step 4 - Tokenize topics
    #vectorizer_model = CountVectorizer(stop_words="english")
    vectorizer_model = CountVectorizer()
    print("STEP 4")

    # Step 5 - Create topic representation
    ctfidf_model = ClassTfidfTransformer()
    print("STEP 5")

    # Step 6 - (Optional) Fine-tune topic representations with 
    # a `bertopic.representation` model
    representation_model = KeyBERTInspired()
    print("STEP 6")

    # All steps together
    topic_model = BERTopic(
    embedding_model=embedding_model,          # Step 1 - Extract embeddings
    umap_model=empty_dimensionality_model,    # Step 2 - Reduce dimensionality
    hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
    vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
    ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
    representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
    )
    print("BERTopic set up!")
    return topic_model


# Filter
# https://colab.research.google.com/drive/1un8ooI-7ZNlRoK0maVkYhmNRl0XGK88f?usp=sharing#scrollTo=AQxSW8IMUpxj
def filter_tweets(data) -> pd.DataFrame:
    data.text = data.apply(lambda row: re.sub(r"http\S+", "", row.text).lower(), 1)
    data.text = data.apply(lambda row: " ".join(filter(lambda x:x[0]!="@", row.text.split())), 1)
    data.text = data.apply(lambda row: " ".join(re.sub("[^a-zäüößA-ZÖÄÜ]+", " ", row.text).split()), 1) #Umlaute und ß hinzufügen
    data = data.loc[(data.text != ""), :]

    return data

# Load data
data_pd = readData.getTweetsFromTo(datetime(2022, 11, 20), datetime(2022, 12, 18))
#data_pd = readData.getTweetsFromTo(datetime(2022, 11, 20), datetime(2022, 11, 21))

data_pd = filter_tweets(data_pd)

timestamps = data_pd.date.to_list()
tweets = data_pd.text.to_list()


#topic_model = BERTopic(language="multilingual" ,min_topic_size=300, verbose=True)
topic_model = setBERTopic()
topics, _ = topic_model.fit_transform(tweets)

freq = topic_model.get_topic_info() 
print(freq.head(10))

print(topic_model.get_topic(5))

fig = topic_model.visualize_topics() 

fig.write_html("path/graph_topic.html")

print("END")