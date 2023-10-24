import pandas as pd
import pdfplumber

# read pdf and store it as dataframe. Each row contains a paragraph's content and its word count.
def pdfreader(file):
    pdf_text = None 
    paragraphs = []
    with pdfplumber.open(file) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            pdf_text  = page.extract_text()
            # read pdf line by line
            pdf_line = pdf_text.split('\n')
            s=''
            # If lines don't end with . ? !, merge lines into a paragraph.
            for j in pdf_line:
                if j[-1] not in ['.', '?', '!']:
                    s += j+' '
                else:
                    s += j
                    paragraphs.append(s)
                    s=''
        df = pd.DataFrame({'Paragraphs': paragraphs})
        df['Word Count'] = df['Paragraphs'].apply(lambda x: len(x.split()))
        return df
    
# run function:
#file='20221120_Diggs_BrandGuidelines_V1 (1).pdf'
#pdfreader(file)