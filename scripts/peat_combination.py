#%%
# import os
import pandas as pd

# Define the folder containing the CSV files
folder_path = "/mnt/wsl/peat_area"

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate through all files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".csv"):  # Check if the file is a CSV
        file_path = os.path.join(folder_path, file)
        print(f"Loading {file_path}...")
        # Read the CSV into a DataFrame and append to the list
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Combine all DataFrames into one by appending row by row
combined_df = pd.concat(dataframes, ignore_index=True)

# Display information about the combined DataFrame
print("Combined DataFrame:")
print(combined_df.info())
print(combined_df.head())

# Optional: Save the combined DataFrame to a new CSV
output_path =  "../input/catchment_characteristics/peat_area.csv"
combined_df.to_csv(output_path, index=False)
print(f"Combined DataFrame saved to {output_path}")

# %%
os.getcwd()