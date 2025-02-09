from dotenv import load_dotenv
load_dotenv()  # load all environment variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini and provide sql query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([{'role': 'user', 'parts': [{'text': prompt}]}, {'role': 'user', 'parts': [{'text': question}]}])
    return response.text

# to get query from sql database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()  # Close connection after fetching all data
        return rows
    except sqlite3.Error as e:
        st.error(f"SQL Error: {e}")  # Display error in Streamlit
        return [] # Return empty list in case of error



prompt = """
You are an expert at converting english questions to SQL queries. The SQL database has two tables one is Employees with columns ID, Name, Department, Salary and Hire_Date. The other table has the name Departments with columns ID, Name, Manager.

For Example 
Example 1 - Show me all employees in the Engineering department, the SQL query will be like SELECT Name FROM Employees where Department = 'Engineering';. 
Example 2- Who is the manager of the Sales department? the SQL query will be like SELECT Manager FROM Departments where Name = "Sales";.
Example 3 - List all employees hired after '2020-01-01', the SQL query will be SELECT Name FROM Employees WHERE Hire_Date > '2020-01-01';. 
Example 4 - What is the total salary expense for the Marketing department? the SQL query will be SELECT Sum(Salary) From Employees WHERE Department = 'Marketing'; also the SQL code should not have ''' in the beginning or at the end.
"""

# Streamlit app
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    print("Gemini Response:", response)  # Print for debugging

    try:
        data = read_sql_query(response, "student.db")
        st.subheader("SQL Query:")
        st.code(response, language="sql") # Display the generated SQL query

        if data: # Check if data is not empty before displaying it
            st.subheader("Query Results:")
            for row in data:
                st.write(row) # Use st.write to display rows nicely
        else:
            st.info("No data returned from the query.")  # Inform user if no results.

    except Exception as e:
        st.error(f"An error occurred: {e}")  # Catch and display general errors