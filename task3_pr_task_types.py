"""
Task 3: Extract PR Task Type Data from AIDev Dataset
Extracts data from the pr_task_type table and creates a CSV file.
"""

import pandas as pd
from datasets import load_dataset
import os

def main():
    print("Loading AIDev dataset - pr_task_type table...")
    
    # Load the dataset from HuggingFace
    dataset = load_dataset("hao-li/AIDev", "pr_task_type", split="train")
    
    print(f"Loaded {len(dataset)} records from pr_task_type table")
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset)
    
    # Create output DataFrame with required columns
    output_df = pd.DataFrame({
        'PRID': df['id'],
        'PRTITLE': df['title'],
        'PRREASON': df['reason'],
        'PRTYPE': df['type'],
        'CONFIDENCE': df['confidence']
    })
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, 'task3_pr_task_types.csv')
    output_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Successfully created {output_path}")
    print(f"Total records: {len(output_df)}")
    print("\nFirst few rows:")
    print(output_df.head())

if __name__ == "__main__":
    main()
