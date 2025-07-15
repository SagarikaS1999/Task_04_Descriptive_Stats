import pandas as pd
import numpy as np
import os

def analyze_fb_ads_dataset():
    """
    Analyze Facebook Ads Presidential dataset
    Research Analyst: Comprehensive descriptive statistics and aggregations
    """
    
    # Load dataset
    df = pd.read_csv('2024_fb_ads_president_scored_anon.csv')
    
    print("=== FACEBOOK ADS DATASET ANALYSIS ===")
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
    categorical_df.to_csv('polar_fb_ads_categorical_analysis.csv', index=False)
    
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
    numerical_analysis.to_csv('polar_fb_ads_numerical_analysis.csv')
    
    # 3. GROUP BY PAGE_ID ANALYSIS
    print("\n=== GROUP BY PAGE_ID ANALYSIS ===")
    if 'page_id' in df.columns:
        page_grouped = df.groupby('page_id').agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col != 'page_id'}
        }).round(4)
        
        page_grouped.columns = ['_'.join(col).strip() for col in page_grouped.columns]
        page_grouped = page_grouped.reset_index()
        
        print(f"Page-level aggregation: {page_grouped.shape}")
        print(page_grouped.head())
        page_grouped.to_csv('polar_fb_ads_page_groupby_analysis.csv', index=False)
    
    # 4. GROUP BY PAGE_ID AND AD_ID ANALYSIS
    print("\n=== GROUP BY PAGE_ID AND AD_ID ANALYSIS ===")
    if 'page_id' in df.columns and 'ad_id' in df.columns:
        page_ad_grouped = df.groupby(['page_id', 'ad_id']).agg({
            # Numerical aggregations
            **{col: ['count', 'mean', 'median', 'std', 'min', 'max'] for col in numerical_cols if col in df.columns},
            # Categorical aggregations
            **{col: ['count', 'nunique'] for col in categorical_cols if col in df.columns and col not in ['page_id', 'ad_id']}
        }).round(4)
        
        page_ad_grouped.columns = ['_'.join(col).strip() for col in page_ad_grouped.columns]
        page_ad_grouped = page_ad_grouped.reset_index()
        
        print(f"Page-Ad level aggregation: {page_ad_grouped.shape}")
        print(page_ad_grouped.head())
        page_ad_grouped.to_csv('polar_fb_ads_page_ad_groupby_analysis.csv', index=False)
    
    # Summary Report
    print("\n=== SUMMARY REPORT ===")
    print(f"Total records: {len(df):,}")
    print(f"Unique pages: {df['page_id'].nunique() if 'page_id' in df.columns else 'N/A'}")
    print(f"Unique ads: {df['ad_id'].nunique() if 'ad_id' in df.columns else 'N/A'}")
    print(f"Date range: {df['ad_creation_time'].min()} to {df['ad_creation_time'].max()}" if 'ad_creation_time' in df.columns else "Date info not available")
    
    # Check for illuminating scored variables
    illuminating_cols = [col for col in df.columns if 'illuminating' in col.lower()]
    print(f"Illuminating variables found: {len(illuminating_cols)}")
    
    print("\n=== FILES GENERATED ===")
    print("1. polar_fb_ads_categorical_analysis.csv")
    print("2. polar_fb_ads_numerical_analysis.csv") 
    print("3. polar_fb_ads_page_groupby_analysis.csv")
    print("4. polar_fb_ads_page_ad_groupby_analysis.csv")

if __name__ == "__main__":
    analyze_fb_ads_dataset()