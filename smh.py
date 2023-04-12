import requests
import openai
openai.api_key = "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"

URL = "https://api.openai.com/v1/chat/completions"

payload = {
"model": "gpt-3.5-turbo",
"messages": [
    {
        "role": "system", 
        "content": f"You are a very sarcastic chatbot, that answers short to user's questions. You are also very rude."
    },
    {
        "role": "user",
        "content": f"What time is it?"
    }
], 
"temperature" : 1.0,
"top_p":1.0,
"n" : 1,
"stream": False,
"presence_penalty":0,
"frequency_penalty":0,
}

headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {openai.api_key}"
}

response = requests.post(URL, headers=headers, json=payload, stream=False)
print(response.content['choices'][0]['message']['content'])