import xml.etree.ElementTree as ET
import requests

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def descargar_xml(url: str = URL_BCE) -> bytes:
    try:
        respuesta = requests.get(url, timeout=10)
        if respuesta.status_code == 200:
            return respuesta.content
        else:
            raise RuntimeError(
                f"Error al conectar con el BCE. Código de estado HTTP: {respuesta.status_code}"
            )
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"No fue posible conectarse con el servidor del BCE: {e}")


def parsear_xml(xml_bytes: bytes) -> tuple[str, dict[str, float]]:
    try:
        raiz = ET.fromstring(xml_bytes)
        ns = {"ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
        nodo_tiempo = raiz.find(".//ecb:Cube[@time]", ns)
        if nodo_tiempo is None:
            raise ValueError("No se encontró el nodo con la fecha en el XML del BCE.")
            
        fecha = nodo_tiempo.get("time", "Desconocida")
        tasas = {"EUR": 1.0}
        
        for nodo_moneda in nodo_tiempo.findall("ecb:Cube", ns):
            moneda = nodo_moneda.get("currency")
            rate = nodo_moneda.get("rate")
            if moneda and rate:
                tasas[moneda] = float(rate)
                
        return fecha, tasas

    except ET.ParseError as e:
        raise ValueError(f"Error al procesar la estructura XML: {e}")


def convertir_divisa(importe_texto: str, origen: str, destino: str, tasas: dict[str, float]) -> float:
    if not isinstance(importe_texto, str) or not importe_texto.strip():
        raise ValueError("El importe no puede estar vacío.")

    texto_normalizado = importe_texto.strip().replace(",", ".")
    
    try:
        importe = float(texto_normalizado)
    except ValueError:
        raise ValueError(f"El valor '{importe_texto}' no es un número válido. Introduce solo dígitos numéricos.")

    if importe < 0:
        raise ValueError("El importe a convertir no puede ser negativo.")

    if origen not in tasas:
        raise ValueError(f"La divisa de origen '{origen}' no está disponible.")
    if destino not in tasas:
        raise ValueError(f"La divisa de destino '{destino}' no está disponible.")

    tasa_origen = tasas[origen]
    tasa_destino = tasas[destino]

    return (importe / tasa_origen) * tasa_destino
