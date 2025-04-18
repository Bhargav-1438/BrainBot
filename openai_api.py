import os
import requests

# Ensure the API key is loaded from environment variables
API_KEY = os.environ.get("OPENROUTER_API_KEY")  # Save this in your .env or system environment variables

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # Model choice; you can change this if needed
        "messages": [
            {"role": "system", "content": "You are BrainBot, a smart assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("Error:", response.status_code, response.text)
            return "Sorry, I couldn't process that. Try again later."
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return "Sorry, there was an issue with the request. Please try again later."
