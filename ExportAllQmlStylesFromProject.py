from qgis.core import QgsProject, QgsLayerTreeGroup
import os

# Local onde será exportado os QMLs, sempre use \\
output_dir = "C:\\Users\\geraldo.junior\\Desktop\\qmlEspeleo"

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def sanitize_path_component(name):
    """Sanitize a string for use in a file or folder path."""
    return name.strip().replace(":", "_").replace("/", "_").replace("\\", "_")


def export_layer_styles(group, base_path=""):
    """Recursively export QML styles for all layers in a group or subgroup."""
    for child in group.children():
        if isinstance(child, QgsLayerTreeGroup):
            # Recurse into subgroups
            new_base_path = os.path.join(
                base_path, sanitize_path_component(
                    child.name()))
            export_layer_styles(child, new_base_path)
        elif isinstance(child, QgsLayerTreeLayer):  # Correct type check for layers
            # Handle layers
            layer = child.layer()
            if layer:
                # Construct the QML file path
                qml_name = f"{sanitize_path_component(layer.name())}.qml"
                qml_path = os.path.join(output_dir, base_path, qml_name)

                # Ensure subdirectories exist
                os.makedirs(os.path.dirname(qml_path), exist_ok=True)

                # Export the style
                layer.saveNamedStyle(qml_path)
                print(f"Exported: {qml_path}")


# Start exporting styles from the root of the layer tree
root = QgsProject.instance().layerTreeRoot()
export_layer_styles(root)

print('Script terminated!')
