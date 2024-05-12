import configparser
import os
import shutil

#menu
def menu_configuracion():
    config = None
    while True:
        print("\n--- Menú de Configuración ---")
        print("1. Crear Nuevo Archivo de Configuración")
        print("2. Cargar Configuración")
        print("3. Ver Configuración")
        print("4. Cambiar Parámetros")
        print("5. Crear directorios")
        print("6. Clasificar archivos")
        print("0. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            config = crear_configuracion()
        elif opcion == '2':
            config = cargar_configuracion()
        elif opcion == '3':
            if config:
                ver_configuracion(config)
            else:
                print("No se ha cargado ninguna configuración.")
        elif opcion == '4':
            if config:
                config = cambiar_parametros(config)
            else:
                print("No se ha cargado ninguna configuración.")
        elif opcion == '5':
            if config:
                crear_directorios(config)
            else:
                print("No se ha cargado ninguna configuración.")
        elif opcion == '6':
            if config:
                clasificar_archivos(config)
            else:
                print("No se ha cargado ninguna configuración")
        elif opcion == '0':
            break
        else:
            print("Opción no válida.")


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
    try:
        config.read(archivo_config)
        print("¡Configuración cargada")
        return config
    except FileNotFoundError:
        print("El archivo de configuración no existe.")
        return None
    except configparser.Error as e:
        print("Error al leer el archivo de configuración:", e)
        return None


def cambiar_parametros(config):
    seccion = 'PARAMETROS'  # Sección fija para los parámetros
    parametros = config[seccion]  # Obtener todos los parámetros de la sección
    print("Parámetros disponibles para modificar:")
    for parametro, valor in parametros.items():
        print(f"{parametro}: {valor}")  # Mostrar el nombre del parámetro y su valor actual
    
    parametro = input("Introduce el nombre del parámetro que quieres cambiar: ")
    if parametro in parametros:
        valor_actual = parametros[parametro]
        print(f"El valor actual de {parametro} es: {valor_actual}")  # Mostrar el valor actual del parámetro
        nuevo_valor = input("Introduce el nuevo valor: ")
        config.set(seccion, parametro, nuevo_valor)
        print("¡Valor cambiado con éxito!")
        
        # Guardar la configuración actualizada en el archivo
        archivo_nuevo = input("Introduce el nombre del archivo de configuración a actualizar: ")
        confirmacion = input(f"¿Estás seguro que quieres guardar la configuración en {archivo_nuevo}? (S/N): ")
        if confirmacion.upper() == 'S':
            with open(archivo_nuevo, 'w') as configfile:
                config.write(configfile)
            print("¡Configuración guardada con éxito!")
    else:
        print("El parámetro ingresado no es válido.")
    
    return config



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
        with open(archivo_nuevo, 'w') as configfile:
            config.write(configfile)
        print("¡Configuración guardada con éxito!")


def crear_directorios(config):
    dir_dst = config.get('PARAMETROS', 'DIR_DST')
    iniciales = input("Pon tus iniciales para dar nombre a los directorios: ")
    try:
        if not os.path.exists(dir_dst):
            os.makedirs(dir_dst)
            print(f"Directorio principal {dir_dst} creado correctamente.")
        for user in [f"{iniciales}1", f"{iniciales}2", f"{iniciales}3"]:
            user_dir = os.path.join(dir_dst, user)
            for size in ['petit', 'mitja', 'gran']:
                size_dir = os.path.join(user_dir, size)
                if not os.path.exists(size_dir):
                    os.makedirs(size_dir)
                    print(f"Directorio {size_dir} creado correctamente para el usuario {user}.")
    except Exception as e:
        print(f"Error al crear directorios: {e}")

def clasificar_archivos(config):
    dir_init = config.get('PARAMETROS', 'DIR_INIT')
    dir_dst = config.get('PARAMETROS', 'DIR_DST')
    mida_petita = int(config.get('PARAMETROS', 'MIDA_PETITA')) * 1024  # Convertir MB a bytes
    mida_mitjana = int(config.get('PARAMETROS', 'MIDA_MITJANA')) * 1024  # Convertir MB a bytes
    
    try:
        for root, dirs, files in os.walk(dir_init):
            for file in files:
                file_path = os.path.join(root, file)
                # Obtener información del archivo
                file_size = os.path.getsize(file_path)
                file_owner = os.stat(file_path).st_uid

                # Clasificar por tamaño
                if file_size < mida_petita:
                    size_dir = 'petit'
                elif mida_petita < file_size < mida_mitjana:
                    size_dir = 'mitja'
                else:
                    size_dir = 'gran'

                # Clasificar por propietario
                owner_dir = str(file_owner)

                # Crear directorio final
                final_dir = os.path.join(dir_dst, owner_dir, size_dir)

                # Crear directorios si no existen
                if not os.path.exists(final_dir):
                    os.makedirs(final_dir)

                # Mover archivo al directorio final
                shutil.move(file_path, final_dir)

                print(f"Archivo {file} clasificado correctamente en {final_dir}")

    except Exception as e:
        print(f"Error al clasificar archivos: {e}")



#ejecutar
if __name__ == "__main__":
    config = None
    menu_configuracion()
