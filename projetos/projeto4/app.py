import streamlit as st
from llama_index.llms.groq import Groq
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.agent.workflow import ToolCallResult, AgentStream
import asyncio
import pandas as pd
import tempfile
from deep_translator import GoogleTranslator
import sys
import io
from dotenv import load_dotenv
load_dotenv()

# Função para leitura e indexação de documentos
def load_and_index(file_path):
    docs = SimpleDirectoryReader(input_files=[file_path]).load_data()

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
    return docs, index

# Função para resumo
def summarize_doc(content):
    template = """
    Você é um analista financeiro experiente.
    Ao ler o relatório a seguir, extraia insights financeiros relevantes e explique-os de forma clara e didática, como se estivesse apresentando para gestores não especialistas.
    Utilize linguagem acessível e destaque pontos importantes sobre lucros, despesas, fluxo de caixa, riscos e oportunidades.
    Retorne o texto em linguagem natural e com caracteres que possuem em um teclado comum, sem caracteres ou símbolos LaTex.
    Resuma de forma breve e objetiva. Retorne a mensagem direto, sem apresentações no início.

    Conteúdo do documento:
    '{}'
    """
    prompt = template.format(content)
    output = llm.complete(prompt)
    return output.text.strip()

# Tradução
def translate(text, source_lang='pt', target_lang='en'):
    return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

def query_spreadsheet(query):
    return str(pandas_query_engine.query(query))


def format_res(res, return_thinking=False):
  res = res.strip()

  if return_thinking:
    res = res.replace("<think>", "[thinking...] ")
    res = res.replace("</think>", "\n---\n")

  else:
    if "</think>" in res:
      res = res.split("</think>")[-1].strip()

  return res

def show_res(res):
    from IPython.display import Markdown
    display(Markdown(res))

# Função Async
async def run_agent(query):
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        handler = st.session_state.agent.run(query)

        async for event in handler.stream_events():
            if isinstance(event, ToolCallResult):
                print(
                    f"Call {event.tool_name} with args {event.tool_kwargs}\nReturned: {event.tool_output}"
                )
            elif isinstance(event, AgentStream):
                print(event.delta, end="", flush=True)

        response = await handler
        formatted = format_res(str(response), return_thinking=True)

    finally:
        sys.stdout = old_stdout

    logs = mystdout.getvalue()
    return formatted, logs

## Configuração Streamlit
st.set_page_config(page_title="Análise de Documentos Financeiros", page_icon="💵", layout="wide")
st.title("Análise de Documentos Financeiros 💵")

if 'docs_list' not in st.session_state:
  st.session_state.docs_list = None
if 'agent' not in st.session_state:
  st.session_state.agent = None
if 'summary' not in st.session_state:
  st.session_state.summary = None
if 'df' not in st.session_state:
  st.session_state.df = None

model_option = st.sidebar.selectbox("Escolha o modelo:", ["Gemini", "Groq / Qwen"]) # Sidebar
#model_option = "Gemini"

if model_option == "Gemini":
  llm = GoogleGenAI(model = "models/gemini-3.5-flash-lite")
else:
  llm = Groq(model = "qwen/qwen3.8-27b", temperature = 0.1)

Settings.llm = llm

upload = st.sidebar.file_uploader("Envie um documento (PDF ou CSV):", type=["pdf", "csv"])

if upload:
  if st.session_state.docs_list != upload:
    with st.spinner("Processando documento..."):
      suffix = ".pdf" if upload.type == "application/pdf" else ".csv"
      with tempfile.NamedTemporaryFile(delete = False, suffix = suffix) as tmp:
        tmp.write(upload.read())
        path = tmp.name

      if upload.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(path)
        st.session_state.df['date'] = pd.to_datetime(st.session_state.df['date'])
        pandas_query_engine = PandasQueryEngine(df=st.session_state.df, llm=llm, verbose=True)
        tool = FunctionTool.from_defaults(fn=query_spreadsheet)
      else:
        st.session_state.df = None
        docs, index = load_and_index(path)
        tool = QueryEngineTool.from_defaults(
            query_engine=index.as_query_engine(similarity_top_k=3, llm=llm),
            name="doc_search",
            description=(
              "Provides information about the company's finances. Use whenever user asks for something"
          ),
        )

      agent = FunctionAgent(tools=[tool], llm=llm)

      st.session_state.agent = agent
      st.session_state.docs_list = upload

      if upload.name.endswith(".pdf"):
        content = "\n".join([doc.text for doc in docs])
        content = content[:200000]
      else:
        content = st.session_state.df.head(500).to_string()
      st.session_state.summary = summarize_doc(content)

    st.toast("Documento enviado com sucesso", icon="✅")

  col1, col2 = st.columns([2, 2])

  with col1:
    user_query = st.text_input("Digite sua pergunta:", key="user_query")
    translate_option = st.checkbox("Ativar tradução", value = False)
    send = st.button("Enviar", type = "primary")

    if send and user_query:
      query = translate(user_query, 'pt', 'en') if translate_option else user_query

      # atualização
      response, agent_logs = asyncio.run(run_agent(query))

      result = translate(str(response), 'en', 'pt') if translate_option else str(response)
      st.divider()
      st.markdown("#### Resposta")
      st.markdown(result)
      with st.expander("Etapas do agente (log)"):
        st.code(agent_logs)

  with col2:
    if st.session_state.df is not None:
      st.dataframe(st.session_state.df)
    with st.expander("💡 Insights rápidos - Resumo do Documento", expanded=True):
      st.write(st.session_state.summary)
else:
  st.info("Por favor, envie um arquivo para continuar.")