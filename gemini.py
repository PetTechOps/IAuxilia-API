import google.generativeai as genai

def gemini_connect():

 # Para criar uma API_KEY https://aistudio.google.com/app/u/0/apikey
  GOOGLE_API_KEY = ""

  genai.configure(api_key=GOOGLE_API_KEY)

  generation_config = {
    "candidate_count": 1,
    "temperature": 0.5
  }

  safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
  )

  conversa = model.start_chat(history=[])
  return conversa





