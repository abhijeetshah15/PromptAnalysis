import pandas as pd
from openai import OpenAI

# 1) Load data from CSV file
df = pd.read_csv('YOUR INPUT FILE PATH')

# Filter the first 10 rows containing only numbers in 'ConversationNumber'
df_filtered = df[pd.to_numeric(df['ConversationNumber'], errors='coerce').notnull()]

# 2) Initialize OpenAI client
OPENAI_API_KEY = "YOUR API KEY"
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize a list to collect new answers
new_answers = []

# Process each row in the filtered DataFrame
for index, row in df_filtered.iterrows():
    messages = [{"role": "user", "content": row['Prompts']}]

    # Receive answers from OpenAI, using stream
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=120,
        n=1,
        messages=messages,
        stream=True,
    )
    
    # Accumulate answer content from the stream
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer = chunk.choices[0].delta.content
            full_response += answer
    
    # Add the collected answer to the list
    new_answers.append(full_response.strip())

# Add new answers to the DataFrame in a column now named 'after'
df_filtered['after'] = new_answers

# Rename 'Answers' column to 'before'
df_filtered.rename(columns={'Answers': 'before'}, inplace=True)

# Delete 'Solved/Unsolved' column
df_filtered.drop(columns=['Solved/Unsolved'], inplace=True)

# Delete 'ConversationNumber' and 'Prompts' columns
df_filtered.drop(columns=['ConversationNumber', 'Prompts'], inplace=True)

# 3) Save the modified DataFrame to a new CSV file
df_filtered.to_csv('YOUR OUTPUT FILE PATH', index=False)
