# src/train_model.py
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def main():
    parser = argparse.ArgumentParser(description="Train baseline model on labeled window features")
    parser.add_argument("--data", default="outputs/dataset.csv", help="Path to dataset CSV")
    args = parser.parse_args()

    df = pd.read_csv(args.data)

    y = df["label"].astype(int)
    X = df.drop(columns=["label"])

    # Train/test split stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nReport:")
    print(classification_report(y_test, y_pred, digits=4))

if __name__ == "__main__":
    main()