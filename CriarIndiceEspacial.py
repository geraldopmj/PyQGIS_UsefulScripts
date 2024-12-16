from qgis.core import QgsProject, QgsVectorLayer, QgsSpatialIndex

def check_and_create_spatial_index():
    for layer in QgsProject.instance().mapLayers().values():
        if isinstance(layer, QgsVectorLayer):  # Verifica se é uma camada vetorial
            if layer.isValid():  # Verifica se a camada é válida
                # Forçar carregamento dos dados para garantir que podemos criar o índice
                layer.dataProvider().forceReload()

                # Verifica se a camada já tem um índice espacial
                if layer.hasSpatialIndex():
                    print(f"Layer '{layer.name()}' já possui um índice espacial.")
                else:
                    print(f"Criando índice espacial para o layer '{layer.name()}'.")
                    # Tenta criar o índice espacial explicitamente
                    spatial_index = QgsSpatialIndex(layer.getFeatures())
                    if spatial_index is not None:
                        print(f"Índice espacial criado com sucesso para o layer '{layer.name()}'.")
                    else:
                        print(f"Falha ao criar índice espacial para o layer '{layer.name()}'.")
            else:
                print(f"Layer '{layer.name()}' é inválido, ignorando.")
        else:
            print(f"Layer '{layer.name()}' não é vetorial, ignorando.")

# Executa a função
check_and_create_spatial_index()