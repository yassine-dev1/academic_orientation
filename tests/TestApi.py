from google import genai

client = genai.Client(api_key="AIzaSyDxC7FSq7NQKbJsh6BpRWsT6C1Nqg1M2zY")

# Lister les modèles disponibles
for model in client.models.list():
    print(f"- {model.name}: {model.supported_actions}")