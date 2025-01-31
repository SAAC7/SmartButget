import requests
import json

# Identificador de la extensión Pylance en el Marketplace
EXTENSION_ID = "ms-python.vscode-pylance"

# URL para obtener los metadatos de la extensión
METADATA_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

# Headers necesarios para la solicitud
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json;api-version=6.1-preview.1"
}

# Cuerpo de la solicitud para obtener la última versión de la extensión
payload = {
    "filters": [{
        "criteria": [{
            "filterType": 7,
            "value": EXTENSION_ID
        }]
    }],
    "assetTypes": [],
    "flags": 1031
}

# Realizar la solicitud para obtener los metadatos de la extensión
response = requests.post(METADATA_URL, headers=HEADERS, data=json.dumps(payload))
data = response.json()

# Obtener el link de descarga del archivo VSIX
try:
    latest_version = data["results"][0]["extensions"][0]["versions"][0]
    for file in latest_version["files"]:
        if file["assetType"] == "Microsoft.VisualStudio.Services.VSIXPackage":
            vsix_url = file["source"]
            break
    
    # Descargar el archivo VSIX
    vsix_response = requests.get(vsix_url)
    with open("pylance.vsix", "wb") as f:
        f.write(vsix_response.content)
    
    print("Descarga completa: pylance.vsix")
except (KeyError, IndexError):
    print("No se pudo obtener la URL del VSIX. Verifica el ID de la extensión.")
