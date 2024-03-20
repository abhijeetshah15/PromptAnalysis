import pandas as pd
from scipy import stats
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the CSV file into a DataFrame
data = pd.read_csv("PromptAnalysis-main/chatGPTAPI/tem0token1024/run_1.csv")

# Appending the data into categories "before" and "after"
before_responses = data['before']
after_responses = data['after']

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Calculate sentiment scores for corresponding key-value pairs
before_sentiment_scores = []
after_sentiment_scores = []

for before, after in zip(before_responses, after_responses):
    before_sentiment = sia.polarity_scores(before)['compound']
    after_sentiment = sia.polarity_scores(after)['compound']
    before_sentiment_scores.append(before_sentiment)
    after_sentiment_scores.append(after_sentiment)

# Perform a paired T-test on the sentiment scores
t_statistic, p_value = stats.ttest_rel(before_sentiment_scores, after_sentiment_scores)

# Print the results
print("Paired T-test Results for Sentiment Analysis of Key-Value Pairs:")
print("T-statistic:", t_statistic)
print("P-value:", p_value)

# Interpreting the p-value
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference in sentiment between before and after responses.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference in sentiment between before and after responses.")
