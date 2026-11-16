import json
import os
from datetime import datetime

ARCHIVO_PERSISTENCIA = "ecotech_operaciones_cache.json"

def guardar_registro_local(tipo, datos):
    """Persiste los datos obtenidos de las APIs en un archivo JSON local."""
    registro = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "contenido": datos
    }
    
    historial = []
    if os.path.exists(ARCHIVO_PERSISTENCIA):
        try:
            with open(ARCHIVO_PERSISTENCIA, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except json.JSONDecodeError:
            historial = []
            
    historial.append(registro)
    
    try:
        with open(ARCHIVO_PERSISTENCIA, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)
        print(f"[✔] Datos persistidos exitosamente en '{ARCHIVO_PERSISTENCIA}'.")
    except Exception:
        print("[!] Error al guardar los datos localmente.")