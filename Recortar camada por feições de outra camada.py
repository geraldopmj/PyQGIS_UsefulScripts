# Importa as camadas
pastos_layer = QgsProject.instance().mapLayersByName(
    "ide_1003_mg_fusos_utm_pol")[0]
area_layer = QgsProject.instance().mapLayersByName(
    "758_ufv08_uso_solo_241203_pl")[0]

# Diretório para salvar os recortes
# Defina o caminho de saída aqui
output_dir = "F:\\Projetos\\Geoprocessamento\\01_Projetos\\0758\\CEMIG_GT\\02_fotovoltaicas\\08_ufv_emborcacao\\01_Shapefile"

# Percorre cada polígono da camada 'pastos'
for pasto_feature in pastos_layer.getFeatures():
    # Obtém a geometria e o ID ou nome do pasto
    pasto_geom = pasto_feature.geometry()
    pasto_id = pasto_feature["fuso"]  # Ajuste se o campo for diferente

    # Verifica e corrige a geometria do pasto
    if not pasto_geom.isGeosValid():
        pasto_geom = pasto_geom.makeValid()

    # Cria uma camada temporária com o polígono do pasto
    temp_layer = QgsVectorLayer(
        "Polygon?crs=" +
        pastos_layer.crs().authid(),
        "temp_layer",
        "memory")
    temp_layer_data = temp_layer.dataProvider()
    temp_layer_data.addAttributes([QgsField("fuso", QVariant.String)])
    temp_layer.updateFields()

    # Adiciona a feição ao temporário
    temp_feat = QgsFeature()
    temp_feat.setGeometry(pasto_geom)
    temp_feat.setAttributes([pasto_id])
    temp_layer_data.addFeature(temp_feat)

    # Define o nome do arquivo de saída
    output_path = f"{output_dir}\\758_uso_solo_241104_{pasto_id}_pl.shp"

    # Configura o processamento do recorte
    parameters = {
        'INPUT': area_layer,
        'OVERLAY': temp_layer,
        'OUTPUT': output_path
    }

    # Executa o recorte com `qgis:intersection`
    result = processing.run("qgis:intersection", parameters)

    # Verifica o resultado do recorte
    output_layer = QgsVectorLayer(result['OUTPUT'], "output", "ogr")
    if output_layer.featureCount() > 0:
        print(f"Recorte salvo em {output_path}")
    else:
        print(f"Feição {pasto_id} não gerou interseção útil e foi ignorado.")

print("Script Terminated!")
