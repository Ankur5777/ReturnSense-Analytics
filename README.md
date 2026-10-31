Markdown
# ReturnPulse.ai — Retail Return Risk Intelligence & Prediction Platform

ReturnPulse.ai is an end-to-end full-stack data analytics and machine learning platform designed to proactively assess and mitigate product returns in fashion e-commerce. Built with a Django backend and powered by a trained Scikit-Learn / HistGradientBoostingClassifie pipeline, the platform performs real-time inference across 12 behavioral and operational dimensions, visualizes aggregate patterns through an interactive Tableau Public dashboard, and maintains a persistent audit log in SQLite.

"We benchmarked Logistic Regression against a tree-based gradient boosted ensemble. For the production pipeline, we leveraged Scikit-Learn’s HistGradientBoostingClassifier (inspired by LightGBM's histogram binning architecture) to achieve optimal ROC-AUC performance while maintaining zero external C++ dependency overhead for clean deployment."

---

## Key Features

- **Real-Time Return Risk Prediction:** Evaluates individual order attributes (price tier, delivery lag, customer tenure, bracketed sizing flags) and returns risk probabilities with clear status classifications.
- **Tableau Public BI Visualizations:** Embedded enterprise analytics dashboard illustrating transit lag impact, pricing tiers, customer age demographics, and high-risk manufacturer benchmarks across ~385k e-commerce records.
- **Audit Logging & History:** Logs every inference query to an SQLite database with timestamp, input variables, probability score, and risk level.
- **Administrative Control Panel:** Integrated Django Admin interface with multi-field search, filtering by risk status and region, and record auditing.
- **Secure Authentication & Guardrails:** Custom login/logout flows with `@login_required` route protection for operational analytics and predictor endpoints.
- **Modern Responsive UI:** Designed with a high-contrast dark "glassmorphism" aesthetic built on Bootstrap 5 and FontAwesome.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Django 5.x (Python) |
| **Machine Learning** | Scikit-Learn, LightGBM, Joblib, NumPy |
| **Data Processing** | Pandas |
| **Business Intelligence** | Tableau Public |
| **Database** | SQLite3 |
| **Frontend UI** | HTML5, CSS3 (Glassmorphism), Bootstrap 5, FontAwesome |

---

## Machine Learning Pipeline & Feature Engineering

The underlying model is trained on a fashion retail dataset of ~384,873 historical transactions. The feature transformation pipeline processes raw transactions through:

- **Delivery Transit Lag (`delivery_duration`):** Derived from `orderDate` and `deliveryDate` to quantify fulfillment speed impact on returns.
- **Bracketed Sizing Detection (`is_bracketed`):** Identifies shoppers purchasing multiple sizes of the identical item with intent to return poor-fitting variations.
- **Unsized Garment Flag (`is_unsized`):** Separates fitted garments from accessories or one-size items.
- **Customer Tenure & Demographics:** Standardized `customer_age` (derived from `dateOfBirth`) and `account_age_days`.
- **Pre-Processing Pipeline:** Column transformers handling categorical imputation, one-hot encoding for regional locations/salutations, and missing transit flags.

---

## Project Structure

```text
Retail_sales_prediction/
├── config/
│   ├── settings.py           # Core project configuration & authentication settings
│   ├── urls.py               # Root URL routing & custom 404 handler
│   └── wsgi.py               # WSGI server entry point
├── prediction/
│   ├── admin.py              # Model admin customizations
│   ├── models.py             # OrderPrediction schema definition
│   ├── urls.py               # Feature endpoints (dashboard, predict, history, login)
│   ├── views.py              # ML inference pipeline loader & route controllers
│   └── templates/
│       └── prediction/
│           ├── home.html         # Landing page
│           ├── login.html        # Authentication interface
│           ├── dashboard.html    # Analytics & Tableau embed container
│           ├── prediction.html   # Live inference web form
│           ├── history.html      # Prediction audit log
│           └── 404.html          # Custom error page
├── return_prediction_pipeline.joblib # Serialized Scikit-Learn/LightGBM pipeline
├── manage.py
├── requirements.txt
└── .gitignore

Getting Started
Prerequisites

Python 3.10+

pip package manager

1. Clone the Repository
Bash
git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd Retail_sales_prediction

2. Set Up a Virtual Environment
Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Run Migrations
Bash
python manage.py makemigrations
python manage.py migrate

5. Create Superuser (Admin Access)
Bash
python manage.py createsuperuser

6. Start Development Server
Bash
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/.

Application Routes
/ — Platform Landing Page

/login/ — User Authentication

/dashboard/ — Visual Analytics & Tableau Integration

/predict/ — Single-Order Live Risk Predictor

/history/ — Database Prediction Audit Log

/admin/ — Django Administrative Backend

License
This project is licensed under the MIT License — see the LICENSE file for details.