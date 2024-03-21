#!/bin/bash

# Define the target directory to move files to
target_dir="neb_converged"

# Check if the target directory exists, create it if not
if [ ! -d "$target_dir" ]; then
  mkdir "$target_dir"
fi

# Function to check the last line and move files if it matches the criteria
move_if_normal_termination() {
  filename="$1"
  last_line=$(tail -n 1 "$filename")

  if [[ "$last_line" == *"Normal termination"* ]]; then
    # Extract the filename without extension
    base_name=$(basename "$filename" .log)
    # Move all related files to the target directory
    mv "${base_name}".* "$target_dir"/
  fi
}

#loop through all log files in current directory
for stru in *.log; do
    file_to_check=$stru # Replace filename.log with the actual file name

    # Call the function with the file to check
    move_if_normal_termination "$file_to_check"
done

