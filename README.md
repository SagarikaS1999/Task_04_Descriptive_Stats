# 📊 Task_04_Descriptive_Stats

## Overview

This project focuses on generating comprehensive descriptive statistics for three real-world datasets related to the **2024 U.S. Presidential Election** on social media (Facebook Ads, Facebook Posts, and Twitter Posts). The goal is to compute identical statistical summaries using three distinct approaches:

- ✅ Pure Python (no third-party libraries)
- ✅ Pandas
- ✅ Polars

Each approach outputs:
- Overall dataset statistics
- Per-column statistics (numeric and categorical)
- Aggregated statistics by key groups (e.g., `page_id`, `source`, `post_id`, `ad_id`)
---

## 📌 Datasets Used

- **Facebook Ads**: `2024_fb_ads_president_scored_anon.csv`
- **Facebook Posts**: `2024_fb_posts_president_scored_anon.csv`
- **Twitter Posts**: `2024_tw_posts_president_scored_anon.csv`

---

2. **Run the desired script** from your terminal:
   ```bash
   # For Facebook Ads    
   python pure_python_stats_fb_ads        # Pure Python
   python pandas_python_stats_fb_ads      # Pandas
   python polars_python_stats_fb_ads      # Polars
   
   # For Facebook Posts
   python pure_python_stats_fb_posts        # Pure Python
   python pandas_python_stats_fb_posts      # Pandas
   python polars_python_stats_fb_posts      # Polars

   # For Twitter Posts
   python pure_python_stats_tw_posts        # Pure Python
   python pandas_python_stats_tw_posts      # Pandas
   python polars_python_stats_tw_posts      # Polars

---

## 🧠 Summary of Findings

This project aimed to compute descriptive statistics across Facebook Ads, Facebook Posts, and Twitter Posts datasets using Pure Python, Pandas, and Polars. 

- **Consistency**: All approaches produced equivalent results for numeric and categorical summaries.
- **Ease of Use**: Pandas was most convenient due to its high-level API.
- **Performance**: Polars delivered faster execution on large datasets, especially for groupby operations.
- **Manual Control**: Pure Python allowed deeper insight into statistical logic but required more verbose code.
- **Data Insights**:
  - `page_id` and `post_id` revealed which accounts were most active.
  - `source` analysis in Twitter highlighted dominant platforms and tweet types.
  - `*_illuminating` variables helped tag content thematically (e.g., fraud, economy, environment).

---

## ✅ Output Includes

- Summary statistics (count, mean, min, max, std)
- Categorical breakdowns (top values, unique counts)
- Grouped analysis (e.g., by `page_id`, `source`, `post_id`)
- CSV exports for use in further analysis or visualization

---
