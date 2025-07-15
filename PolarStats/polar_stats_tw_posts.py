import pandas as pd
import numpy as np
import os

def analyze_twitter_dataset():
    """
    Analyze Twitter Posts Presidential dataset
    Research Analyst: Comprehensive descriptive statistics and aggregations
    """
    
    # Load dataset
    df = pd.read_csv('2024_tw_posts_president_scored_anon.csv')
    
    print("=== TWITTER POSTS DATASET ANALYSIS ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Identify column types
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    print(f"\nNumerical columns ({len(numerical_cols)}): {numerical_cols}")
    print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols}")
    
    # 1. CATEGORICAL ANALYSIS
    print("\n=== CATEGORICAL ANALYSIS ===")
    categorical_stats = []
    
    for col in categorical_cols:
        if col in df.columns:
            unique_count = df[col].nunique()
            top_value = df[col].value_counts().index[0] if not df[col].empty else 'N/A'
            top_freq = df[col].value_counts().iloc[0] if not df[col].empty else 0
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            
            categorical_stats.append({
                'column': col,
                'unique_count': unique_count,
                'top_value': top_value,
                'top_frequency': top_freq,
                'missing_count': missing_count,
                'missing_percentage': missing_pct
            })
            
            print(f"{col}: {unique_count} unique values, Top: {top_value} ({top_freq}), Missing: {missing_count}")
    
    categorical_df = pd.DataFrame(categorical_stats)
    categorical_df.to_csv('polar_twitter_categorical_analysis.csv', index=False)
    
    # 2. NUMERICAL ANALYSIS
    print("\n=== NUMERICAL ANALYSIS ===")
    numerical_stats = df[numerical_cols].describe()
    
    # Add additional statistics
    additional_stats = pd.DataFrame({
        'missing_count': df[numerical_cols].isnull().sum(),
        'missing_percentage': (df[numerical_cols].isnull().sum() / len(df)) * 100,
        'skewness': df[numerical_cols].skew(),
        'kurtosis': df[numerical_cols].kurtosis()
    })
    
    numerical_analysis = pd.concat([numerical_stats, additional_stats.T])
    print(numerical_analysis)
    numerical_analysis.to_csv('polar_twitter_numerical_analysis.csv')
    
    # 3. GROUP BY SOURCE ANALYSIS
    print("\n=== GROUP BY SOURCE ANALYSIS ===")
    if 'source' in df.columns:
        source_grouped = df.groupby('source').agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col != 'source'}
        }).round(4)
        
        source_grouped.columns = ['_'.join(col).strip() for col in source_grouped.columns]
        source_grouped = source_grouped.reset_index()
        
        print(f"Source-level aggregation: {source_grouped.shape}")
        print(source_grouped.head())
        source_grouped.to_csv('polar_twitter_source_groupby_analysis.csv', index=False)
    
    # 4. GROUP BY SOURCE AND ID ANALYSIS
    print("\n=== GROUP BY SOURCE AND ID ANALYSIS ===")
    if 'source' in df.columns and 'id' in df.columns:
        source_id_grouped = df.groupby(['source', 'id']).agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col not in ['source', 'id']}
        }).round(4)
        
        source_id_grouped.columns = ['_'.join(col).strip() for col in source_id_grouped.columns]
        source_id_grouped = source_id_grouped.reset_index()
        
        print(f"Source-ID level aggregation: {source_id_grouped.shape}")
        print(source_id_grouped.head())
        source_id_grouped.to_csv('polar_twitter_source_id_groupby_analysis.csv', index=False)
    
    # Summary Report
    print("\n=== SUMMARY REPORT ===")
    print(f"Total records: {len(df):,}")
    print(f"Unique sources: {df['source'].nunique() if 'source' in df.columns else 'N/A'}")
    print(f"Unique tweet IDs: {df['id'].nunique() if 'id' in df.columns else 'N/A'}")
    print(f"Date range: {df['createdAt'].min()} to {df['createdAt'].max()}" if 'createdAt' in df.columns else "Date info not available")
    
    # Engagement metrics summary
    engagement_cols = ['retweetCount', 'replyCount', 'likeCount', 'quoteCount', 'viewCount', 'bookmarkCount']
    existing_engagement = [col for col in engagement_cols if col in df.columns]
    if existing_engagement:
        print(f"\nEngagement metrics available: {existing_engagement}")
        for col in existing_engagement:
            print(f"Average {col}: {df[col].mean():.2f}" if col in df.columns else "")
    
    # Tweet type analysis
    tweet_types = ['isReply', 'isRetweet', 'isQuote']
    existing_types = [col for col in tweet_types if col in df.columns]
    if existing_types:
        print(f"\nTweet type indicators: {existing_types}")
        for col in existing_types:
            if col in df.columns:
                true_count = df[col].sum() if df[col].dtype == 'bool' else df[col].value_counts().get(True, 0)
                print(f"{col}: {true_count} ({true_count/len(df)*100:.1f}%)")
    
    # Language analysis
    if 'lang' in df.columns:
        print(f"\nLanguage distribution:")
        print(df['lang'].value_counts().head())
    
    # Check for illuminating scored variables
    illuminating_cols = [col for col in df.columns if 'illuminating' in col.lower()]
    print(f"\nIlluminating variables found: {len(illuminating_cols)}")
    
    print("\n=== FILES GENERATED ===")
    print("1. polar_twitter_categorical_analysis.csv")
    print("2. polar_twitter_numerical_analysis.csv") 
    print("3. polar_twitter_source_groupby_analysis.csv")
    print("4. polar_twitter_source_id_groupby_analysis.csv")

if __name__ == "__main__":
    analyze_twitter_dataset()