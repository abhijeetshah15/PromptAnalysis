import pandas as pd
import glob
from joblib import load
from sklearn.metrics import accuracy_score, classification_report

# Load Model and Vectorizer
model = load('ML/RandomForestClassifier.joblib')
tfidf_vectorizer = load('ML/tfidf_vectorizer.joblib')

# Read all CSV files in the current directory
csv_files = glob.glob('./Test Data/*.csv')
all_data = pd.DataFrame()
for csv_file in csv_files:
    data = pd.read_csv(csv_file)
    all_data = pd.concat([all_data, data], ignore_index=True)

fdata = all_data[all_data['Solved/Unsolved'].isin(['Solved', 'Unsolved'])]
fdata.loc[:, 'Prompts'] = fdata['Prompts'].fillna('')

# TF-IDF Vectorizer
X = tfidf_vectorizer.transform(fdata['Prompts'])
y_true = fdata['Solved/Unsolved'].apply(lambda x: 1 if x == 'Solved' else 0)

# Evaluation model
y_pred = model.predict(X)

# Create a DataFrame with original prompts, original 'Solved/Unsolved', and predicted 'Solved/Unsolved'
results_df = pd.DataFrame({
    'Prompts': fdata['Prompts'],
    'Original_Solved/Unsolved': fdata['Solved/Unsolved'],
    'Predicted_Solved/Unsolved': ['Solved' if pred == 1 else 'Unsolved' for pred in y_pred]
})

# Save the DataFrame to a CSV file
results_df.to_csv('ML Model Results/predicted_results.csv', index=False)

# Print results
print("Evaluating combined predictions")
accuracy = accuracy_score(y_true, y_pred)
print(f"Combined Accuracy: {accuracy}")
print(classification_report(y_true, y_pred))
