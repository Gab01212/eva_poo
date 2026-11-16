from auth import login_sistema
from api_service import consultar_clima, consultar_tipo_cambio, validar_entrada_texto
from database import guardar_registro_local

def menu_principal():
    print("\n=============================================")
    print("   ECOTECH SOLUTIONS - GESTIÓN OPERATIVA     ")
    print("=============================================")
    print("1. Consultar Planificación Climática de Proyecto")
    print("2. Consultar Tipo de Cambio para Pagos Internacionales")
    print("3. Salir del Sistema")

def main():
    # Paso 2: Autenticación obligatoria previa al uso
    if not login_sistema():
        return

    while True:
        menu_principal()
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\n--- MÓDULO CLIMÁTICO PARA PROYECTOS ---")
            print("Ejemplos de coordenadas: Santiago (-33.44, -70.66) | Concepción (-36.82, -73.04)")
            lat = validar_entrada_texto("Ingrese Latitud: ", "coordenada")
            lon = validar_entrada_texto("Ingrese Longitud: ", "coordenada")
            
            resultado = consultar_clima(lat, lon)
            if resultado["estado"] == "Exitoso":
                print("\n[RESULTADO CLIMÁTICO]")
                print(f" Temperatura actual: {resultado['temperatura']} °C")
                print(f" Velocidad del viento: {resultado['velocidad_viento']} km/h")
                guardar_registro_local("Clima", resultado)
            else:
                print(f"\n[!] Error controlado: {resultado['mensaje']}")
                
        elif opcion == "2":
            print("\n--- MÓDULO DE PAGOS INTERNACIONALES ---")
            moneda = validar_entrada_texto("Ingrese código de moneda base (ej. USD, EUR): ", "moneda")
            
            resultado = consultar_tipo_cambio(moneda)
            if resultado["estado"] == "Exitoso":
                print(f"\n[RESULTADO TASA DE CAMBIO - Base: {resultado['base']}]")
                rates = resultado["rates"]
                # Mostramos algunas monedas de referencia relevante
                for m in ["CLP", "ARS", "BRL", "EUR"]:
                    if m in rates:
                        print(f" 1 {resultado['base']} = {rates[m]} {m}")
                guardar_registro_local("Divisas", resultado)
            else:
                print(f"\n[!] Error controlado: {resultado['mensaje']}")
                
        elif opcion == "3":
            print("\n[✔] Saliendo del sistema de EcoTech Solutions. ¡Hasta luego!")
            break
        else:
            print("[!] Opción inválida. Por favor, seleccione un número entre 1 y 3.")

if __name__ == "__main__":
    main()