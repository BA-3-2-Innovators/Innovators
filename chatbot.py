import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("finaldepressiondataset1.csv")

# Drop irrelevant columns
drop_cols = ['Name', 'City', 'Profession']
df.drop(columns=drop_cols, inplace=True)

# Fill missing numeric values with median
for col in df.select_dtypes(include=['float64','int64']).columns:
    df[col].fillna(df[col].median(), inplace=True)
# Fill missing categorical values with mode
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Encode categorical columns using LabelEncoder and save encoders
categorical_columns = ['Gender', 'Working Professional or Student', 'Dietary Habits', 'Degree',
                       'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness']
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    # Save each encoder
    filename = f"le_{col.lower().replace(' ', '_').replace('?', '')}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(le, f)

# Define feature columns (exclude target 'Depression')
target_col = 'Depression'
feature_columns = [col for col in df.columns if col != target_col]

# Scale numeric features and save scaler
scaler = StandardScaler()
X = df[feature_columns]
y = df[target_col]

# Split data to train and test (if needed)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Fit scaler on training data and transform both training and test
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# Train Random Forest model and save
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

with open("rf_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

# Save label encoder for target variable as well, if exists
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
with open("le_target.pkl", "wb") as f:
    pickle.dump(le_target, f)

print("Pickle files created: label encoders, scaler, model.")
