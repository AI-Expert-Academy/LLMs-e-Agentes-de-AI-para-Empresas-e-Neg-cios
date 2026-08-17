import streamlit as st
from datetime import datetime
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# Configurações iniciais
st.set_page_config(page_title="Gerador de Exercícios", layout="centered", page_icon="📖")
st.title("Gerador de Exercícios 📖")

# Função para carregar o modelo
def load_llm(id_model, temperature):
    return ChatGroq(
        model=id_model,
        temperature=temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

# Função para formatar a resposta da LLM
def format_res(res, return_thinking=False):
    res = res.strip()
    if return_thinking:
        res = res.replace("<think>", "[pensando...] ")
        res = res.replace("</think>", "\n---\n")
    else:
        if "</think>" in res:
            res = res.split("</think>")[-1].strip()
    return res

# Função para criar o prompt
def build_prompt(topic, quantity, level, interests):
    prompt = f"""
Você é um tutor especialista em {topic}. Gere {quantity} exercícios para um aluno de nível {level}.
{f"- Apenas caso faça sentido no contexto, adapte de forma natural e sutil os enunciados dos exercícios para refletir a afinidade do aluno com o tema '{interests}'." if interests else ""}
- Formato dos exercícios: Múltipla escolha com 4 opções.
- Incluir explicação passo a passo e o raciocínio usado para chegar à resposta.
- Não use LaTeX e nenhuma sequência iniciada por barra invertida (como \frac, \sqrt, ou similares). Use apenas linguagem natural e símbolos comuns do teclado.

Exemplo de estrutura:
1. [Enunciado]
   a) Opção 1
   b) Opção 2
   c) Opção 3
   d) Opção 4
   Resposta: [Letra correta]
   Explicação: [Passo a passo detalhado]
"""
    return prompt

st.sidebar.header("Configurações do modelo")
id_model = st.sidebar.text_input("ID do modelo", value = "llama-3.3-70b-versatile")
temperature = st.sidebar.slider("Temperatura", 0.1, 1.5, 0.7, 0.1)

with st.form("formulario"):
  level = st.selectbox("Nível", ['Iniciante', 'Intermediário', 'Avançado'], index = 1)
  topic = st.text_input("Tema", placeholder="Matemática, Inglês, Física, etc.")
  quantity = st.slider("Quantidade de Exercícios", 1, 10, 5)
  interests = st.text_input("Interesses ou Preferências", placeholder="Ex: Filmes, Música, etc.")
  gerar = st.form_submit_button("Gerar Exercícios")

if gerar:
  with st.spinner("Gerando exercícios..."):
    llm = load_llm(id_model, temperature)
    prompt = build_prompt(topic, quantity, level, interests)
    res = llm.invoke(prompt)
    res_formatado = format_res(res.content, return_thinking=True)
    st.markdown(res_formatado)
