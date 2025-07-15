import csv
import math
from collections import Counter, defaultdict

# Global list to store all output for CSV
output_data = []

def add_to_output(analysis_type, column_name, metric, value, group_info=""):
    """Add analysis result to output data"""
    output_data.append({
        'analysis_type': analysis_type,
        'group_info': group_info,
        'column_name': column_name,
        'metric': metric,
        'value': value
    })

def is_numeric(value):
    """Check if a value can be converted to a number"""
    if value is None or value == '':
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False

def safe_float(value):
    """Convert value to float, return None if not possible"""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except ValueError:
        return None

def calculate_stats(values):
    """Calculate basic statistics for numeric values"""
    numeric_values = [v for v in values if v is not None]
    if not numeric_values:
        return {
            'count': 0,
            'mean': None,
            'min': None,
            'max': None,
            'std': None
        }
    
    count = len(numeric_values)
    mean = sum(numeric_values) / count
    minimum = min(numeric_values)
    maximum = max(numeric_values)
    
    # Calculate standard deviation
    if count > 1:
        variance = sum((x - mean) ** 2 for x in numeric_values) / (count - 1)
        std = math.sqrt(variance)
    else:
        std = 0
    
    return {
        'count': count,
        'mean': mean,
        'min': minimum,
        'max': maximum,
        'std': std
    }

def analyze_column(column_data, column_name, analysis_type="Overall", group_info=""):
    """Analyze a single column"""
    print(f"\n--- Analysis for column: {column_name} ---")
    
    # Check if column is numeric
    numeric_values = []
    all_values = []
    
    for value in column_data:
        all_values.append(value)
        if is_numeric(value):
            numeric_values.append(safe_float(value))
    
    # Basic counts
    total_count = len(all_values)
    non_null_count = len([v for v in all_values if v is not None and v != ''])
    
    print(f"Total Count: {total_count}")
    print(f"Non-null Count: {non_null_count}")
    
    # Add to output
    add_to_output(analysis_type, column_name, "total_count", total_count, group_info)
    add_to_output(analysis_type, column_name, "non_null_count", non_null_count, group_info)
    
    # If mostly numeric, treat as numeric
    if len(numeric_values) > total_count * 0.5:  # More than 50% numeric
        stats = calculate_stats(numeric_values)
        print(f"Mean: {stats['mean']:.4f}" if stats['mean'] is not None else "Mean: N/A")
        print(f"Min: {stats['min']}")
        print(f"Max: {stats['max']}")
        print(f"Std Dev: {stats['std']:.4f}" if stats['std'] is not None else "Std Dev: N/A")
        
        # Add to output
        add_to_output(analysis_type, column_name, "mean", stats['mean'], group_info)
        add_to_output(analysis_type, column_name, "min", stats['min'], group_info)
        add_to_output(analysis_type, column_name, "max", stats['max'], group_info)
        add_to_output(analysis_type, column_name, "std", stats['std'], group_info)
    else:
        # Treat as categorical
        non_null_values = [v for v in all_values if v is not None and v != '']
        if non_null_values:
            value_counts = Counter(non_null_values)
            unique_count = len(value_counts)
            most_common = value_counts.most_common(5)
            
            print(f"Unique Values: {unique_count}")
            print("Most Frequent Values:")
            for value, count in most_common:
                print(f"  '{value}': {count}")
            
            # Add to output
            add_to_output(analysis_type, column_name, "unique_count", unique_count, group_info)
            for i, (value, count) in enumerate(most_common):
                add_to_output(analysis_type, column_name, f"most_frequent_{i+1}", f"{value}:{count}", group_info)

