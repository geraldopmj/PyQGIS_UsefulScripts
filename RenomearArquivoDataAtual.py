import os
from datetime import datetime

# Assign your Windows directory to the variable `local`
local = r'F:\\Projetos\\Geoprocessamento\\01_Projetos\\0758\\CEMIG_GT\\02_fotovoltaicas\\08_ufv_emborcacao\\10_Figuras\\RAS_IBAMA_mf'

# Get today's date in 'yymmdd' format
today = datetime.now().strftime('%y%m%d')

# Iterate through all files in the specified directory
for filename in os.listdir(local):
    # Get the full path of the file
    filepath = os.path.join(local, filename)
    
    # Check if it's a file (not a directory) and has the correct extension
    if os.path.isfile(filepath) and filename.lower().endswith(('.png', '.jpeg', '.pdf')):
        # Separate the file name and its extension
        name, ext = os.path.splitext(filename)
        
        # Create the new name by appending the date
        new_filename = f"{name}_{today}{ext}"
        
        # Get the full path of the new file name
        new_filepath = os.path.join(local, new_filename)
        
        # Rename the file
        os.rename(filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")