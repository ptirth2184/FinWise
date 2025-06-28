
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load data
df = pd.read_csv("/workspaces/FinWise/data/data.csv")

# Features and labels
X = df['Description']
y = df['Category']

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english')
X_vect = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vect, y)

# Save model and vectorizer
joblib.dump(model, 'categorizer_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
