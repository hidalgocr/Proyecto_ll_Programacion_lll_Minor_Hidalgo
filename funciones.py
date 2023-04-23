import re
import json


# Funcion que lo que hace es validarme la fecha con una libreria
def validarFecha(fecha):
    patron = r'^\d{2}/\d{2}/\d{4}$'
    return bool(re.match(patron, fecha))


#Funcion para realizar el calculo de porcentaje de computadoras que se encuentra en el json
def calcular_porcentaje():
    # cargamos el JSON desde un archivo o una cadena, por ejemplo:
    with open('inventario_laboratorio_2023.json') as f:
        data = json.load(f)

    # calculamos la cantidad total de computadoras
    total_computadoras = sum([l['Computadoras'] for l in data['matriz']])

    # calculamos el porcentaje de cada laboratorio y lo agregamos a una lista
    resultados = []
    for l in data['matriz']:
        porcentaje = (l['Computadoras'] / total_computadoras) * 100
        resultados.append(f"El laboratorio {l['nombre']} tiene un porcentaje de {porcentaje}% de computadoras")

    # devolvemos una cadena con todos los resultados
    return '\n'.join(resultados)


# Calcular la media de los elementos de todos los laboratorios
def calcular_promedio_elementos():
    with open('inventario_laboratorio_2023.json') as f:
        data = json.load(f)

    elementos = ["Computadoras", "teclados", "mouses", "parlantes", "Arduinos UNO"]
    promedios = {}

    # Calcular el promedio de la cantidad de elementos en cada categoría en todos los laboratorios
    for elemento in elementos:
        total_elementos = sum([l[elemento] for l in data['matriz']])
        promedio_elementos = total_elementos / len(data['matriz'])
        promedios[elemento] = promedio_elementos
    
    return promedios


# Calcular el porcentaje de elementos de todos los laboratorios
def calcular_porcentaje_equipos():
    # cargamos el JSON desde un archivo o una cadena, por ejemplo:
    with open('inventario_laboratorio_2023.json') as f:
        data = json.load(f)

    # calculamos los totales de cada tipo de dispositivo
    total_computadoras = sum([l['Computadoras'] for l in data['matriz']])
    total_impresoras = sum([l['Impresora HP'] for l in data['matriz']])
    total_arduinos = sum([l['Arduinos UNO'] for l in data['matriz']])
    total_teclados = sum([l['teclados'] for l in data['matriz']])
    total_mouses = sum([l['mouses'] for l in data['matriz']])
    total_parlantes = sum([l['parlantes'] for l in data['matriz']])

    # creamos una cadena con los resultados
    resultadosporcentaje = ""
    for l in data['matriz']:
        porcentaje_computadoras = (l['Computadoras'] / total_computadoras) * 100
        porcentaje_impresoras = (l['Impresora HP'] / total_impresoras) * 100
        porcentaje_arduinos = (l['Arduinos UNO'] / total_arduinos) * 100
        porcentaje_teclados = (l['teclados'] / total_teclados) * 100
        porcentaje_mouses = (l['mouses'] / total_mouses) * 100
        porcentaje_parlantes = (l['parlantes'] / total_parlantes) * 100

        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_computadoras:.2f}% de computadoras\n"
        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_impresoras:.2f}% de impresoras HP\n"
        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_arduinos:.2f}% de Arduinos UNO\n"
        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_teclados:.2f}% de teclados\n"
        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_mouses:.2f}% de mouses\n"
        resultadosporcentaje += f"El laboratorio {l['nombre']} ({l['Numero']}) tiene un porcentaje de {porcentaje_parlantes:.2f}% de parlantes\n"

    return resultadosporcentaje


    




