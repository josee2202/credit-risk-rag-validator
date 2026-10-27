import os
import sys

# ? Añadimos dinámicamente la carpeta padre al path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Codigo_sas import ProcesarSAS

def main(directory_path):
    if not os.path.exists(directory_path):
        print(f"El directorio '{directory_path}' no existe.")
        return

    print(f"Cargando archivos SAS desde el directorio: {directory_path}")
    
    procesador = ProcesarSAS("descargas/source.spm")
    
    # 1. Cargar archivos
    documents = procesador.read_directory(directory_path)
    print(f"Se han cargado {len(documents)} documentos.")

    # 2. Aplicar split
    split_documents = procesador.split_documents_2(documents)
    print(f'Cantidad de Chunks: {len(split_documents)}')

    # 3. Agrupar bloques en chunks largos optimizados
    grupos = procesador.agrupar_bloques_por_longitud(split_documents, max_length=2400)
    print(f'Tenemos {len(grupos)} bloques de código sintetizados.')

    # 4. Generara los textos explicando los bloques de código
    respuestas = procesador.generar_respuestas(grupos)

    # 5. Almacenar los resultados en un word
    procesador.guardar_respuestas_en_word(respuestas, r'.\Resultados\04_tests\Pruebas\Prueba_9\resultados_test_sas_9.docx')

    procesador.guardar_respuestas_en_word(procesador.historial_respuestas, r'.\Resultados\04_tests\Pruebas\Prueba_9\contextos_test_9.docx')


if __name__ == "__main__":
    # Ruta al directorio que deseas procesar
    path_to_directory = r"<RAIZ_PROYECTO>\01. Test estadísticos"
    
    # Llamar a la función main
    main(path_to_directory)



