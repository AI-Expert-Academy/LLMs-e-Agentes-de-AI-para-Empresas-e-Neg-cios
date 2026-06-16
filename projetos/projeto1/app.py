import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

## conexão com LLM
id_model = 'llama-3.3-70b-versatile'

llm = ChatGroq(
    model = id_model,
    temperature = 0.7,
    max_tokens = None,
    timeout = None,
    max_retries = 2
)

## função de geração
def llm_generate(llm, prompt):
    template = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva"),
        ("human", "{prompt}")
    ])

    chain = template | llm | StrOutputParser()

    res = chain.invoke({"prompt": prompt})
    return res

st.set_page_config(page_title = "Gerador de conteúdo 🤖", page_icon="🤖")
st.title("Gerador de conteúdo")

# Campos do formulário
topic = st.text_input("Tema:", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")
platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])
cta = st.text_input("Call to Action:", placeholder="Ex: Clique para aproveitar a promoção!")
hashtags = st.checkbox("Retornar Hashtags")
keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")

if st.button("Gerar conteúdo"):
    cta_text = (
        f"Incluir uma chamada para ação clara utilizando o seguinte texto: {cta}."
        if cta
        else "Não inclua uma chamada para ação."
    )

    hashtags_text = (
        f"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."
    )

    seo_text = (
        f"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""
    )
    
    prompt = f"""
        Escreva um texto com SEO otimizado sobre o tema '{topic}'.
        Retorne em sua resposta apenas o texto final.
        - Onde será publicado: {platform}.
        - Tom: {tone}.
        - Público-alvo: {audience}.
        - Comprimento: {length}.
        - {cta_text}
        - {hashtags_text}
        {seo_text}
    """

    try:
        res = llm_generate(llm, prompt)
        st.markdown(res)
    except Exception as e:
        print("Ocorreu um erro ao gerar o conteúdo:", str(e))