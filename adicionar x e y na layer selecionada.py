from qgis.core import QgsProject, QgsField
from PyQt5.QtCore import QVariant

# Get the active layer (selected layer in QGIS)
layer = iface.activeLayer()

# Check if the layer is valid and is a vector layer
if not layer or not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
    print("Invalid layer selected. Please select a vector layer.")
else:
    # Start editing the layer
    layer.startEditing()
    
    # Add two new fields (columns) for X and Y coordinates
    layer.dataProvider().addAttributes([
        QgsField("X_coord", QVariant.Double),
        QgsField("Y_coord", QVariant.Double)
    ])
    
    # Update the fields in the layer
    layer.updateFields()
    
    # Get the indices of the newly added fields
    x_index = layer.fields().indexOf('X_coord')
    y_index = layer.fields().indexOf('Y_coord')
    
    # Loop through each feature in the layer
    for feature in layer.getFeatures():
        # Get the geometry of the feature
        geom = feature.geometry()
        
        # Get the X and Y coordinates of the feature's centroid
        x_coord = geom.centroid().asPoint().x()
        y_coord = geom.centroid().asPoint().y()
        
        # Update the feature's attributes with the X and Y coordinates
        layer.changeAttributeValue(feature.id(), x_index, x_coord)
        layer.changeAttributeValue(feature.id(), y_index, y_coord)
    
    # Commit the changes
    layer.commitChanges()
    print("X and Y coordinates added to the attribute table.")