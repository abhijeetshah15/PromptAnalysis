import pandas as pd
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump, load

# Read all CSV files in the current directory
csv_files = glob.glob('./*.csv')  

# Read and merge data
dataframes = [pd.read_csv(file) for file in csv_files]
combined_data = pd.concat(dataframes, ignore_index=True)
fdata = combined_data[combined_data['Solved/Unsolved'].isin(['Solved', 'Unsolved'])]

# Use TF-IDF to vectorize the 'Prompts' column
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(fdata['Prompts'])

# Encode 'Solved/Unsolved' as binary labels
y = fdata['Solved/Unsolved'].apply(lambda x: 1 if x == 'Solved' else 0)

# Directly use all data for training
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X, y)  # Note that we're directly using all of X and y for training, without splitting

# Save the model and vectorizer
dump(rf_classifier, 'RandomForestClassifier.joblib')
dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
