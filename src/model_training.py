# src/model_training.py

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/lifestyle_dataset.csv")

# -------------------------
# SPLIT FEATURES & TARGET
# -------------------------
X = df.drop("risk_level", axis=1)
y = df["risk_level"]

# -------------------------
# COLUMN TYPES
# -------------------------
categorical_cols = X.select_dtypes(include=["object"]).columns
numerical_cols = X.select_dtypes(exclude=["object"]).columns

# -------------------------
# PREPROCESSING
# -------------------------
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])

# -------------------------
# TRAIN-TEST SPLIT
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# MODELS
# -------------------------
lr_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])

dt_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", DecisionTreeClassifier())
])

# -------------------------
# TRAIN
# -------------------------
lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

# -------------------------
# EVALUATE
# -------------------------
lr_acc = accuracy_score(y_test, lr_model.predict(X_test))
dt_acc = accuracy_score(y_test, dt_model.predict(X_test))

print("Logistic Regression Accuracy:", lr_acc)
print("Decision Tree Accuracy:", dt_acc)

# -------------------------
# SELECT BEST
# -------------------------
if lr_acc > dt_acc:
    best_model = lr_model
    print("✅ Logistic Regression Selected")
else:
    best_model = dt_model
    print("✅ Decision Tree Selected")

# -------------------------
# SAVE MODEL
# -------------------------
joblib.dump(best_model, "models/model.pkl")

print("🔥 Model saved to models/model.pkl")