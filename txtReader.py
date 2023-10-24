import pandas as pd

# read txt and store it as dataframe. Each row contains a paragraph's content and its word count. 
def txtreader(file):
    paragraphs=[]
    for line in file:
        newline=line.decode()
        paragraphs.append(newline)
    df = pd.DataFrame({'Paragraphs': paragraphs})
    df['Word Count'] = df['Paragraphs'].apply(lambda x: len(x.split()))
    df = df.drop(df[df['Word Count']==0].index)
    return df

#run function
#file='test.txt'
#txtreader(file)
