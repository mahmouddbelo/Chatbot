# Health Insurance Data Analysis Chatbot
This repository contains an AI-powered chatbot that automates the analysis of health insurance data by generating and executing Python code from natural language queries. Using Gradio for a user-friendly interface, this chatbot allows users to ask questions about the dataset and returns real-time results using pandas for data analysis.

## Features

Natural Language Processing: Ask questions in plain language, and the chatbot will automatically generate and execute Python code to answer.

Data Analysis: The chatbot can analyze health insurance data, providing insights such as service usage, policy information, and more.

Real-time Execution: The generated Python code is executed in real-time, returning immediate results or error messages for troubleshooting.

Gradio Web Interface: Easy-to-use, web-based interface powered by Gradio, making it accessible for non-technical users.

Error Handling: Built-in error handling for syntax and runtime issues.

### Project Structure
chatbot.py: Core logic for generating and executing Python code from user queries.
data_description.txt: Description of the dataset fields used by the chatbot for code generation.
dtat.xlsx: Example dataset used for testing the chatbot's functionality.
interface.py: Gradio-based interface that takes user input and returns results.
Dataset Description

## The chatbot works on a dataset containing the following columns:

total
policy_id
program_id
Type_Name_En
the_type
the_date
Service_Class_Name_En
provider_name
provider_category
member_id
member_name
Service_Name_Ar
Service_name_En
Client Name

![image 1](https://github.com/M-craspo/Chatbot/blob/main/5972066362421527011.jpg)
