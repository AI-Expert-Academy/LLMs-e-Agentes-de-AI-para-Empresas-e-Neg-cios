from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

# models/gemini-2.0-flash não está mais disponível
llm_google = GoogleGenAI(model="models/gemini-3.5-flash-lite")
res = llm_google.complete(prompt="Olá, tudo legal?")
print(res.text)    