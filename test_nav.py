import requests
import json

def test_chat_nav():
    url = "http://localhost:7842/chat"
    payload = {
        "message": "¿Cómo registro una pausa?",
        "session_id": "test-session-2",
        "current_screen": "Principal"
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

if __name__ == "__main__":
    test_chat_nav()
