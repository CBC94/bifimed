import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sanidad.gob.es"

def scrape_bifimed(principio_activo):
    try:
        url = f"{BASE_URL}/profesionales/medicamentos.do"
        payload = {"nombre": principio_activo}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
        }

        session = requests.Session()
        response = session.post(url, data=payload, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table")
        if not tabla:
            return {"resultados": []}

        filas = tabla.find_all("tr")[1:]
        resultados = []

        for fila in filas:
            columnas = fila.find_all("td")
            if len(columnas) >= 6:
                # Extraer link de "Más información"
                enlace_relativo = columnas[5].find("a")["href"] if columnas[5].find("a") else None
                url_detalle = f"{BASE_URL}/profesionales/{enlace_relativo}" if enlace_relativo else None

                # Valores base de la fila
                resultado = {
                    "nombre_comercial": columnas[2].get_text(strip=True),
                    "principio_activo": columnas[1].get_text(strip=True),
                    "cn": columnas[0].get_text(strip=True),
                    "financiacion": columnas[3].get_text(strip=True),
                    "tipo": columnas[4].get_text(strip=True),
                }

                # Si hay detalle, entrar a la URL y extraer info adicional
                if url_detalle:
                    detalle = scrape_detalle(url_detalle, headers, session)
                    resultado.update(detalle)

                resultados.append(resultado)

        return {"resultados": resultados}

    except Exception as e:
        return {"error": f"Excepción no controlada: {str(e)}"}

def scrape_detalle(url, headers, session):
    try:
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        def buscar_texto(selector):
            celda = soup.find("td", string=selector)
            if celda and celda.find_next_sibling("td"):
                return celda.find_next_sibling("td").get_text(strip=True)
            return "No disponible"

        return {
            "indicacion_autorizada": buscar_texto("Indicación autorizada"),
            "estado_expediente": buscar_texto("Situación expediente indicación"),
            "resolucion_financiacion": buscar_texto("Resolución expediente de financiación indicación"),
        }

    except Exception as e:
        return {
            "indicacion_autorizada": f"Error: {str(e)}",
            "estado_expediente": "Error",
            "resolucion_financiacion": "Error"
        }
