#!/usr/bin/env python

import os
import sys
import sqlite3
import pandas as pd
import absl.logging
import google.generativeai as genai

# Suppress logs
absl.logging.set_verbosity(absl.logging.ERROR)
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

# Load Excel file and process dataframe
dataframe = pd.read_excel('/Users/gayatrikrishnakumar/Documents/Interdepartmental EL/python/scores.xlsx', index_col=0)
dataframe.rename(columns={"Total-Test": "total"}, inplace=True)

# (Optional) Clean the data by replacing NaN values with 0
dataframe.fillna(0, inplace=True)

# Create SQLite database (or connect if it already exists)
connection = sqlite3.connect('mydatabase.db')
dataframe.to_sql('mytable', connection, if_exists='replace')

# Configure Google Generative AI (Gemini)
# Replace "YOUR_API_KEY" with your actual API key.
genai.configure(api_key="")

# Define an SQL query tool
def sql_query(query: str):
    """Run a SQL SELECT query on the SQLite database and return the results."""
    return pd.read_sql_query(query, connection).to_dict(orient='records')

# Define system prompt with database schema
system_prompt = """
You are an expert SQL analyst. Generate SQL queries based on the user question and the database schema.
Use the 'sql_query' function to execute queries and return the results.

database_schema: [
    {
        table: 'mytable',
        columns: [
            { name: 'Name', type: 'string' },
            { name: 'USN', type: 'string' },
            { name: 'Email', type: 'string' },
            { name: 'T1a', type: 'int' },
            { name: 'T1b', type: 'int' },
            { name: 'T2', type: 'int' },
            { name: 'T3a', type: 'int' },
            { name: 'T3b', type: 'int' },
            { name: 'T4a', type: 'int' },
            { name: 'T4b', type: 'int' },
            { name: 'T5a', type: 'int' },
            { name: 'T5b', type: 'int' },
            { name: 'total', type: 'int' }
        ]
    }
]
""".strip()

# Create Gemini model with the SQL tool
sql_gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[sql_query],
    system_instruction=system_prompt
)

# Start chat with function calling enabled
chat = sql_gemini.start_chat(enable_automatic_function_calling=True)

def run_query(user_query: str):
    response = chat.send_message(user_query)
    return response.text

if __name__ == "__main__":
    # Always read the query from standard input.
    if sys.stdin.isatty():
        # If no piped input is available, prompt interactively.
        query = input("Enter your query: ")
    else:
        query = sys.stdin.read().strip()

    result = run_query(query)
    print(result)
