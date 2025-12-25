import sqlite3
import pandas as pd
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL')
groq_client = Groq()

db_path = Path(__file__).parent / "db.sqlite"

prompt = f'''Your are a sql expert in understanding the database schemas and generating sql queries for a natural language questions.
table name: product
table contains data related to shoes
The schema is provided in schema tags.
<schema>
product_link - string(hyperlink to product)
title - string (name of the product)
brand - string (brand of product)
price - integer (price of product in indian rs)
discount - float (discount on product 10% discount represented as 0.1, 30% discount represented as 0.3)
avg_rating - float (rating of product. Maximum rating is 5 and lowest is 1)
total_ratings - integer (total number of rating product has)

</schema>

whenever you will search for brand name, remember the brand name in database can be case sensitive.Make sure to use
%LIKE% to search for brand name.
create a single query for the question provided. return only query nothing extra.Note :Always provide all fields use (select *) and return the query between <sq></sql> this sql tag


'''

def generate_sql_query(question):

    # calling llm
    completion = groq_client.chat.completions.create(  # type: ignore
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2,
        max_completion_tokens=1024,
        top_p=0.9,
        stream=False,
    )
    return completion.choices[0].message.content


def run_query(sql_query):
    if sql_query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(db_path) as conn:
            df  = pd.read_sql_query(sql_query,conn)
            return df


def sql_chain(question):
    sql_query = generate_sql_query(question)
    pattern = r"<sql>(.*?)</sql>"
    matches = re.findall(pattern,sql_query,re.DOTALL)
    print(matches[0].strip())
    if len(matches) == 0:
        return "Sorry, LLM is not able to generate query for your question"
    response = run_query(matches[0].strip())
    if response is None:
        return "Sorry, there is a problem executing the query"

    context = response.to_dict(orient='records')

    MAX_ROWS = 10

    if len(context) > MAX_ROWS:
        return (
            f"Too many shoes found ({len(context)} results). "
            "Please be more specific or ask for top results."
        )

    answer = data_comprehension(question,context)
    return answer


comprehension_prompt = '''You are an expert in understanding the context of the question and reply based on data provided.
You will be provided with QUESTION: and DATA:. The data will be in the form of an array or a dataframe or dict.
Reply based on only the data provided.Just give a plain simple natural language response.For example if the question is 
"what is the average rating?" and data is "4.3, then answer should be "The average rating for the product is 4.3". so make sure the response is curated with
question and data.There can also be cases where you are given entire dataframe int the Data: field. Always remember that the 
data field contains the answer of the question asked.Always reply in the following format.
Product title, price in indian rupees, discount,and rating, and then product link. Take care that all the in List format,
one line after the other , Not as a paragraph.
STRICT RULES:
- Every product MUST be included
- Every line MUST contain product_link
- If product_link is missing in DATA, say "Link not available"
- DO NOT summarize
- DO NOT skip rows
- DO NOT merge products
- NEVER wrap links inside < >
- Always print the URL as plain text
- Output MUST follow the exact format shown in the example
example:
1.Nike women Running shoes: Rs. 4500 (35 percent off), Rating: 4.4 <link>
2.Nike women Running shoes: Rs. 4500 (35 percent off), Rating: 4.4 <link>   
3.Nike women Running shoes: Rs. 4500 (35 percent off), Rating: 4.4 <link>

'''
def data_comprehension(question,context):

    # calling llm
    completion = groq_client.chat.completions.create(  # type: ignore
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt
            },
            {
                "role": "user",
                "content": f"QUESTION: {question} DATA: {context}"
            }
        ],
        temperature=0.2,
        # max_completion_tokens=1024,
        top_p=0.9,
        stream=False,
    )
    return completion.choices[0].message.content



if __name__ == "__main__":
    # query = "select * from product where brand like '%nike%'"
    # df = run_query(query)
    question = "Give me puma shoes with rating higher than 4.5 and more than 30% discount"
    # query = generate_sql_query(question)
    # print(query)
    answer = sql_chain(question)
    print(answer)


