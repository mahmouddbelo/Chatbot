import gradio as gr
import pandas as pd
import os
import io
import sys
import re
import traceback
from groq import Groq

def generate_formula_from_query(query, data_description, samples):
    prompt = f"""
    You are an advanced data analysis assistant. You are given a dataset with the following columns: {data_description}.
    and samples of my data I will provide you 20 samples of my data: {samples}.
    A user asks you: "{query}"
    Provide the correct Python code only without any text to answer the user's question using pandas on the dataset.
    The code should assume that the DataFrame is named 'df'.
    Return only executable Python code without any explanations, comments, or markdown formatting.
    Do not include any import statements or function definitions.
    Ensure the code is syntactically correct and produces a result that can be displayed.
    """
   
    api_key = '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'
    client = Groq(api_key=os.environ.get("api_key", api_key))

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

# Load the dataset
df = pd.read_excel('/Users/mahmoudahmed/Desktop/chatpot/chatbot/dtat.xlsx')


# Get 20 random samples from the DataFrame
samples = df.sample(n=20, random_state=1).to_dict(orient='records')

data_description = """
total, policy_id, program_id, Type_Name_En, the_type, the_date, Service_Class_Name_En,
provider_name, provider_category, member_id, member_name, Service_Name_Ar,
Service_name_En, Client Name
"""

def clean_code(code):
    # Remove any import statements or function definitions
    code = re.sub(r'^(import|from|def).*$', '', code, flags=re.MULTILINE)
    # Remove markdown code blocks
    code = re.sub(r'```.*?\n|```', '', code, flags=re.DOTALL)
    # Remove any leading/trailing whitespace
    code = code.strip()
    return code

def preprocess_code(code):
    # Clean the code first
    code = clean_code(code)
    # Wrap the code in a try-except block to catch potential runtime errors
    return f"""
try:
    result = {code}
    print(result)
except Exception as e:
    print(f"Runtime Error: {{str(e)}}")
"""

def execute_code(code):
    # Preprocess the code
    code = preprocess_code(code)
    
    # Create a string buffer to capture the output
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        # First, try to compile the code to catch syntax errors
        compile(code, '<string>', 'exec')
        
        # If compilation succeeds, execute the code
        exec(code, {'df': df, 'pd': pd})
        
        # Get the captured output
        output = buffer.getvalue().strip()
        
        if not output:
            output = "The operation was successful, but didn't produce any output to display."
        else:
            # Convert the output to an HTML table if it's a DataFrame or Series
            if isinstance(output, pd.DataFrame) or isinstance(output, pd.Series):
                output = output.to_html(classes='table table-striped')
            else:
                output = f"<pre>{output}</pre>"
                
    except SyntaxError as e:
        output = f"<pre>Syntax Error: {str(e)}\n{traceback.format_exc()}</pre>"
    except Exception as e:
        output = f"<pre>Error executing code: {str(e)}\n{traceback.format_exc()}</pre>"
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__

    return output

def process(user_query):
    # Generate the Python code using the query and data description
    formula_code = generate_formula_from_query(user_query, data_description, samples)

    # Clean the generated code
    cleaned_code = clean_code(formula_code)

    # Execute the generated code and get the result
    result = execute_code(cleaned_code)

    return result

# Gradio interface
def chatbot_interface(user_query):
    response = process(user_query)
    return response

# Launch the Gradio app
import gradio as gr

# Launch the Gradio app
iface = gr.Interface(
    fn=process,  # Function to process user input
    inputs=gr.Textbox(label="Ask a question"),  # Textbox for user input
    outputs=gr.Textbox(),  # Textbox for displaying output
    title="Health Insurance AI",  # Title of the app
    description="Ask a question about the dataset, and the AI will generate Python code and execute it to give you the result."
)

# Launch the app with a public link
iface.launch(share=True)



