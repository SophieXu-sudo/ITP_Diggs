# import all packages we need

import pandas as pd
import openai
#import os
import string
from openai.embeddings_utils import get_embedding, cosine_similarity

# Object chatbot

class Chatbot():
    def __init__(self):
        self.chat_history = []
    
    #this function should go through our database and find top 3 sentences relative to our question. 
    #now, we use a pandas dataframe instead. 
    def get_sentence(self,query:string,df:pd.DataFrame,n:int):
        query_embedding = get_embedding(query,engine="text-embedding-ada-002")
        df["similarity"] = df.Embeddings.apply(lambda x: cosine_similarity(x, query_embedding))
        results = df.sort_values("similarity", ascending=False, ignore_index=True)
        results = results.head(n)
        return results
    
    def chat_prompt(self,user_input:string):
        self.chat_history.append(user_input)
        messages = [{"role": "system", "content": "You are a smart chatbot."}]
        for i in range(len(self.chat_history)):
            if i%2 == 0:
                messages.append({"role": "user", "content": self.chat_history[i]})
            else:
                messages.append({"role": "assistant", "content": self.chat_history[i]})
        print("Done create chat message: ")
        #print(messages)
        return (messages)

    #this function should generate a prompt that tells the AI model what it is and what it needs to do.
    def create_prompt(self, result:pd.DataFrame, user_input:string):
        # add last answer from chatbot into the question
        if len(self.chat_history) > 1:
            question = self.chat_history[-1] + user_input
        else:
            question = user_input
        result = self.get_sentence(question,result,3)
        print(result)

        # specify chat schema
        top_sim = result.iloc[0]['similarity']
        if top_sim < 0.8:
            return self.chat_prompt(user_input)

        system_role = """who is a smart chatbot and whose expertise is summarizing answer from given text. You are given a query, 
        a series of text embeddings in order of their cosine similarity to the query. 
        You must take the given embeddings and return a brief summary of the answer in the language of the query: 
        
        Here is the question: """+ question + """
            
        and here are the embeddings: 
            
            1.""" + str(result.iloc[0]['Paragraphs']) + """
            2.""" + str(result.iloc[1]['Paragraphs']) + """
            3.""" + str(result.iloc[2]['Paragraphs']) + """
        """

        user_content = f"""Given the question: "{str(question)}". Return a brief answer based on the document:"""
        # store chat history
        self.chat_history.append(user_content)
        # final prompt
        messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_content},]
        #messages = [{"role": "system", "content": system_role}]
        #for i in range(len(self.chat_history)):
            #if i%2 == 0:
                #messages.append({"role": "user", "content": self.chat_history[i]})
            #else:
                #messages.append({"role": "assistant", "content": self.chat_history[i]})

        print('Done creating prompt')
        return messages

    #this function should generate our final answer using GPT3.5 model
    def gpt(self, messages:list):
        print('Sending request to GPT-3.5')
        #openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = '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'
        r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0.4, max_tokens=1500)
        answer = r.choices[0]["message"]["content"]
        self.chat_history.append(answer)
        print('Done sending request to GPT-3.5')
        response = {'answer': answer}
        #response = {'answer': answer,'sources': sources}
        print(self.chat_history)
        return response
    
#codes for debugging
