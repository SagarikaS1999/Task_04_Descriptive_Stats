import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('2024_fb_ads_president_scored_anon.csv')

print("="*60)
print("FACEBOOK ADS DATASET ANALYSIS")
print("="*60)

# Basic dataset information
print(f"Dataset shape: {df.shape}")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

# 1. Numerical Analysis
print("\n1. NUMERICAL DATA ANALYSIS")
numerical_cols = df.select_dtypes(include=[np.number]).columns
numerical_stats = df[numerical_cols].describe()
print(numerical_stats)

# Save numerical analysis
numerical_stats.to_csv('fb_ads_numeric_analysis.csv')

# 2. Categorical Analysis
print("\n2. CATEGORICAL DATA ANALYSIS")
categorical_cols = df.select_dtypes(include=['object', 'category']).columns
categorical_summary = []

for col in categorical_cols:
    if col in df.columns:
        value_counts = df[col].value_counts()
        categorical_summary.append({
            'column': col,
            'unique_count': df[col].nunique(),
            'most_frequent': value_counts.index[0] if len(value_counts) > 0 else None,
            'most_frequent_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
            'total_records': len(df[col].dropna())
        })

categorical_analysis = pd.DataFrame(categorical_summary)
print(categorical_analysis)

# Save categorical analysis
categorical_analysis.to_csv('fb_ads_categorical_analysis.csv', index=False)

# 3. Aggregation by page_id
print("\n3. AGGREGATION BY PAGE_ID")
page_agg = df.groupby('page_id').agg({
    'ad_id': 'count',
    'estimated_audience_size': ['mean', 'median', 'sum'],
    'estimated_impressions': ['mean', 'median', 'sum'],
    'estimated_spend': ['mean', 'median', 'sum'],
    'advocacy_msg_type_illuminating': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
    'issue_msg_type_illuminating': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
    'covid_topic_illuminating': 'mean',
    'economy_topic_illuminating': 'mean',
    'education_topic_illuminating': 'mean'
}).round(2)

# Flatten column names
page_agg.columns = ['_'.join(col).strip() for col in page_agg.columns.values]
page_agg = page_agg.rename(columns={'ad_id_count': 'total_ads'})

print(f"Page-level aggregation shape: {page_agg.shape}")
print(page_agg.head())

# Save page aggregation
page_agg.to_csv('fb_ads_page_id.csv')

# 4. Aggregation by page_id and ad_id
print("\n4. AGGREGATION BY PAGE_ID AND AD_ID")
ad_agg = df.groupby(['page_id', 'ad_id']).agg({
    'estimated_audience_size': 'first',
    'estimated_impressions': 'first',
    'estimated_spend': 'first',
    'advocacy_msg_type_illuminating': 'first',
    'issue_msg_type_illuminating': 'first',
    'attack_msg_type_illuminating': 'first',
    'covid_topic_illuminating': 'first',
    'economy_topic_illuminating': 'first',
    'education_topic_illuminating': 'first',
    'environment_topic_illuminating': 'first',
    'incivility_illuminating': 'first',
    'fraud_illuminating': 'first'
}).round(2)

print(f"Ad-level aggregation shape: {ad_agg.shape}")
print(ad_agg.head())

# Save ad aggregation
ad_agg.to_csv('fb_ads_page_id_ad_id.csv')

print("\n" + "="*60)
print("ANALYSIS COMPLETE - FILES SAVED:")
print("- fb_ads_numeric_analysis.csv")
print("- fb_ads_categorical_analysis.csv")
print("- fb_ads_page_id.csv")
print("- fb_ads_page_id_ad_id.csv")
print("="*60)