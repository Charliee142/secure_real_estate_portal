import pandas as pd
from sklearn.ensemble import IsolationForest
from .models import *

def detect_fraudulent_listings():
    # Load property data
    properties = Property.objects.all().values("id", "sale_price", "location", "category")
    df = pd.DataFrame(properties)

    if df.empty:  # Avoid errors if no data exists
        return Property.objects.none()

    # Train Isolation Forest Model
    clf = IsolationForest(contamination=0.05, random_state=42)
    
    # Ensure price column is numeric
    df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce").fillna(0)

    df["fraud_score"] = clf.fit_predict(df[["sale_price"]])  # Using price as fraud indicator

    # Flag suspicious listings
    fraudulent_listings = df[df["fraud_score"] == -1]["id"].tolist()
    return Property.objects.filter(id__in=fraudulent_listings)
