"""
Task 5: Create Security Analysis Report
Combines data from tasks 1-4 and adds SECURITY flag based on security-related keywords.
"""

import pandas as pd
import os
import re

# Security-related keywords from the project requirements
SECURITY_KEYWORDS = [
    'race', 'racy', 'buffer', 'overflow', 'stack', 'integer', 'signedness',
    'underflow', 'improper', 'unauthenticated', 'gain access', 'permission',
    'cross site', 'css', 'xss', 'denial service', 'dos', 'crash', 'deadlock',
    'injection', 'request forgery', 'csrf', 'xsrf', 'forged', 'security',
    'vulnerability', 'vulnerable', 'exploit', 'attack', 'bypass', 'backdoor',
    'threat', 'expose', 'breach', 'violate', 'fatal', 'blacklist', 'overrun',
    'insecure'
]

def check_security_keywords(text):
    """
    Check if any security-related keywords appear in the text.
    Returns 1 if security keyword found, 0 otherwise.
    """
    if pd.isna(text) or text is None:
        return 0
    
    # Convert to lowercase for case-insensitive matching
    text_lower = str(text).lower()
    
    # Check each keyword
    for keyword in SECURITY_KEYWORDS:
        if keyword in text_lower:
            return 1
    
    return 0

def main():
    print("Loading data from Task 1 (Pull Requests)...")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    
    # Load Task 1 output (pull requests)
    task1_path = os.path.join(output_dir, 'task1_pull_requests.csv')
    if not os.path.exists(task1_path):
        print(f"Error: {task1_path} not found. Please run task1_pull_requests.py first.")
        return
    
    df_pr = pd.read_csv(task1_path)
    print(f"Loaded {len(df_pr)} pull request records")
    
    # Load Task 3 output (PR task types)
    print("Loading data from Task 3 (PR Task Types)...")
    task3_path = os.path.join(output_dir, 'task3_pr_task_types.csv')
    if not os.path.exists(task3_path):
        print(f"Error: {task3_path} not found. Please run task3_pr_task_types.py first.")
        return
    
    df_task_type = pd.read_csv(task3_path)
    print(f"Loaded {len(df_task_type)} PR task type records")
    
    # Merge pull request data with task type data on ID/PRID
    print("Merging data from tasks 1 and 3...")
    merged_df = pd.merge(
        df_pr,
        df_task_type,
        left_on='ID',
        right_on='PRID',
        how='inner'
    )
    
    print(f"Merged dataset contains {len(merged_df)} records")
    
    # Check for security keywords in title and body
    print("Scanning for security-related keywords...")
    merged_df['SECURITY'] = merged_df.apply(
        lambda row: max(
            check_security_keywords(row['TITLE']),
            check_security_keywords(row['BODYSTRING'])
        ),
        axis=1
    )
    
    # Create final output DataFrame
    output_df = pd.DataFrame({
        'ID': merged_df['ID'],
        'AGENT': merged_df['AGENTNAME'],
        'TYPE': merged_df['PRTYPE'],
        'CONFIDENCE': merged_df['CONFIDENCE'],
        'SECURITY': merged_df['SECURITY']
    })
    
    # Save to CSV
    output_path = os.path.join(output_dir, 'task5_security_analysis.csv')
    output_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\nSuccessfully created {output_path}")
    print(f"Total records: {len(output_df)}")
    print(f"Records with security flag = 1: {output_df['SECURITY'].sum()}")
    print(f"Records with security flag = 0: {len(output_df) - output_df['SECURITY'].sum()}")
    print("\nFirst few rows:")
    print(output_df.head())
    
    # Print summary by agent
    print("\nSecurity-related PRs by Agent:")
    security_by_agent = output_df[output_df['SECURITY'] == 1].groupby('AGENT').size().sort_values(ascending=False)
    print(security_by_agent)

if __name__ == "__main__":
    main()
