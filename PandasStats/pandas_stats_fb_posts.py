import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('2024_fb_posts_president_scored_anon.csv')

print("="*60)
print("FACEBOOK POSTS DATASET ANALYSIS")
print("="*60)

# Basic dataset information
print(f"Dataset shape: {df.shape}")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

# Convert numeric columns that might be stored as strings
numeric_columns = ['Total Interactions', 'Likes', 'Comments', 'Shares', 'Post Views', 
                  'covid_topic_illuminating', 'economy_topic_illuminating', 
                  'education_topic_illuminating', 'environment_topic_illuminating',
                  'incivility_illuminating', 'fraud_illuminating']

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nData types after conversion:")
print(df.dtypes)

# 1. Numerical Analysis
print("\n1. NUMERICAL DATA ANALYSIS")
numerical_cols = df.select_dtypes(include=[np.number]).columns
numerical_stats = df[numerical_cols].describe()
print(numerical_stats)

# Save numerical analysis
numerical_stats.to_csv('fb_posts_numeric_analysis.csv')

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
categorical_analysis.to_csv('fb_posts_categorical_analysis.csv', index=False)

# 3. Aggregation by Facebook_Id
print("\n3. AGGREGATION BY FACEBOOK_ID")

# Define aggregation functions more carefully
agg_dict = {
    'post_id': 'count'
}

# Add numeric columns with proper aggregation
numeric_interaction_cols = ['Total Interactions', 'Likes', 'Comments', 'Shares', 'Post Views']
for col in numeric_interaction_cols:
    if col in df.columns:
        agg_dict[col] = ['mean', 'median', 'sum']

# Add categorical columns with mode calculation
categorical_mode_cols = ['advocacy_msg_type_illuminating', 'issue_msg_type_illuminating']
for col in categorical_mode_cols:
    if col in df.columns:
        agg_dict[col] = lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan

# Add binary/numeric topic columns with mean
topic_cols = ['covid_topic_illuminating', 'economy_topic_illuminating', 'education_topic_illuminating',
              'environment_topic_illuminating', 'incivility_illuminating', 'fraud_illuminating']
for col in topic_cols:
    if col in df.columns and df[col].dtype in ['int64', 'float64']:
        agg_dict[col] = 'mean'

try:
    Facebook_Id_agg = df.groupby('Facebook_Id').agg(agg_dict).round(2)
    
    # Flatten column names
    Facebook_Id_agg.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col 
                               for col in Facebook_Id_agg.columns.values]
    Facebook_Id_agg = Facebook_Id_agg.rename(columns={'post_id': 'total_posts'})
    
    print(f"Facebook_Id-level aggregation shape: {Facebook_Id_agg.shape}")
    print(Facebook_Id_agg.head())
    
    # Save page aggregation
    Facebook_Id_agg.to_csv('fb_posts_Facebook_Id_agg.csv')
    
except Exception as e:
    print(f"Error in Facebook_Id aggregation: {e}")
    print("Column data types:")
    for col in agg_dict.keys():
        if col in df.columns:
            print(f"{col}: {df[col].dtype}")

# 4. Aggregation by Facebook_Id and post_id
print("\n4. AGGREGATION BY FACEBOOK_ID AND POST_ID")

# Define columns for post-level aggregation
post_agg_cols = ['Total Interactions', 'Likes', 'Comments', 'Shares', 'Post Views',
                 'advocacy_msg_type_illuminating', 'issue_msg_type_illuminating', 
                 'attack_msg_type_illuminating', 'covid_topic_illuminating', 
                 'economy_topic_illuminating', 'education_topic_illuminating',
                 'environment_topic_illuminating', 'incivility_illuminating', 'fraud_illuminating']

# Filter to only include columns that exist in the dataframe
existing_cols = [col for col in post_agg_cols if col in df.columns]
post_agg_dict = {col: 'first' for col in existing_cols}

try:
    Facebook_Id_post_id_agg = df.groupby(['Facebook_Id', 'post_id']).agg(post_agg_dict).round(2)
    
    print(f"Facebook_Id_post_id-level aggregation shape: {Facebook_Id_post_id_agg.shape}")
    print(Facebook_Id_post_id_agg.head())
    
    # Save post aggregation
    Facebook_Id_post_id_agg.to_csv('fb_posts_Facebook_Id_post_id_agg.csv')
    
except Exception as e:
    print(f"Error in Facebook_Id_post_id aggregation: {e}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE - FILES SAVED:")
print("- fb_posts_numeric_analysis.csv")
print("- fb_posts_categorical_analysis.csv")
print("- fb_posts_Facebook_Id_agg.csv")
print("- fb_posts_Facebook_Id_post_id_agg.csv")
print("="*60)