import pandas as pd
import glob
from joblib import load
from sklearn.metrics import accuracy_score, classification_report

# Load Model and Vectorizer
model = load('RandomForestClassifier.joblib')
tfidf_vectorizer = load('tfidf_vectorizer.joblib')

# Read all CSV files in the current directory
csv_files = glob.glob('./*.csv')
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

# Print results
print("Evaluating combined predictions")
accuracy = accuracy_score(y_true, y_pred)
print(f"Combined Accuracy: {accuracy}")
print(classification_report(y_true, y_pred))
