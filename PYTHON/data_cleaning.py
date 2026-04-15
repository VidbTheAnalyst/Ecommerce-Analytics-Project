import pandas as pd

# ==============================
# 1. LOAD DATA
# ==============================
print("Loading dataset...")
df = pd.read_csv('data/online_retail.csv', encoding='ISO-8859-1')

# ==============================
# 2. INITIAL EXPLORATION
# ==============================
print("\n--- Initial Data ---")
print(df.head())

print("\nShape:", df.shape)

print("\nInfo:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# ==============================
# 3. DATA CLEANING
# ==============================

# Remove rows with missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Remove negative or zero Quantity (returns)
df = df[df['Quantity'] > 0]

# Remove zero or negative prices
df = df[df['UnitPrice'] > 0]

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)

# Remove duplicates
df = df.drop_duplicates()

# ==============================
# 4. FEATURE ENGINEERING
# ==============================

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# ==============================
# 5. FINAL CHECK
# ==============================
print("\n--- Cleaned Data ---")
print(df.head())

print("\nNew Shape:", df.shape)

print("\nSummary Stats:")
print(df.describe())

# ==============================
# 6. SAVE CLEANED DATA
# ==============================
df.to_csv('data/cleaned_data.csv', index=False)

print("\n✅ Data cleaning completed and saved as 'cleaned_data.csv'")