#%% 
import os
import shutil
import subprocess
import time
import numpy as np
#%% 

# Define user folder 

folder = "C:/sim/Anna/Vminteq40"

output_directory = "C:/sim/Anna/Output_Auto"
additional_input_directory = "C:/sim/Anna/Input"

os.chdir(folder)
# Define paths and filenames
input_file = "minin.vda"
output_file = "vmint.ou2"
program_command = [r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"]  

# %%
import os
import shutil
import subprocess
import time
import numpy as np

def run_program_over_iterations(
    initial_file_path,            # Path to the initial template input file
    working_file_path,            # Path to the working input file (overwritten each iteration)
    output_directory,             # Directory to save output files
    additional_input_directory,   # Additional directory for copying modified input files
    program_command,              # Command to run the external program
    output_prefix="split",        # Prefix for output file names
    start_a=1.00,                 # Start value for 'a'
    end_a=2.00,                   # End value for 'a'
    increment=0.10                # Increment for 'a' values
):
    # Define the array of 'a' values based on start, end, and increment
    a_values = np.arange(start_a, end_a + increment, increment)
    last_output_file = None  # Variable to store the path of the last output file

    # Loop through each 'a' value
    for a in a_values:
        # Step 1: Open and modify the input file in reverse order
        with open(initial_file_path, 'r') as file:
            lines = file.readlines()

        # Initialize x_value to be set once the 1700 line is encountered
        x_value = None

        # Process lines from bottom to top
        for j in reversed(range(len(lines))):
            line = lines[j].strip()  # Strip whitespace

            # Check for the 1700 line to extract x_value
            if line.startswith("1700"):
                parts = line.split(',')
                x_value = float(parts[1])  # Extract and store the x_value for use in Comp. no 1:
                # print(f"Found 1700 line: x_value={x_value}")

            # Check for Comp. no 1: line for modification if x_value is already known
            elif line.startswith("Comp") and x_value is not None:
                parts = line.split(',')
                parts[-1] = f"{x_value * 12.0 * a:.8f}"  # Update the last value with x * a, formatted to 8 decimals
                lines[j] = ','.join(parts) + '\n'
                # print(f"Modified Comp. no 1: {lines[j]}")

            elif line.startswith("Ionic"):
            # Insert a line above the "Ionic" line
            # The new line to be added: "Z-(6)(aq),Concentration\n"
                lines.insert(j, "Z-(6)(aq),Concentration\n")

            # Check for the 1702 line to modify the second element based on 'a' alone
            elif line.startswith("1702"):
                parts = line.split(',')
                parts[1] = f"{12.0 * x_value * 0.00702 * a:.8f}"  # Update with 0.00702 * a, formatted to 8 decimals
                lines[j] = ','.join(parts)+ '\n'
                # print(f"Modified 1702 line: {lines[j]}")
                # 
           
            elif line.startswith("Selected"):
                parts = line.split(',')
                parts[1] = "13"  # Update the 4th element with the new 'a' value
                lines[j] = ','.join(parts) + '\n'
                # print(f"Modified Other settings: {lines[j]}") 

            # Modify the Other settings: line for the current 'a' value
            elif line.startswith("Other settings:"):
                parts = line.split(',')
                parts[3] = f"{a:.2f}"  # Update the 4th element with the new 'a' value
                lines[j] = ','.join(parts) + '\n'
                # print(f"Modified Other settings: {lines[j]}")

            elif line.startswith("END"):
                x_value = None

        # Write the modified lines back to the working input file
        with open(working_file_path, 'w') as file:
            file.writelines(lines)

        # Copy the modified input file to the additional input directory
        additional_input_file_path = os.path.join(additional_input_directory, f"input_{a:.2f}.vda")
        shutil.copyfile(working_file_path, additional_input_file_path)
        # print(f"Copied modified input file to {additional_input_file_path}")

        # Step 2: Run the external program in the terminal
        try:
            print(f"Running program for a={a:.2f}...")
            result = subprocess.run(program_command, text=True, check=True)
            print("Done")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the program: {e}")
            continue  # Skip to the next iteration if an error occurs

        # Step 3: Rename and copy the output file with the custom prefix
        timestamp = int(time.time())  # Use a timestamp to make filenames unique
        output_filename = f"{output_prefix}_{a:.2f}_{timestamp}.ou2"
        new_output_file_path = os.path.join(output_directory, output_filename)

        # Check for duplicate output file
        if last_output_file is not None:
            with open(last_output_file, 'r') as last_file, open(output_file, 'r') as new_file:
                last_lines = last_file.readlines()[:10]  # Read the first 10 lines of the last output file
                new_lines = new_file.readlines()[:10]    # Read the first 10 lines of the new output file

            if last_lines == new_lines:
                print(f"Warning: The new output file is identical to the last output file: {last_output_file}. Skipping this iteration.")
                continue  # Skip moving the file if it is a duplicate

        # Move the new output file
        shutil.move(output_file, new_output_file_path)
        print(f"Saved output to {new_output_file_path}")

        # Update the last output file path for the next iteration comparison
        last_output_file = new_output_file_path

# Split 1
# run_program_over_iterations(
#     initial_file_path=r"C:\sim\Anna\minin.vda\Split_1\minin.vda",
#     working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
#     output_directory="C:/sim/Anna/Output_Auto",
#     additional_input_directory="C:/sim/Anna/Input/Split 1",  # New directory for modified input files
#     program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
#     output_prefix="split_1_",
#     start_a=1,                 # Start value for 'a'
#     end_a=1.5,                   # End value for 'a'
#     increment=0.5                # Increment for 'a' values

# )
#%% rest of the splits

# Split 1
# run_program_over_iterations(
#     initial_file_path=r"C:\sim\Anna\minin.vda\Split_1\minin.vda",
#     working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
#     output_directory="C:/sim/Anna/Output_Auto",
#     additional_input_directory="C:/sim/Anna/Input/Split 1",  # New directory for modified input files
#     program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
#     output_prefix="split_1_",
#     start_a=0.05,                 # Start value for 'a'
#     end_a=3.5,                   # End value for 'a'
#     increment=0.05                # Increment for 'a' values    
# )

# # Split 2
# run_program_over_iterations(
#     initial_file_path=r"C:\sim\Anna\minin.vda\Split_2\minin.vda",
#     working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
#     output_directory="C:/sim/Anna/Output_Auto",
#     additional_input_directory="C:/sim/Anna/Input/Split 2",  # New directory for modified input files
#     program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
#     output_prefix="split_2_",
#     start_a=0.05,                 # Start value for 'a'
#     end_a=3.50,                   # End value for 'a'
#     increment=0.05                # Increment for 'a' values
# )

# Split 3
run_program_over_iterations(
    initial_file_path=r"C:\sim\Anna\minin.vda\Split_3\minin.vda",
    working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
    output_directory="C:/sim/Anna/Output_Auto",
    additional_input_directory="C:/sim/Anna/Input/Split 3",  # New directory for modified input files
    program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
    output_prefix="split_3_",
    start_a=1.60,                 # Start value for 'a'
    end_a=3.50,                   # End value for 'a'
    increment=0.05                # Increment for 'a' values
)

# Split 4
run_program_over_iterations(
    initial_file_path=r"C:\sim\Anna\minin.vda\Split_4\minin.vda",
    working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
    output_directory="C:/sim/Anna/Output_Auto",
    additional_input_directory="C:/sim/Anna/Input/Split 4",  # New directory for modified input files
    program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
    output_prefix="split_4_",
    start_a=0.05,                 # Start value for 'a'
    end_a=3.50,                   # End value for 'a'
    increment=0.05                # Increment for 'a' values
)

# Split 5
run_program_over_iterations(
    initial_file_path=r"C:\sim\Anna\minin.vda\Split_5\minin.vda",
    working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
    output_directory="C:/sim/Anna/Output_Auto",
    additional_input_directory="C:/sim/Anna/Input/Split 5",  # New directory for modified input files
    program_command=[r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"],
    output_prefix="split_5_",
    start_a=0.05,                 # Start value for 'a'
    end_a=3.50,                   # End value for 'a'
    increment=0.05                # Increment for 'a' values
)

#%%
import pandas as pd
import glob
import os

# Define the directory where output files are stored
output_directory = "C:/sim/Anna/Output_Auto"

# Initialize an empty list to store data from each output file
output_data = []

# Find all output files in the output directory with the .ou2 extension
output_files = glob.glob(os.path.join(output_directory, "*.ou2"))

# Process each file
for file_path in output_files:
    # Read the file into a DataFrame, skipping the first and third lines, and using the second line as the header
    df = pd.read_csv(file_path, sep='\t', skiprows=[0, 2], header=0)
    
    # Add a column to store the filename or unique identifier (e.g., x value) for tracking
    df['file'] = os.path.basename(file_path)
    
    # Append to the list of DataFrames
    output_data.append(df)

# Concatenate all data into a single DataFrame for comparison
combined_df = pd.concat(output_data, ignore_index=True)

# Display the combined data to verify
print(combined_df.head())

# Example analysis: Compare specific columns across output files
# Calculate the mean and standard deviation of "Sum of cations" and "Sum of anions" for each file
comparison_summary = combined_df.groupby('file')[['Sum of cations', 'Sum of anions']].agg(['mean', 'std'])

print("\nComparison summary across files:")
print(comparison_summary)


# %% Complete

#%%
import os
import shutil
import subprocess
import time
import numpy as np

# Define user folders and paths
folder = "C:/sim/Anna/Vminteq40"
output_directory = "C:/sim/Anna/Output_Auto"
input_file = "minin.vda"
output_file = "vmint.ou2"
program_command = [r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"]

os.chdir(folder)

# Define the range for the value 'a' from 1.00 to 2.00 in increments of 0.10
a_values = np.arange(1.00, 2.01, 0.10)

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

for a in a_values:
    # Step 1: Open and modify the input file in reverse order
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Initialize x_value to be set once the 1700 line is encountered
    x_value = None

    # Process lines from bottom to top
    for j in reversed(range(len(lines))):
        line = lines[j]

        # Check for Comp. no 1: line for modification if x_value is already known
        if line.startswith("Comp. no 1:") and x_value is not None:
            parts = line.split(',')
            parts[-1] = f"{x_value * 12.0 * a:.8f}"  # Update the last value with x * a, formatted to 8 decimals
            lines[j] = ','.join(parts) 

        # Check for the 1700 line to extract x_value
        elif line.startswith("1700"):
            parts = line.split(',')
            x_value = float(parts[1])  # Extract and store the x_value for use in Comp. no 1:

        # Check for the 1702 line to modify the second element based on 'a' alone
        elif line.startswith("1702"):
            parts = line.split(',')
            parts[1] = f"{ 12.0 * x_value * 0.00702 * a:.8f}"  # Update with 0.00702 * a, formatted to 8 decimals
            lines[j] = ','.join(parts)

        # Modify the Other settings: line for the current 'a' value
        elif line.startswith("Other settings:"):
            parts = line.split(',')
            parts[3] = f"{a:.2f}"  # Update the 4th element with the new 'a' value
            lines[j] = ','.join(parts)
        
        elif line.startswith("END"):
            x_value = None
    
    # Write the modified lines back to the file
    with open(input_file, 'w') as file:
        file.writelines(lines)

    # Step 2: Run the program
    try:
        print(f"Running program for a={a:.2f}...")
        result = subprocess.run(program_command, text=True, check=True)
        print("Done")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the program: {e}")
        continue  # Skip to the next iteration if an error occurs

    # Step 3: Rename and copy the output file
    timestamp = int(time.time())  # Use a timestamp to make filenames unique
    output_filename = f"output_{a:.2f}_{timestamp}.ou2"
    shutil.move(output_file, os.path.join(output_directory, output_filename))

    print(f"Saved output to {output_filename}")

run_program_over_iterations(
    initial_file_path=r"C:\sim\Anna\minin.vda\Split_1\minin.vda",
    working_file_path=r"C:\sim\Anna\Vminteq40\minin.vda",
    output_directory = "C:/sim/Anna/Output_Auto",
    program_command=program_command,
    output_prefix="split_1_",
    start_x=1.00,
    end_x=2.00,
    increment=0.05
)

# %%
import pandas as pd
import glob
import os

# Define the directory where output files are stored
output_directory = "C:/sim/Anna/Output_Auto"

# Initialize an empty list to store data from each output file
output_data = []

# Find all output files in the output directory with the .ou2 extension
output_files = glob.glob(os.path.join(output_directory, "*.ou2"))

# Process each file
for file_path in output_files:
    # Extract the unique identifier (e.g., a value) from the filename
    a_value = os.path.basename(file_path).split("_")[1]
    
    # Read the file into a DataFrame, skipping the first and third lines, and using the second line as the header
    df = pd.read_csv(file_path, sep='\t', skiprows=[0, 2], header=0)
    
    # Add a column to identify the file's a_value for tracking in the combined DataFrame
    df['a_value'] = a_value
    
    # Append to the list of DataFrames
    output_data.append(df)

# Concatenate all data into a single DataFrame for comparison
combined_df = pd.concat(output_data, ignore_index=True)

combined_df

#%% 
import os
import shutil
import subprocess
import time
import numpy as np

# Define user folders and paths
folder = "C:/sim/Anna/Vminteq40"
output_directory = "C:/sim/Anna/Output_Auto"
input_file = "minin.vda"
output_file = "vmint.ou2"
program_command = [r"C:\Users\anlr0006\AppData\Local\Programs\Vminteq40\MintrunC20M.exe"]
input_files_directory = os.path.join(folder, "modified_inputs")

# Ensure the input files directory exists
os.makedirs(input_files_directory, exist_ok=True)

# Define the range for the value 'a' from 1.00 to 2.00 in increments of 0.10
a_values = np.arange(1.00, 2.01, 0.5)

os.chdir(folder)

def create_input_files(a_values, input_file, input_files_directory):
    """
    Create modified input files based on different values of 'a'.
    """
    for a in a_values:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Initialize x_value to be set once the 1700 line is encountered
        x_value = None

        # Process lines from bottom to top
        for j in reversed(range(len(lines))):
            line = lines[j]

            # Check for Comp. no 1: line for modification if x_value is already known
            if line.startswith("Comp. no 1:") and x_value is not None:
                parts = line.split(',')
                parts[-1] = f"{x_value * 12.0 * a:.8f}"  # Update the last value with x * a, formatted to 8 decimals
                lines[j] = ','.join(parts)

            # Check for the 1700 line to extract x_value
            elif line.startswith("1700"):
                parts = line.split(',')
                x_value = float(parts[1])  # Extract and store the x_value for use in Comp. no 1:

            # Check for the 1702 line to modify the second element based on 'a' alone
            elif line.startswith("1702"):
                parts = line.split(',')
                parts[1] = f"{12.0 * x_value * 0.00702 * a:.8f}"  # Update with 0.00702 * a, formatted to 8 decimals
                lines[j] = ','.join(parts)

            # Modify the Other settings: line for the current 'a' value
            elif line.startswith("Other settings:"):
                parts = line.split(',')
                parts[3] = f"{a:.2f}"  # Update the 4th element with the new 'a' value
                lines[j] = ','.join(parts)

            elif line.startswith("END"):
                x_value = None

        # Write the modified lines to a new input file
        modified_input_file_path = os.path.join(input_files_directory, f"modified_input_a_{a:.2f}.vda")
        with open(modified_input_file_path, 'w') as file:
            file.writelines(lines)

        print(f"Created input file: {modified_input_file_path}")

def run_simulation(a_values, program_command, output_directory, input_file):
    """
    Run the simulation for each value of 'a' and handle the output files.
    """
    for a in a_values:
        # Step 1: Modify the input file (already done in create_input_files)
        
        # Run the program
        try:
            print(f"Running program for a={a:.2f}...")
            result = subprocess.run(program_command, text=True, check=True)
            print("Done")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the program: {e}")
            continue  # Skip to the next iteration if an error occurs

        # Step 3: Rename and copy the output file
        timestamp = int(time.time())  # Use a timestamp to make filenames unique
        output_filename = f"output_{a:.2f}_{timestamp}.ou2"
        new_output_file_path = os.path.join(output_directory, output_filename)

        # Check for duplicate output file
        last_output_file = None
        for file in os.listdir(output_directory):
            if file.startswith("output_") and file.endswith(".ou2"):
                last_output_file = os.path.join(output_directory, file)

        if last_output_file:
            with open(last_output_file, 'r') as last_file, open(output_file, 'r') as new_file:
                last_lines = [last_file.readline() for _ in range(10)]
                new_lines = [new_file.readline() for _ in range(10)]

            if last_lines == new_lines:
                print(f"Error: The new output file is identical to the last output file: {last_output_file}.")
                continue  # Skip moving the file if it is a duplicate

        shutil.move(output_file, new_output_file_path)
        print(f"Saved output to {output_filename}")

# Usage example
# Create modified input files
create_input_files(a_values, input_file, input_files_directory)

# Run the simulation for each value of 'a'
run_simulation(a_values, program_command, output_directory, input_file)

#%%
import os
import shutil

# Define the main folder containing subfolders
main_folder = r'C:\sim\Anna\Output'
# Define the new folder where you want to save the renamed files
output_folder = r'C:\sim\Anna\Out_VM'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each subfolder in the main folder
for folder_name in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, folder_name)

    # Check if it's a directory
    if os.path.isdir(subfolder_path):
        # Construct the full path to the vmint.ou2 file
        vmint_file = os.path.join(subfolder_path, 'vmint.ou2')
        
        # Check if the vmint.ou2 file exists
        if os.path.isfile(vmint_file):
            # Define the new file name in lowercase and the new path
            new_file_name = f"{folder_name.lower()}.ou2"  # Convert folder name to lowercase
            new_file_path = os.path.join(output_folder, new_file_name)
            
            # Copy the file to the new location with the new name
            shutil.copy(vmint_file, new_file_path)
            
            # Optional: Print a message indicating success
            print(f"Copied and renamed: {vmint_file} to {new_file_path}")
        else:
            print(f"File not found in: {subfolder_path}")


# %%
