import json
import re
import pandas as pd

# Opening and Loading JSON File
JSON_FILE_NAME = "20230824_101836_issue_sharings"
with open(f"DevGPT/{JSON_FILE_NAME}.json") as file:
    data = json.load(file)

# Dictionary to store data extracted from JSON File
data_dict = {
    "ConversationNumber": [],
    "Prompts": [],
    "Answers": [],
    "Solved/Unsolved": [],
}

# Filtering out languages except English and Code
ascii_pattern = re.compile(r'[^\x00-\x7F]+')

# Looping through the data in JSON file
for i in range(len(data["Sources"])):
    
    # Getting the Issue State (Open or Closed)
    state = data['Sources'][i]["State"]
    
    # Check if the issue is Solved or Unsolved
    if state == "OPEN" or state == "CLOSED":
        try:
            # Flag to check if non-ASCII characters are found
            ascii_flag = True
            
            # Looping through the first conversation thread
            for j in range(len(data["Sources"][i]["ChatgptSharing"][0]["Conversations"])):

                prompt = data['Sources'][i]['ChatgptSharing'][0]['Conversations'][j]['Prompt']
                answer = data['Sources'][i]['ChatgptSharing'][0]['Conversations'][j]['Answer']

                # Use regex to check if any non-ASCII characters are present
                if ascii_pattern.search(prompt) or ascii_pattern.search(answer):
                    ascii_flag = False
                    break
                
                # Giving conversation numbers and Solved/Unsolved label and appending the data to dictionary
                if j == 0:
                    data_dict["ConversationNumber"].append(i + 1)
                    
                    if state == "OPEN":
                        data_dict["Solved/Unsolved"].append("Unsolved")
                    elif state == "CLOSED":
                        data_dict["Solved/Unsolved"].append("Solved")
                else:
                    data_dict["Solved/Unsolved"].append(" ")
                    data_dict["ConversationNumber"].append(" ")
                    
                data_dict["Prompts"].append(prompt)
                data_dict["Answers"].append(answer)

            # Add the data only if no non-ASCII characters are found in any column
            if ascii_flag:
                continue

        except Exception as e:
            print(f"Error processing data: {e}")
   
# Creating a dataframe from the dictionary
df = pd.DataFrame.from_dict(data_dict)

# Coverting the dataframe to CSV file
df.to_csv(f"Sampled Data/{JSON_FILE_NAME}.csv", index=False)