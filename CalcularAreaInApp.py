from qgis.PyQt.QtWidgets import QDialog, QLabel, QComboBox, QVBoxLayout, QPushButton
from qgis.core import QgsProject, QgsField, QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
import processing

class LayerSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selecionar Camadas")

        # Layout do diálogo
        layout = QVBoxLayout()

        # Rótulos e combobox para seleção de camadas
        self.label_input_layer = QLabel("Camada de Uso do Solo:")
        self.combo_input_layer = QComboBox()
        self.label_overlay_layer = QLabel("Camada de APP:")
        self.combo_overlay_layer = QComboBox()

        # Preencher as comboboxes com as camadas carregadas no projeto
        self.load_layers()

        # Botão para executar
        self.ok_button = QPushButton("Executar")
        self.ok_button.clicked.connect(self.accept)

        # Adicionar os widgets ao layout
        layout.addWidget(self.label_input_layer)
        layout.addWidget(self.combo_input_layer)
        layout.addWidget(self.label_overlay_layer)
        layout.addWidget(self.combo_overlay_layer)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def load_layers(self):
        """Carrega as camadas do projeto no combobox."""
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            self.combo_input_layer.addItem(layer.name(), layer)
            self.combo_overlay_layer.addItem(layer.name(), layer)

    def get_selected_layers(self):
        """Retorna as camadas selecionadas pelo usuário."""
        input_layer = self.combo_input_layer.currentData()
        overlay_layer = self.combo_overlay_layer.currentData()
        return input_layer, overlay_layer


def calculate_area(intersection_layer):
    """Adiciona um campo de área na camada de interseção."""
    # Abre a camada de interseção
    provider = intersection_layer.dataProvider()

    # Adiciona um novo campo para armazenar a área
    provider.addAttributes([QgsField("area", QVariant.Double)])
    intersection_layer.updateFields()

    # Índice do campo de área
    area_idx = intersection_layer.fields().indexFromName('area_APP')

    # Calcula a área de cada feição e atualiza o novo campo
    with edit(intersection_layer):
        for feature in intersection_layer.getFeatures():
            geom = feature.geometry()
            area = geom.area()  # Calcula a área da geometria
            feature.setAttribute(area_idx, area)
            intersection_layer.updateFeature(feature)

    # Atualiza a exibição da tabela de atributos
    intersection_layer.updateFields()
    print("Campo de área calculado e adicionado com sucesso!")


def run_intersection_and_area_calculation():
    # Abre o diálogo de seleção de camadas
    dialog = LayerSelectionDialog()

    if dialog.exec_():
        input_layer, overlay_layer = dialog.get_selected_layers()

        if input_layer and overlay_layer:
            # Definir parâmetros para a ferramenta de Interseção
            params = {
                'INPUT': input_layer,
                'OVERLAY': overlay_layer,
                'OUTPUT': 'memory:areas_in_app'  # Salva o resultado em memória
            }

            # Executar a ferramenta de Interseção
            result = processing.run('native:intersection', params)
            intersection_layer = result['OUTPUT']

            # Adiciona a camada de interseção ao projeto
            QgsProject.instance().addMapLayer(intersection_layer)

            # Calcular a área das feições na camada de interseção
            calculate_area(intersection_layer)

# Executa o processo de interseção e cálculo de área
run_intersection_and_area_calculation()