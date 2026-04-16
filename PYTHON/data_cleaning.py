import pandas as pd

print("Loading dataset...")
df = pd.read_csv('data/online_retail.csv', encoding='ISO-8859-1')

print("\n--- Initial Data ---")
print(df.head())

print("\nShape:", df.shape)

print("\nInfo:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna(subset=['CustomerID'])

df = df[df['Quantity'] > 0]

df = df[df['UnitPrice'] > 0]

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)

df = df.drop_duplicates()

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

print("\n--- Cleaned Data ---")
print(df.head())

print("\nNew Shape:", df.shape)

print("\nSummary Stats:")
print(df.describe())

df.to_csv('data/cleaned_data.csv', index=False)

print("\n✅ Data cleaning completed and saved as 'cleaned_data.csv'")
