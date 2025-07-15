import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('2024_tw_posts_president_scored_anon.csv')

print("="*60)
print("TWITTER POSTS DATASET ANALYSIS")
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
numerical_stats.to_csv('twitter_posts_numeric_analysis.csv')

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
categorical_analysis.to_csv('twitter_posts_categorical_analysis.csv', index=False)

# 3. Aggregation by source
print("\n3. AGGREGATION BY SOURCE")
source_agg = df.groupby('source').agg({
    'id': 'count',
    'retweetCount': ['mean', 'median', 'sum'],
    'replyCount': ['mean', 'median', 'sum'],
    'likeCount': ['mean', 'median', 'sum'],
    'quoteCount': ['mean', 'median', 'sum'],
    'viewCount': ['mean', 'median', 'sum'],
    'advocacy_msg_type_illuminating': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
    'issue_msg_type_illuminating': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
    'covid_topic_illuminating': 'mean',
    'economy_topic_illuminating': 'mean',
    'education_topic_illuminating': 'mean'
}).round(2)

# Flatten column names
source_agg.columns = ['_'.join(col).strip() for col in source_agg.columns.values]
source_agg = source_agg.rename(columns={'id_count': 'total_posts'})

print(f"Source-level aggregation shape: {source_agg.shape}")
print(source_agg.head())

# Save source aggregation
source_agg.to_csv('twitter_posts_source.csv')

# 4. Aggregation by source and id
print("\n4. AGGREGATION BY SOURCE AND ID")
source_id_agg = df.groupby(['source', 'id']).agg({
    'retweetCount': 'first',
    'replyCount': 'first',
    'likeCount': 'first',
    'quoteCount': 'first',
    'viewCount': 'first',
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

print(f"Post-level aggregation shape: {source_id_agg.shape}")
print(source_id_agg.head())

# Save post aggregation
source_id_agg.to_csv('twitter_posts_page_id_ad_id.csv')

print("\n" + "="*60)
print("ANALYSIS COMPLETE - FILES SAVED:")
print("- twitter_posts_numeric_analysis.csv")
print("- twitter_posts_categorical_analysis.csv")
print("- twitter_posts_source.csv")
print("- twitter_posts_source_id.csv")
print("="*60)
