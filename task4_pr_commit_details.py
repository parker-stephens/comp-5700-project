"""
Task 4: Extract PR Commit Details from AIDev Dataset
Extracts data from the pr_commit_details table and creates a CSV file.
Cleans special characters from the patch/diff to avoid string encoding errors.
"""

import pandas as pd
from datasets import load_dataset
import os
import re

def clean_diff(diff_text):
    """
    Remove special characters from diff to avoid string encoding errors.
    """
    if pd.isna(diff_text) or diff_text is None:
        return ""
    
    # Convert to string if not already
    diff_str = str(diff_text)
    
    # Remove non-printable characters except common whitespace
    # Keep letters, numbers, basic punctuation, and common whitespace
    cleaned = re.sub(r'[^\x20-\x7E\n\r\t]', '', diff_str)
    
    return cleaned

def main():
    print("Loading AIDev dataset - pr_commit_details table...")
    
    # Load the dataset from HuggingFace
    dataset = load_dataset("hao-li/AIDev", "pr_commit_details", split="train")
    
    print(f"Loaded {len(dataset)} records from pr_commit_details table")
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset)
    
    # Clean the patch/diff column
    print("Cleaning patch/diff data to remove special characters...")
    df['cleaned_patch'] = df['patch'].apply(clean_diff)
    
    # Create output DataFrame with required columns
    output_df = pd.DataFrame({
        'PRID': df['pr_id'],
        'PRSHA': df['sha'],
        'PRCOMMITMESSAGE': df['message'],
        'PRFILE': df['filename'],
        'PRSTATUS': df['status'],
        'PRADDS': df['additions'],
        'PRDELSS': df['deletions'],
        'PRCHANGECOUNT': df['changes'],
        'PRDIFF': df['cleaned_patch']
    })
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, 'task4_pr_commit_details.csv')
    output_df.to_csv(output_path, index=False, encoding='utf-8', errors='replace')
    
    print(f"Successfully created {output_path}")
    print(f"Total records: {len(output_df)}")
    print("\nFirst few rows (excluding PRDIFF for readability):")
    print(output_df.drop('PRDIFF', axis=1).head())

if __name__ == "__main__":
    main()
