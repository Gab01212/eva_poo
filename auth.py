import hashlib
import secrets

DATABASE_USUARIOS = {
    "admin": {
        "salt": "a1b2c3d4e5",
        "hash": hashlib.sha256(("Password123!" + "a1b2c3d4e5").encode()).hexdigest()
    },
    "operador": {
        "salt": "f5e4d3c2b1",
        "hash": hashlib.sha256(("EcoTech2026*" + "f5e4d3c2b1").encode()).hexdigest()
    }
}

def verificar_credenciales(username, password):
    """
    Verifica las credenciales del usuario comparando el hash de la contraseña ingresada 
    con el salt almacenado, previniendo ataques de texto plano.
    """
    if not username or not password:
        return False, "El usuario y la contraseña no pueden estar vacíos."
    
    user_data = DATABASE_USUARIOS.get(username)
    if not user_data:
        return False, "Credenciales inválidas."
    
    intent_hash = hashlib.sha256((password + user_data["salt"]).encode()).hexdigest()
    
    if intent_hash == user_data["hash"]:
        return True, f"¡Bienvenido al sistema, {username}!"
    else:
        return False, "Credenciales inválidas."

def login_sistema():
    """Gestiona el flujo de inicio de sesión en consola con límite de intentos."""
    print("=== ECOTECH SOLUTIONS - ACCESO SEGURO ===")
    intentos = 3
    while intentos > 0:
        username = input("Ingrese usuario: ").strip()
        password = input("Ingrese contraseña: ").strip()
        
        exito, mensaje = verificar_credenciales(username, password)
        if exito:
            print(f"[✔] {mensaje}")
            return True
        else:
            intentos -= 1
            print(f"[✖] {mensaje} Intentos restantes: {intentos}")
            
    print("[!] Acceso bloqueado por exceder los intentos permitidos.")
    return false