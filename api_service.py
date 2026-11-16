import requests
import re

def validar_entrada_texto(prompt, tipo="general"):
    """Valida y sanitiza las entradas del usuario según el contexto."""
    while True:
        valor = input(prompt).strip()
        if not valor:
            print("[!] El campo no puede estar vacío. Intente nuevamente.")
            continue
        
        if tipo == "moneda":
            if re.match(r"^[A-Za-z]{3}$", valor):
                return valor.upper()
            print("[!] Formato de moneda inválido. Debe ser de 3 letras (ej. USD, CLP).")
        elif tipo == "coordenada":
            try:
                return float(valor)
            except ValueError:
                print("[!] Ingrese un valor numérico válido.")
        else:
            return valor

def consultar_clima(lat, lon):
    """
    Consume la API de Open-Meteo para obtener información climática en tiempo real.
    Aplica manejo robusto de errores de conexión y códigos HTTP.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        print(f"[*] Consultando servicio meteorológico en coordenadas ({lat}, {lon})...")
        response = requests.get(url, timeout=10)
        
        # Validación de códigos de estado HTTP
        if response.status_code == 200:
            data = response.json()
            clima_actual = data.get("current_weather", {})
            return {
                "estado": "Exitoso",
                "temperatura": clima_actual.get("temperature"),
                "velocidad_viento": clima_actual.get("windspeed"),
                "condicion_codigo": clima_actual.get("weathercode")
            }
        elif response.status_code == 404:
            return {"estado": "Error", "mensaje": "Recurso climático no encontrado (404)."}
        elif response.status_code == 500:
            return {"estado": "Error", "mensaje": "Error interno en el servidor del proveedor externo (500)."}
        else:
            return {"estado": "Error", "mensaje": f"Respuesta inesperada del servidor HTTP: {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"estado": "Error", "mensaje": "La solicitud al servicio de clima ha expirado (Timeout)."}
    except requests.exceptions.ConnectionError:
        return {"estado": "Error", "mensaje": "Fallo de conexión a red. Verifique su acceso a internet."}
    except Exception as e:
        return {"estado": "Error", "mensaje": "Ocurrió un error inesperado al procesar la solicitud externa."}

def consultar_tipo_cambio(moneda_base):
    """
    Consume una API de indicadores económicos y tipos de cambio internacionales.
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{moneda_base}"
    
    try:
        print(f"[*] Consultando tasas de cambio para la moneda: {moneda_base}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "estado": "Exitoso",
                "base": data.get("base"),
                "rates": data.get("rates", {})
            }
        elif response.status_code == 404:
            return {"estado": "Error", "mensaje": f"Moneda base '{moneda_base}' no encontrada (404)."}
        else:
            return {"estado": "Error", "mensaje": f"Error HTTP al consultar tasas: {response.status_code}"}
            
    except requests.exceptions.RequestException:
        return {"estado": "Error", "mensaje": "Error de conexión al servicio de divisas."}