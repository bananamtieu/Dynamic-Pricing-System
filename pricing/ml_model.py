import os
import joblib  # Import joblib for saving/loading models
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from scipy.optimize import minimize
from pricing.models import SalesData, DemandIndicator, CompetitorPricing

# File paths for saved models
MODEL_PATH = "pricing/trained_model.pkl"

def load_data():
    """Fetches data from the database and prepares it for training."""
    
    # ✅ Fetch Data
    sales = list(SalesData.objects.values("product_id", "date", "units_sold", "price"))
    demand = list(DemandIndicator.objects.values("product_id", "date", "views", "add_to_cart", "conversion_rate"))
    competitor = list(CompetitorPricing.objects.values("product_id", "date", "competitor_price"))

    # ✅ Convert to DataFrames
    df_sales = pd.DataFrame(sales)
    df_demand = pd.DataFrame(demand)
    df_competitor = pd.DataFrame(competitor)

    # ✅ Merge datasets on `product_id` and `date`
    df = df_sales.merge(df_demand, on=["product_id", "date"], how="left")
    df = df.merge(df_competitor, on=["product_id", "date"], how="left")

    # ✅ Convert `date` column to proper datetime format
    df["date"] = pd.to_datetime(df["date"])

    # ✅ Sort by product and date before shifting (VERY IMPORTANT)
    df = df.sort_values(by=["product_id", "date"])

    # ✅ Fill missing competitor prices per product
    df["competitor_price"] = df.groupby("product_id")["competitor_price"].transform(lambda x: x.fillna(x.mean()))
    df["competitor_price"] = df["competitor_price"].fillna(df["price"])  # Use product price if no competitor price available

    # ✅ Shift `price` to get `price_tomorrow` (WITHIN each product!)
    df["price_tomorrow"] = df.groupby("product_id")["price"].shift(-1)

    return df

def trend_difference_loss(coeffs, X, y, prev_price, lambda_factor=0.5):
    """
    Custom loss function that minimizes both MAE and trend direction error.
    """
    predictions = X @ coeffs  # Compute y_pred

    # Compute actual & predicted trends
    actual_trend = y - prev_price
    predicted_trend = predictions - prev_price

    # Penalize incorrect trend predictions
    trend_penalty = np.abs(actual_trend - predicted_trend)

    # Compute final loss
    mae_loss = np.abs(y - predictions)  # Standard MAE
    return np.mean(mae_loss + lambda_factor * trend_penalty)

# ✅ Train Pricing Model with Trend Difference Loss
def train_pricing_model(force_retrain=False):
    """Trains a Linear Regression model using trend difference loss for multiple products."""
    if not force_retrain and os.path.exists(MODEL_PATH):
        print("\n✅ Loading saved model...")
        model = joblib.load(MODEL_PATH)
        return model

    print("\n🚀 Training new model...")

    df = load_data()  # ✅ Load updated dataset with multiple products
    df = df.dropna()

    # ✅ Convert date to ordinal for potential time-based features
    df["date"] = pd.to_datetime(df["date"])
    df["date_ordinal"] = df["date"].map(lambda d: d.toordinal())  # Convert to ordinal

    # ✅ Sort by product_id & date before shifting (VERY IMPORTANT)
    df = df.sort_values(by=["product_id", "date"])

    # ✅ Extract Features (EXCLUDE "date" column)
    X = df[["price", "units_sold", "views", "add_to_cart", "conversion_rate", "competitor_price"]].values
    y = df["price_tomorrow"].values

    # ✅ Compute prev_price (MUST BE PER PRODUCT!)
    df["prev_price"] = df.groupby("product_id")["price"].shift(1).fillna(df["price"])
    prev_price = df["prev_price"].values

    print(f"\n🚀 Total Data Points After Shift: {len(df)}")

    # ✅ Train-Test Split (Ensure it is RANDOM but per product)
    X_train, X_test, y_train, y_test, prev_price_train, prev_price_test = train_test_split(
        X, y, prev_price, test_size=0.2, random_state=42
    )

    # ✅ Initialize Coefficients
    initial_coeffs = np.zeros(X_train.shape[1])

    # ✅ Optimize Model using Trend Difference Loss
    result = minimize(
        trend_difference_loss, initial_coeffs,
        args=(X_train, y_train, prev_price_train),
        method="BFGS"
    )

    optimized_coeffs = result.x
    print("\n✅ Optimized Coefficients:", optimized_coeffs)

    # ✅ Model Evaluation
    y_pred = np.dot(X_test, optimized_coeffs)

    # ✅ Calculate Metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("\n📊 Model Performance:")
    print(f"🔹 R² Score: {r2:.4f}")
    print(f"🔹 Mean Absolute Error (MAE): ${mae:.2f}")

    # ✅ Save trained model
    joblib.dump(optimized_coeffs, MODEL_PATH)
    print("\n✅ Model saved!")

    return optimized_coeffs

def suggest_price(product_id):
    """Suggests the optimal price for a product using the trained model."""
    
    # ✅ Load saved model
    if os.path.exists(MODEL_PATH):
        coeffs = joblib.load(MODEL_PATH)
        print("\n✅ Using saved model for prediction...")
    else:
        print("\n⚠️ Model not found! Retraining...")
        coeffs = train_pricing_model()

    df = load_data()  # ✅ Data includes multiple products now!

    # ✅ Convert date column to datetime for proper sorting
    df["date"] = pd.to_datetime(df["date"])

    # ✅ Get the most recent row for this product
    product_df = df[df["product_id"] == product_id].sort_values("date")

    if product_df.empty:
        return "⚠️ Error: No data found for this product"

    product_data = product_df.iloc[-1]  # ✅ Most recent day

    print("\n🚀 Features for Prediction:")
    print(product_data[["price", "units_sold", "views", "add_to_cart", "conversion_rate", "competitor_price"]])

    # ✅ Prepare input features (match training format)
    X_new = np.array([[
        product_data["price"], 
        product_data["units_sold"], 
        product_data["views"], 
        product_data["add_to_cart"], 
        product_data["conversion_rate"], 
        product_data["competitor_price"]
    ]])

    # ✅ Predict tomorrow’s price
    predicted_price = np.dot(X_new, coeffs)
    predicted_price = float(predicted_price)  # Convert NumPy array to scalar

    # ✅ Apply product constraints
    from pricing.models import Product
    product = Product.objects.get(id=product_id)
    final_price = max(min(predicted_price, product.max_price), product.min_price)

    print(f"\n🚀 Predicted Price for Tomorrow: {final_price}")
    return round(final_price, 2)
