import os
import joblib

# === Load ML Model & Vectorizer ===
model_path = os.path.join("helpers", "categorizer_model.pkl")
vectorizer_path = os.path.join("helpers", "vectorizer.pkl")

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except:
    model = None
    vectorizer = None

# === 1. Rule-Based Categorization ===
def rule_based_categorize(description: str) -> str:
    desc = description.lower()

    if any(keyword in desc for keyword in ['zomato', 'swiggy', 'restaurant', 'cafe']):
        return 'Food'
    elif any(keyword in desc for keyword in ['netflix', 'prime', 'spotify', 'hotstar']):
        return 'Entertainment'
    elif any(keyword in desc for keyword in ['grocery', 'mart', 'store']):
        return 'Groceries'
    elif any(keyword in desc for keyword in ['uber', 'ola', 'fuel', 'petrol', 'diesel']):
        return 'Transport'
    elif any(keyword in desc for keyword in ['electricity', 'water', 'gas', 'bill', 'recharge']):
        return 'Utilities'
    elif any(keyword in desc for keyword in ['salary', 'credited', 'income', 'bonus', 'lottery']):
        return 'Income'
    elif any(keyword in desc for keyword in ['amazon', 'flipkart', 'myntra', 'zudio', 'ajio']):
        return 'Shopping'
    else:
        return 'Others'

# === 2. ML-Based Categorization ===
def ml_categorize(description: str) -> str:
    if model and vectorizer:
        X = vectorizer.transform([description])
        return model.predict(X)[0]
    else:
        return "Others"  # or raise error

# === 3. Hybrid (ML + Rule-Based Fallback) ===
def hybrid_categorize(description: str) -> str:
    try:
        return ml_categorize(description)
    except:
        return rule_based_categorize(description)