def analyze_grouped_data(data, headers, group_columns, group_name):
    """Analyze data after grouping by specified columns"""
    print(f"\n{'='*60}")
    print(f"ANALYSIS GROUPED BY {group_name}")
    print(f"{'='*60}")
    
    # Get indices of grouping columns
    group_indices = []
    for col in group_columns:
        if col in headers:
            group_indices.append(headers.index(col))
    
    if not group_indices:
        print("Grouping columns not found in dataset")
        return
    
    # Group data
    groups = defaultdict(list)
    for row in data:
        # Create group key
        group_key = tuple(row[i] if i < len(row) else '' for i in group_indices)
        groups[group_key].append(row)
    
    print(f"Number of groups: {len(groups)}")
    
    # Analyze each group
    group_sizes = []
    for group_key, group_data in groups.items():
        group_sizes.append(len(group_data))
    
    if group_sizes:
        print(f"Group size - Min: {min(group_sizes)}, Max: {max(group_sizes)}, Mean: {sum(group_sizes)/len(group_sizes):.2f}")
        
        # Add group summary to output
        add_to_output(f"Grouped_{group_name}", "GROUP_SUMMARY", "num_groups", len(groups))
        add_to_output(f"Grouped_{group_name}", "GROUP_SUMMARY", "group_size_min", min(group_sizes))
        add_to_output(f"Grouped_{group_name}", "GROUP_SUMMARY", "group_size_max", max(group_sizes))
        add_to_output(f"Grouped_{group_name}", "GROUP_SUMMARY", "group_size_mean", sum(group_sizes)/len(group_sizes))
    
    # Show top 5 largest groups
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    print("\nTop 5 largest groups:")
    for i, (group_key, group_data) in enumerate(sorted_groups[:5]):
        group_display = " | ".join(f"{group_columns[j]}={group_key[j]}" for j in range(len(group_key)))
        print(f"{i+1}. {group_display}: {len(group_data)} records")
        
        # Add to output
        add_to_output(f"Grouped_{group_name}", "TOP_GROUPS", f"top_group_{i+1}", f"{group_display}:{len(group_data)}")
    
    # Analyze key numeric columns for aggregated stats
    numeric_columns = ['estimated_audience_size', 'estimated_impressions', 'estimated_spend']
    
    print(f"\nAggregated statistics for numeric columns:")
    for col_name in numeric_columns:
        if col_name in headers:
            col_idx = headers.index(col_name)
            
            # Calculate aggregated stats across all groups
            all_group_stats = []
            for group_key, group_data in groups.items():
                column_data = [safe_float(row[col_idx]) if col_idx < len(row) else None for row in group_data]
                stats = calculate_stats(column_data)
                if stats['mean'] is not None:
                    all_group_stats.append(stats['mean'])
            
            if all_group_stats:
                agg_stats = calculate_stats(all_group_stats)
                print(f"  {col_name} (group means): Count={agg_stats['count']}, Mean={agg_stats['mean']:.4f}, Min={agg_stats['min']:.4f}, Max={agg_stats['max']:.4f}")
                
                # Add to output
                add_to_output(f"Grouped_{group_name}", col_name, "group_means_count", agg_stats['count'])
                add_to_output(f"Grouped_{group_name}", col_name, "group_means_mean", agg_stats['mean'])
                add_to_output(f"Grouped_{group_name}", col_name, "group_means_min", agg_stats['min'])
                add_to_output(f"Grouped_{group_name}", col_name, "group_means_max", agg_stats['max'])

def save_output_to_csv(filename_prefix):
    """Save output data to CSV file"""
    output_filename = f"{filename_prefix}_analysis_results.csv"
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['analysis_type', 'group_info', 'column_name', 'metric', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in output_data:
            writer.writerow(row)
    
    print(f"\nAnalysis results saved to: {output_filename}")

def main():
    """Main function to analyze Facebook Ads dataset"""
    filename = "2024_fb_ads_president_scored_anon.csv"
    
    print(f"{'='*60}")
    print(f"FACEBOOK ADS DATASET ANALYSIS")
    print(f"{'='*60}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            # Read all data
            data = []
            for row in reader:
                while len(row) < len(headers):
                    row.append('')
                data.append(row)
            
            print(f"Dataset Shape: {len(data)} rows × {len(headers)} columns")
            
            # Add basic dataset info to output
            add_to_output("Dataset_Info", "BASIC", "total_rows", len(data))
            add_to_output("Dataset_Info", "BASIC", "total_columns", len(headers))
            
            # Overall dataset analysis
            print(f"\n--- OVERALL DATASET ANALYSIS ---")
            print(f"Total Records: {len(data)}")
            
            # Column-by-column analysis
            print(f"\n--- COLUMN-BY-COLUMN ANALYSIS ---")
            for i, header in enumerate(headers):
                column_data = [row[i] if i < len(row) else '' for row in data]
                analyze_column(column_data, header, "Overall")
            
            # Group by page_id
            analyze_grouped_data(data, headers, ['page_id'], "page_id")
            
            # Group by page_id and ad_id
            analyze_grouped_data(data, headers, ['page_id', 'ad_id'], "page_id_ad_id")
            
            # Save results to CSV
            save_output_to_csv("fb_ads")
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error analyzing {filename}: {str(e)}")

if __name__ == "__main__":
    main()