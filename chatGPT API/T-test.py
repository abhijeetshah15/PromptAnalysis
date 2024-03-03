import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file into a DataFrame
data = pd.read_csv("PromptAnalysis-main/chatGPTAPI/tem02token120/rerun_1c.csv")


# Assuming your CSV file has columns named 'before' and 'after' for the two sets of responses
before_responses = data['before']
after_responses = data['after']

# Define a function to calculate cosine similarity between two strings
def calculate_cosine_similarity(str1, str2):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([str1, str2])
    similarity = cosine_similarity(vectors)
    return similarity[0, 1]

# Calculate cosine similarity for each corresponding pair of key-value pairs
similarities = [calculate_cosine_similarity(before, after) for before, after in zip(before_responses, after_responses)]

# Perform a paired T-test on the calculated cosine similarities
t_statistic, p_value = stats.ttest_1samp(similarities, 0)

# Print the results
print("Paired T-test Results:")
print("T-statistic:", t_statistic)
print("P-value:", p_value)

# Interpret the p-value
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference in responses.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference in responses.")
