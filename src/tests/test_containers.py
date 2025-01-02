import socket
import requests
import time
import requests

def test_app_is_running():
    response = requests.get("http://app:5000")
    assert response.status_code == 200

def check_service(host, port, retries=5, delay=5):
    """Verifica si un servicio está disponible en el host y puerto especificados."""
    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout=5):
                return True
        except Exception as e:
            print(f"Error al conectar con {host}:{port} - {e}")
            time.sleep(delay)  # Espera antes de reintentar
    return False


def test_app():
    """Comprueba que el servicio de la aplicación responde correctamente."""
    url = "http://app:5000"  # Reemplaza con la URL de tu servicio Flask
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200
        print(f"Aplicación responde correctamente con código {response.status_code}.")
    except Exception as e:
        print(f"Error al comprobar la aplicación: {e}")
        assert False

def test_db():
    """Comprueba que el servicio de la base de datos está activo."""
    assert check_service("db", 5432)  # Puerto 5432 para PostgreSQL

def test_logs():
    """Comprueba que el servicio de logs está activo."""
    assert check_service("logs", 24224), "El servicio de logs no está disponible en logs:24224"

if __name__ == "__main__":
    time.sleep(5)
    test_app()
    test_db()
    test_logs()
