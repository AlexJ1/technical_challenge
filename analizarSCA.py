# Instalar las librerías necesarias:
# pip install GitPython requests

import git
import requests
import os
import xml.etree.ElementTree as ET  # Para analizar archivos XML (pom.xml)

# Función para clonar el repositorio
def clonar_repositorio(url_repositorio, ruta_local):
    try:
        git.Repo.clone_from(url_repositorio, ruta_local)
        print(f"Repositorio clonado con éxito en {ruta_local}")
        return True
    except Exception as e:
        print(f"Error al clonar el repositorio: {e}")
        return False

# Función para analizar dependencias de Maven (pom.xml)
def analizar_dependencias_maven(ruta_repositorio):
    ruta_pom = os.path.join(ruta_repositorio, "pom.xml")
    if not os.path.exists(ruta_pom):
        print("Archivo pom.xml no encontrado")
        return None

    tree = ET.parse(ruta_pom)
    root = tree.getroot()
    dependencias = []

    for dep in root.findall(".//{http://maven.apache.org/POM/4.0.0}dependency"):
        groupId_el = dep.find("{http://maven.apache.org/POM/4.0.0}groupId")
        artifactId_el = dep.find("{http://maven.apache.org/POM/4.0.0}artifactId")
        version_el = dep.find("{http://maven.apache.org/POM/4.0.0}version")

        groupId = groupId_el.text if groupId_el is not None else None
        artifactId = artifactId_el.text if artifactId_el is not None else None
        version = version_el.text if version_el is not None else "No version specified"

        if groupId and artifactId:
            dependencias.append({"groupId": groupId, "artifactId": artifactId, "version": version})

    return dependencias

# Función para reportar dependencias a un API
def reportar_dependencias(dependencias, url_api, url_repositorio):
    data = {
        "repositorio": url_repositorio,
        "dependencias": dependencias
    }
    try:
        response = requests.post(url_api, json=data)
        if response.status_code == 200:
            print("Dependencias reportadas con éxito")
            return True
        else:
            print(f"Error al reportar dependencias: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error al realizar la petición al API: {e}")
        return False

# Ejemplo de uso
url_repositorio = "https://github.com/paulczar/spring-helloworld.git"  # URL del repositorio a clonar
ruta_local = "./repo_clonado"  # Ruta local donde se clonará el repositorio
url_api = "http://localhost:5000/api/reportar"  # URL del API para reportar dependencias

if clonar_repositorio(url_repositorio, ruta_local):
    dependencias = analizar_dependencias_maven(ruta_local)
    if dependencias is not None:
        reportar_dependencias(dependencias, url_api, url_repositorio)
