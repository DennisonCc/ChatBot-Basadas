import requests
import json

def test_chat():
    url = "http://localhost:7842/chat"
    payload = {
        "message": "¿Quiénes son los empleados registrados?",
        "session_id": "test-session",
        "current_screen": "Personal"
    }
    
    print(f"Enviando mensaje: {payload['message']}")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("\nRespuesta del Chatbot:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\nError: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Detalle: {e.response.text}")

if __name__ == "__main__":
    test_chat()
