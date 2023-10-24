import streamlit as st
import openai
from openai.embeddings_utils import get_embedding

# this function is used to generate embedding
@st.cache_data
def embeddings(df):
    print('Calculating embeddings')
    #openai.api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = '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'
    # use openai's emmbedding, model is ada
    embedding_model = "text-embedding-ada-002"
    # add embedding result as a column to dataframe
    embeddings = df.Paragraphs.apply([lambda x: get_embedding(x, engine=embedding_model)])
    df["Embeddings"] = embeddings
    print('Done calculating embeddings')
    # drop paragraphs that word count <= 10, reduce the effect of title
    df = df.drop(df[df['Word Count']<=10].index)
    return df
