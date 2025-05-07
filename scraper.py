import requests
from bs4 import BeautifulSoup

def scrape_bifimed(principio_activo):
    try:
        url = "https://www.sanidad.gob.es/profesionales/medicamentos.do"
        payload = {"nombre": principio_activo}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
        }

        session = requests.Session()
        response = session.post(url, data=payload, headers=headers)

        if response.status_code != 200:
            return {"error": "No se pudo acceder a BIFIMED"}

        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table")
        if not tabla:
            return {"resultados": []}

        filas = tabla.find_all("tr")[1:]  # Omitir encabezado
        resultados = []

        for fila in filas:
            columnas = fila.find_all("td")
            if len(columnas) >= 5:
                resultado = {
                    "nombre_comercial": columnas[0].get_text(strip=True),
                    "principio_activo": columnas[1].get_text(strip=True),
                    "cn": columnas[2].get_text(strip=True),
                    "precio": columnas[3].get_text(strip=True),
                    "financiacion": columnas[4].get_text(strip=True)
                }
                resultados.append(resultado)

        return {"resultados": resultados}

    except Exception as e:
        return {"error": f"Excepción no controlada: {str(e)}"}
