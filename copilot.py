import os
import configparser
import shutil

def menu():
    config = None
    while True:
        print("--- Menú de Configuración ---")
        print("1. Crear Nuevo Archivo de Configuración")
        print("2. Cargar Configuración")
        print("3. Ver Configuración")
        print("4. Cambiar Parámetros")
        print("5. Crear Directorios")
        print("6. Clasificar Archivos")
        print("7. Filtrar Archivos")
        print("0. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            config = crear_configuracion()
        elif opcion == '2':
            config = cargar_configuracion()
        elif opcion == '3':
            if config is not None:
                ver_configuracion(config)
            else:
                print("Primero debes cargar o crear una configuración.")
        elif opcion == '4':
            if config is not None:
                cambiar_parametros(config)
            else:
                print("Primero debes cargar o crear una configuración.")
        elif opcion == '5':
            if config is not None:
                crear_directorios(config)
            else:
                print("Primero debes cargar o crear una configuración.")
        elif opcion == '6':
            if config is not None:
                clasificar_archivos(config)
            else:
                print("Primero debes cargar o crear una configuración.")
        elif opcion == '7':
            if config is not None:
                filtrar_archivos(config)
            else:
                print("Primero debes cargar o crear una configuración.")
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def ver_configuracion(config):
    for section in config.sections():
        print()
        print(f"--- {section} ---")
        print()
        for key, value in config.items(section):
            print(f"{key}: {value}")
        print()

def cargar_configuracion():
    archivo_config = input("Introduce el nombre del archivo de configuración: ")
    config = configparser.ConfigParser()
    if not os.path.exists(archivo_config):
        print("El archivo de configuración no existe.")
        return None
    try:
        config.read(archivo_config)
        print("¡Configuración cargada con éxito!")
        return config
    except configparser.Error as e:
        print("Error al leer el archivo de configuración:", e)
        return None

def crear_configuracion():
    config = configparser.ConfigParser()
    config['PARAMETROS'] = {}
    print("Introduce los valores para los siguientes parámetros:")
    for parametro in ['DIR_INIT', 'DIR_DST', 'MIDA_PETITA', 'MIDA_MITJANA', 'EXTENSIO_FILTRADA', 'DIR_QUARANTENA', 'ZIP_FILE', 'REPORT_FILE']:
        valor = input(f"{parametro}: ")
        config['PARAMETROS'][parametro] = valor
    print("¡Configuración creada con éxito!")
    #Guardar configuración
    archivo_nuevo = input("Introduce el nombre del archivo de configuración a crear o sobrescribir: ")
    confirmacion = input(f"¿Estás seguro que quieres guardar la configuración en {archivo_nuevo}? (S/N): ")
    if confirmacion.upper() == 'S':
        try:
            with open(archivo_nuevo, 'w') as configfile:
                config.write(configfile)
            print("¡Configuración guardada con éxito!")
        except IOError as e:
            print(f"Error al guardar la configuración: {e}")

def cambiar_parametros(config):
    seccion = 'PARAMETROS'
    parametros = config[seccion]
    print("Parámetros disponibles para modificar:")
    for parametro, valor in parametros.items():
        print(f"{parametro}: {valor}")

    parametro = input("Introduce el nombre del parámetro que quieres cambiar: ")
    if parametro in parametros:
        valor_actual = parametros[parametro]
        print(f"El valor actual de {parametro} es: {valor_actual}")
        nuevo_valor = input("Introduce el nuevo valor: ")
        config.set(seccion, parametro, nuevo_valor)
        print("¡Valor cambiado con éxito!")

        archivo_nuevo = input("Introduce el nombre del archivo de configuración a actualizar: ")
        confirmacion = input(f"¿Estás seguro que quieres guardar la configuración en {archivo_nuevo}? (S/N): ")
        if confirmacion.upper() == 'S':
            try:
                with open(archivo_nuevo, 'w') as configfile:
                    config.write(configfile)
                print("¡Configuración guardada con éxito!")
            except IOError as e:
                print(f"Error al guardar la configuración: {e}")
    else:
        print("El parámetro ingresado no es válido.")

    return config

def crear_directorios(config):
    dir_dst = config.get('PARAMETROS', 'DIR_DST')
    if not os.path.exists(dir_dst):
        try:
            os.makedirs(dir_dst)
            print(f"Directorio {dir_dst} creado correctamente.")
        except OSError as e:
            print(f"Error al crear el directorio {dir_dst}: {e}")
    else:
        print(f"El directorio {dir_dst} ya existe.")

def clasificar_archivos(config):
    try:
        dir_init = config.get('PARAMETROS', 'DIR_INIT')
        dir_dst = config.get('PARAMETROS', 'DIR_DST')
        mida_petita = int(config.get('PARAMETROS', 'MIDA_PETITA')) * 1024
        mida_mitjana = int(config.get('PARAMETROS', 'MIDA_MITJANA')) * 1024

        for root, dirs, files in os.walk(dir_init):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_owner = os.stat(file_path).st_uid

                if file_size < mida_petita:
                    size_dir = 'petit'
                elif mida_petita <= file_size < mida_mitjana:
                    size_dir = 'mitja'
                else:
                    size_dir = 'gran'

                final_dir = os.path.join(dir_dst, str(file_owner), size_dir)

                if not os.path.exists(final_dir):
                    os.makedirs(final_dir)

                shutil.move(file_path, final_dir)
                print(f"Archivo {file} clasificado correctamente en {final_dir}")
    except Exception as e:
        print(f"Error al clasificar archivos: {e}")

def filtrar_archivos(config):
    try:
        dir_init = config.get('PARAMETROS', 'DIR_INIT')
        dir_quarantena = config.get('PARAMETROS', 'DIR_QUARANTENA')
        extensio_filtrada = config.get('PARAMETROS', 'EXTENSIO_FILTRADA')

        for root, dirs, files in os.walk(dir_init):
            for file in files:
                if file.endswith(extensio_filtrada):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, dir_init)
                    quarantined_path = os.path.join(dir_quarantena, relative_path)
                    os.makedirs(os.path.dirname(quarantined_path), exist_ok=True)
                    shutil.move(file_path, quarantined_path)
                    print(f"Archivo {file} filtrado y movido a {quarantined_path}")
    except Exception as e:
        print(f"Error al filtrar archivos: {e}")

if __name__ == "__main__":
    menu()
