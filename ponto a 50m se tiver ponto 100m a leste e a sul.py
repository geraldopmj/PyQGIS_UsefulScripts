from qgis.core import *
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
import math

# Função para calcular a distância entre dois pontos em metros (projeção plana)
def distance_in_meters(p1, p2):
    return math.sqrt((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2)

# Camada de entrada (substitua com sua camada de pontos)
layer = iface.activeLayer()

# Criar uma nova camada temporária para os novos pontos
new_layer = QgsVectorLayer("Point?crs=EPSG:4326", "New Points", "memory")
new_layer_provider = new_layer.dataProvider()
new_layer_provider.addAttributes([QgsField("id", QVariant.Int)])
new_layer.updateFields()

# Preparar para adicionar novos pontos
new_features = []

# Iterar sobre todos os pontos na camada
for feature in layer.getFeatures():
    geom = feature.geometry()
    point = geom.asPoint()
    
    point_100m_east = None
    point_100m_south = None
    
    # Iterar novamente para verificar se há pontos a 100 metros ao leste e ao sul
    for other_feature in layer.getFeatures():
        if other_feature.id() != feature.id():
            other_geom = other_feature.geometry()
            other_point = other_geom.asPoint()
            
            # Verifica ponto a 100 metros a leste
            if abs(other_point.x() - (point.x() + 100)) < 0.01 and abs(other_point.y() - point.y()) < 0.01:
                point_100m_east = other_point
            
            # Verifica ponto a 100 metros ao sul
            if abs(other_point.y() - (point.y() - 100)) < 0.01 and abs(other_point.x() - point.x()) < 0.01:
                point_100m_south = other_point
    
    # Se encontrou ambos os pontos
    if point_100m_east and point_100m_south:
        # Criar novo ponto 50m a leste e 50m ao sul
        new_x = point.x() + 50
        new_y = point.y() - 50
        new_point = QgsPointXY(new_x, new_y)
        
        # Criar nova feição para o novo ponto
        new_feature = QgsFeature(new_layer.fields())
        new_feature.setGeometry(QgsGeometry.fromPointXY(new_point))
        new_features.append(new_feature)

# Adicionar os novos pontos à nova camada
new_layer_provider.addFeatures(new_features)

# Adicionar a nova camada ao projeto
QgsProject.instance().addMapLayer(new_layer)

iface.messageBar().pushMessage("Script finalizado", "Novos pontos adicionados", level=Qgis.Info)
