"""
Finding the sample id's of all the samples which came from the SLU lab
"""

#%%
import os
import pandas as pd
from collections import Counter

# Define the folder containing the JSON files
folder_path = r"\\storage.slu.se\Home$\anlr0006\My Documents\04_Projects\02_Top-Down\01_data\02_raw_data\01_mvm_miljödata\JSON"

# Initialize a list to store the results
results = []

# Iterate through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        print(file_path)
        # Open the file as a text file
        with open(file_path, 'r', encoding='utf-8') as f:
            data_str = f.read()

        # Find all occurrences of "analysisLabs":"xxxx"
        matches = []
        start_idx = 0
        while True:
            start_idx = data_str.find('"analysisLabs":"', start_idx)
            if start_idx == -1:
                break
            start_idx += len('"analysisLabs":"')
            end_idx = data_str.find('"', start_idx)
            if end_idx != -1:
                matches.append(data_str[start_idx:end_idx])

        # Count occurrences of each "xxxx"
        counter = Counter(matches)

        # Prepare a row for this file
        row = {
            "file_number": int(file_name.split('.')[0]),
            "total_analysisLabs": sum(counter.values()),
        }
        row.update(counter)  # Add the counts for each "xxxx"
        results.append(row)

# Create a DataFrame
df = pd.DataFrame(results)

# Fill missing values with 0 (for files where some "xxxx" are absent)
df.fillna(0, inplace=True)

df['Prop_SLU'] = (df['SLUVoM']+ df['SERI; SLUVoM']) / df['total_analysisLabs']
df['Prop_SLU_plus'] = (df['SLUVoM']+ df['SERI; SLUVoM']+ df['Uppgift saknas']) / df['total_analysisLabs']
df['Prop_SLU_samples'] = (df['SLUVoM']+ df['SERI; SLUVoM']+ df['Uppgift saknas'])
df['Prop_samples'] = (df['SLUVoM']+ df['SERI; SLUVoM'])
# Save the DataFrame to a CSV file
# df.to_csv("analysis_labs_summary.csv", index=False)

# Display the DataFrame
print(df)

# %%
import os
import pandas as pd
import json

# Define the folder containing the JSON files
folder_path = r"\\storage.slu.se\Home$\anlr0006\My Documents\04_Projects\02_Top-Down\01_data\02_raw_data\01_mvm_miljödata\JSON"

# Initialize a list to store the sample IDs that have SLU in the analysis lab
slu_sample_ids = []

# Iterate through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        print(f"Processing file: {file_path}")
        
        # Open the file as a JSON object
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Assuming each file is a JSON object
        
        # Check if the data contains the 'samples' key
        if 'samples' in data:
            # Loop through each sample in the 'samples' list
            for record in data['samples']:
                # Check if 'analysisLabs' exists in the sample and contains 'SLU'
                if 'analysisLabs' in record and 'SLU' in record['analysisLabs']:
                    # Extract the sampleId if the analysisLabs field contains 'SLU'
                    sample_id = record.get('sampleId', None)
                    if sample_id:
                        slu_sample_ids.append(sample_id)

# Convert the list of SLU sample IDs to a DataFrame
slu_df = pd.DataFrame(slu_sample_ids, columns=['SLU_sampleId'])

# Save the DataFrame to a CSV file
#slu_df.to_csv("../results/chemistry/slu_sample_ids.csv", index=False)

# Display the DataFrame
print(slu_df)