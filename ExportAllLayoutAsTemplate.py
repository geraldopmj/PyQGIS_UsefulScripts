import os

# Set the output directory where the templates will be saved
output_directory = r'F:/Projetos/Geoprocessamento/01_Projetos/2287/03_Mxd_Qgs'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Get the current QGIS project instance
project = QgsProject.instance()

# Get the layout manager
layout_manager = project.layoutManager()

# Get all the layouts in the project
layouts = layout_manager.layouts()

# Loop through all layouts and export each as a .qpt template
for layout in layouts:
    # Define the template output file path
    layout_name = layout.name()
    output_path = os.path.join(output_directory, f"{layout_name}.qpt")
    
    # Save the layout as a .qpt template
    layout.saveAsTemplate(output_path, QgsReadWriteContext())

    print(f"Exported layout '{layout_name}' as {output_path}")

print("All layouts have been exported.")