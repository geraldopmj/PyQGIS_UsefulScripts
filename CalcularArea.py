from qgis.PyQt.QtWidgets import QDialog, QLabel, QComboBox, QVBoxLayout, QPushButton
from qgis.core import QgsProject, QgsField, QgsVectorLayer, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils, edit
from qgis.PyQt.QtCore import QVariant

active_layer = iface.activeLayer()

if active_layer:
    print(f"A camada ativa é: {active_layer.name()}")
else:
    print("Nenhuma camada ativa foi selecionada.")


def calculate_total_area(layer):
    """Calcula a área total das feições na camada de interseção e adiciona ou atualiza campos para a área usando QgsExpression."""
    provider = layer.dataProvider()

    # Adiciona os campos, se não existirem
    if layer.fields().indexFromName('area_ha') == -1:
        provider.addAttributes([QgsField("area_ha", QVariant.Double)])
    if layer.fields().indexFromName('area_m2') == -1:
        provider.addAttributes([QgsField("area_m2", QVariant.Double)])

    layer.updateFields()

    # Índice dos campos de área
    area_idx = layer.fields().indexFromName('area_ha')
    area_idx2 = layer.fields().indexFromName('area_m2')

    # Expressão para cálculo de área
    area_expression = QgsExpression("area(@geometry)")
    context = QgsExpressionContext()
    context.appendScopes(
        QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    # Calcula a área total e atualiza os campos
    with edit(layer):
        for feature in layer.getFeatures():
            context.setFeature(feature)
            area = area_expression.evaluate(context)
            if area is None:
                continue  # Pula feições com geometria inválida

            area_ha = area / 10000  # Converte para hectares
            feature.setAttribute(area_idx, area_ha)
            feature.setAttribute(area_idx2, area)
            layer.updateFeature(feature)


# Executa o processo de cálculo de área
if active_layer and isinstance(active_layer, QgsVectorLayer):
    calculate_total_area(active_layer)
    print("Cálculo de áreas concluído!")
else:
    print("Camada ativa inválida ou não é uma camada vetorial.")

print("Script finalizado!")
