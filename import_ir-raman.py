import os
import pandas as pd

# Function to extract X and Y values after "# Spectra"
def extract_spectra_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Find the line with '# Spectra' and note the index
            spectra_index = next(i for i, line in enumerate(lines) if '# Spectra' in line)
            # Extract the data after this index
            data = lines[spectra_index + 2:]  # +2 to skip the headers
            x_values = []
            y_values = []
            # Go through the data and split into X and Y values
            for line in data:
                if line.strip():  # Ensure that line is not empty
                    split_line = line.split()
                    x_values.append(float(split_line[0]))
                    y_values.append(float(split_line[1]))
            return x_values, y_values
    except StopIteration:
        print(f"'# Spectra' not found in {file_path}")
        return [], []  # Return empty lists if '# Spectra' not found
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return [], []  # Return empty lists in case of error

# Directory where the .txt files are stored
directory = os.getcwd()
##'G:/Research/12-SPAN/50_IR-Raman_analysis/li6/raman'

# Initialize a list to hold data from all files
all_data = []

# Go through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        x_values, y_values = extract_spectra_data(file_path)
        if x_values and y_values:  # Only add if data is not empty
            # Use filename without '.txt' as key
            all_data.append({'File Prefix': filename.replace('.txt', ''), 'X': x_values, 'Y': y_values})

# Convert list of dicts to a DataFrame
combined_df = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True, axis = 1)

# Save the combined data to a CSV file
csv_filename = os.path.join(directory, 'combined_data.csv')
combined_df.to_csv(csv_filename, index=False)

print(f"Data combined into {csv_filename}")
