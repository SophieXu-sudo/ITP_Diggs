import docx
import pandas as pd

# read docx and store it as dataframe. Each row contains a paragraph's content and its word count. 
def docxreader(file):
    doc = docx.Document(file)
    paragraphs = []
    for para in doc.paragraphs:
        if len(para.text)>0:
            paragraphs.append(para.text)
    df = pd.DataFrame({'Paragraphs': paragraphs})
    df['Word Count'] = df['Paragraphs'].apply(lambda x: len(x.split()))
    return df

#run function
#file = 'Diggs Info Repository Products Example.docx'
#docxreader(file)