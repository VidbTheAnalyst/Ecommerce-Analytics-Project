import pandas as pd

# ==============================
# 1. LOAD CLEANED DATA
# ==============================
print("Loading cleaned data...")
df = pd.read_csv('data/cleaned_data.csv')

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ==============================
# 2. CREATE REFERENCE DATE
# ==============================
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# ==============================
# 3. CALCULATE RFM METRICS
# ==============================

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
})

# Rename columns
rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
}, inplace=True)

print("\nRFM Table:")
print(rfm.head())

# ==============================
# 4. RFM SCORING (1–4)
# ==============================

rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

# ✅ Convert scores to integer (IMPORTANT FIX)
rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

# ==============================
# 5. CREATE RFM SCORE STRING
# ==============================

rfm['RFM_Score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)

print("\nRFM Scores:")
print(rfm.head())

# ==============================
# 6. CUSTOMER SEGMENTATION
# ==============================

def segment_customer(row):
    if row['R_score'] == 4 and row['F_score'] == 4 and row['M_score'] == 4:
        return 'VIP Customers'
    
    elif row['F_score'] >= 3 and row['M_score'] >= 3:
        return 'Loyal Customers'
    
    elif row['R_score'] >= 3 and row['F_score'] <= 2:
        return 'Potential Customers'
    
    elif row['R_score'] <= 2 and row['F_score'] >= 3:
        return 'At Risk'
    
    else:
        return 'Lost Customers'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# ==============================
# 7. SEGMENT SUMMARY
# ==============================

print("\nCustomer Segments Count:")
print(rfm['Segment'].value_counts())

# ==============================
# 8. SAVE FINAL DATA
# ==============================

rfm.to_csv('data/rfm_segmented.csv')

print("\n✅ RFM segmented data saved as 'data/rfm_segmented.csv'")