import pandas as pd
import numpy as np
import os

def analyze_fb_posts_dataset():
    """
    Analyze Facebook Posts Presidential dataset
    Research Analyst: Comprehensive descriptive statistics and aggregations
    """
    
    # Load dataset
    df = pd.read_csv('2024_fb_posts_president_scored_anon.csv')
    
    print("=== FACEBOOK POSTS DATASET ANALYSIS ===")
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
    categorical_df.to_csv('polar_fb_posts_categorical_analysis.csv', index=False)
    
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
    numerical_analysis.to_csv('polar_fb_posts_numerical_analysis.csv')
    
    # 3. GROUP BY FACEBOOK_ID ANALYSIS
    print("\n=== GROUP BY FACEBOOK_ID ANALYSIS ===")
    if 'Facebook_Id' in df.columns:
        facebook_grouped = df.groupby('Facebook_Id').agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col != 'Facebook_Id'}
        }).round(4)
        
        facebook_grouped.columns = ['_'.join(col).strip() for col in facebook_grouped.columns]
        facebook_grouped = facebook_grouped.reset_index()
        
        print(f"Facebook ID level aggregation: {facebook_grouped.shape}")
        print(facebook_grouped.head())
        facebook_grouped.to_csv('polar_fb_posts_facebook_id_groupby_analysis.csv', index=False)
    
    # 4. GROUP BY FACEBOOK_ID AND POST_ID ANALYSIS
    print("\n=== GROUP BY FACEBOOK_ID AND POST_ID ANALYSIS ===")
    if 'Facebook_Id' in df.columns and 'post_id' in df.columns:
        facebook_post_grouped = df.groupby(['Facebook_Id', 'post_id']).agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col not in ['Facebook_Id', 'post_id']}
        }).round(4)
        
        facebook_post_grouped.columns = ['_'.join(col).strip() for col in facebook_post_grouped.columns]
        facebook_post_grouped = facebook_post_grouped.reset_index()
        
        print(f"Facebook ID-Post level aggregation: {facebook_post_grouped.shape}")
        print(facebook_post_grouped.head())
        facebook_post_grouped.to_csv('polar_fb_posts_facebook_post_groupby_analysis.csv', index=False)
    
    # Summary Report
    print("\n=== SUMMARY REPORT ===")
    print(f"Total records: {len(df):,}")
    print(f"Unique Facebook IDs: {df['Facebook_Id'].nunique() if 'Facebook_Id' in df.columns else 'N/A'}")
    print(f"Unique posts: {df['post_id'].nunique() if 'post_id' in df.columns else 'N/A'}")
    print(f"Date range: {df['Post Created Date'].min()} to {df['Post Created Date'].max()}" if 'Post Created Date' in df.columns else "Date info not available")
    
    # Engagement metrics summary
    engagement_cols = ['Total Interactions', 'Likes', 'Comments', 'Shares', 'Love', 'Wow', 'Haha', 'Sad', 'Angry', 'Care']
    existing_engagement = [col for col in engagement_cols if col in df.columns]
    if existing_engagement:
        print(f"\nEngagement metrics available: {existing_engagement}")
        print(f"Average total interactions: {df['Total Interactions'].mean():.2f}" if 'Total Interactions' in df.columns else "")
    
    # Check for illuminating scored variables
    illuminating_cols = [col for col in df.columns if 'illuminating' in col.lower()]
    print(f"Illuminating variables found: {len(illuminating_cols)}")
    
    print("\n=== FILES GENERATED ===")
    print("1. polar_fb_posts_categorical_analysis.csv")
    print("2. polar_fb_posts_numerical_analysis.csv") 
    print("3. polar_fb_posts_facebook_id_groupby_analysis.csv")
    print("4. polar_fb_posts_facebook_post_groupby_analysis.csv")

if __name__ == "__main__":
    analyze_fb_posts_dataset()