# 💸 FinWise - "Track. Predict. Save. Smarter."


**FinWise** is an intelligent personal finance tracker built with **Python** and **Streamlit**. It empowers users to upload their bank statements, automatically categorize transactions, visualize spending, forecast future expenses, and track their budget goals — all in a single, smart dashboard.

---

## 🚀 Features

* 📁 Upload CSV/Excel bank statements
* 🧹 Auto-clean and parse financial data
* 🧠 Categorize transactions using:

  * Rule-based logic
  * Machine Learning (custom trained model)
  * Hybrid (ML + fallback)
* 📊 Interactive visualizations:

  * Pie chart, line graph, bar chart
* 🔮 Expense forecasting using Facebook Prophet
* 💡 Smart suggestions to control overspending
* 💰 Budget goal tracker and top category alerts
* 📤 Optional report export (CSV + TXT summaries)

---

## 🛠️ Tech Stack

* **Frontend/UI**: [Streamlit](https://streamlit.io/)
* **ML & Forecasting**: `scikit-learn`, `Prophet`
* **Visualization**: `Plotly`, `Matplotlib`
* **Data Processing**: `Pandas`, `NumPy`

---

## 🧩 Project Structure

```
FinWise/
├── app.py                     # Main Streamlit app
├── helpers/
│   ├── categorizer.py         # ML & rule-based categorization functions
│   ├── predictor.py           # Prophet-based forecast
│   └── suggestions.py         # Smart tip generation
├── visuals/
│   └── charts.py              # All visualizations
├── sample_data/
│   ├── data.csv
|   |___sample_statement.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/ptirth2184/finwise.git
cd finwise
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the App**

```bash
streamlit run app.py
```

---

## 📸 Screenshots (optional)

*Add images of the dashboard, charts, or forecasting section here.*

---

## ✅ To-Do / Future Enhancements

* [ ] Add PDF export
* [ ] Deploy on Streamlit Cloud
* [ ] Allow category-level budgets
* [ ] Multi-user login with session storage

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Created by

**Tirth Patel**
Student | Data & AI Enthusiast <br>
📧 Reach me: \[[ptirth2184@gmail.com](mailto:your.email@example.com)]

---

## 💬 Feedback & Contributions

Feel free to fork, suggest changes, or contribute ideas via pull requests or issues!
