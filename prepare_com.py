import os
import re
import sys

def create_com_files(path):
    # Get all .log files in the current directory
    log_files = [file for file in os.listdir('.') if file.endswith('.log')]
    
    for log_file in log_files:
        # Extract prefix from the log filename
        prefix = os.path.splitext(log_file)[0]
        com_filename = f"{prefix}.com"
        
        with open(log_file, 'r') as log_f:
            log_content = log_f.readlines()
        
        # Prepare content for the .com file
        com_content = []
        com_content.append(f"%Chk={path}/{prefix}.chk\n")
        # Don't forget to change the input keywords here
        com_content.append("#P opt freq b3lyp/aug-cc-pvtz empiricaldispersion=gd3 pop=full scf=(qc,maxcycle=512) gfinput gfprint\n")
        com_content.append("\n")  # Blank line
        com_content.append("Title Card Here\n")
        com_content.append("\n")  # Blank line
        
        charge, multiplicity = "", ""
        coords_started = False
        for i, line in enumerate(log_content):
            if "Charge" in line and "Multiplicity" in line:
                charge = re.search("Charge =  (\d+)", line).group(1)
                multiplicity = re.search("Multiplicity = (\d+)", line).group(1)
                print(charge + multiplicity)
            if "Redundant internal coordinates" in line:
                coords_started = True
                com_content.append(f"{charge} {multiplicity}\n")  # Add charge and multiplicity
                continue
            if "Recover connectivity" in line:
                coords_started = False
            if coords_started:
                # Transform coordinates
                line = line.replace(",0,", "                  ")
                line = line.replace(",", "    ")
                com_content.append(line)
        
        com_content.append("\n\n")  # Leave two blank lines at the end
        
        # Write to the .com file
        with open(com_filename, 'w') as com_f:
            com_f.writelines(com_content)
        
        print(f"Created: {com_filename}")

if __name__ == "__main__":
    # Get the path from user input
    if len(sys.argv) != 2:
        print("Usage: python script.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    create_com_files(path)

