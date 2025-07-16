# Estudo de Caso - Deploy de App com Docker e Agente de IA Para Provisionamento de Infraestrutura com IaC
#=================================================
# ARQUIVO: app/app.py
#=================================================
# Este é o script da aplicação para criar a interface de usuário e gerenciar a interação com o Agente de IA.
import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente. Essencial para o Docker.
load_dotenv()

# --- Configuração da Página do Streamlit ---
st.set_page_config(
    page_title="Minski IAC",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown('<p class="header">Gerador de Scripts Terraform com Agente de IA</p>', unsafe_allow_html=True)
st.markdown("""
<style>
    /* Remove o padding padrão do Streamlit para a área principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    /* Estiliza o cabeçalho */
    .header {
        font-size: 5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* Estiliza o sub-cabeçalho */
    .subheader {
        font-size: 1.2rem;
        color: #808080; /* Cinza suave */
        text-align: center;
        margin-bottom: 3rem;
    }
    /* Estiliza a área de input */
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #4F8BF9;
        resize: none;
    }
    /* Estiliza o botão */
    }
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        background-color: blue;
        color: white;
        font-weight: bold;
        width: 30%;
        justify-content: center;
    }
    .stButton > button:hover {
        background-color: #3a6ecc;
    }
    /* Estiliza as abas para um visual mais limpo */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F0F2F6; /* Cor de fundo da aba ativa */
    }
    .stTextArea textarea {
        resize: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header">Mistral está Aqui</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Descreva a infraestrutura desejada de forma clara e detalhada. O agente de IA irá traduzir sua necessidade em código Terraform pronto para uso.</p>', unsafe_allow_html=True)

def get_llm():
    try:
        llm = ChatOpenAI(
            model="openrouter/mistralai/mistral-7b-instruct:free",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
    )
        return llm 
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo de linguagem: {e}. Verifique se a sua OPENROUTER_API_KEY está configurada no arquivo .env.")
    return None

openrouter_llm = get_llm()

if not openrouter_llm:
        st.stop()

# Define o Agente de IA 
def terraform_expert(openrouter_llm):
    return Agent(
        role='Especialista Sênior em Engenharia de Dados e Automação de Nuvem',
        goal='Desenvolver scripts e códigos de alta qualidade, que sejam precisos, performáticos, seguros e prontos para produção, traduzindo fielmente os requisitos do usuário em soluções técnicas.',
        backstory=(
    "Você é um Engenheiro de Dados Sênior com uma década de experiência prática, focado em automação de nuvem, engenharia de dados e desenvolvimento de software."
    "Seu conhecimento abrange profundamente os principais provedores de nuvem, incluindo AWS, Azure e Google Cloud Platform (GCP), garantindo soluções otimizadas para cada ambiente."
    "Você domina com maestria a programação e a lógica de banco de dados, sendo um especialista na criação de código limpo, modular e reutilizável."
    "Sua expertise técnica inclui HCL (Terraform), SQL, PL/SQL, Python, Shell Scripting (Linux), Docker e Docker-Compose."
    "Sua missão principal é converter requisitos de alto nível em código funcional e pronto para produção, aplicando sempre as melhores práticas de engenharia."
    "Como especialista em ETL, você possui vasta experiência em análise, tratamento e orquestração de dados com ferramentas como Apache Airflow e Apache NiFi."
    "Você tem proficiência comprovada no design, implementação e gerenciamento de arquiteturas de dados modernas, como Data Lakes, Data Warehouses e Lakehouses."
  ),
  verbose=True,
  allow_delegation=False,
  llm=openrouter_llm
)

# --- Interface do Usuário ---

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    prompt = st.text_area(
        "**Prompt para o Agente de IA:**",
        height=200,
        placeholder="Exemplo: Digite aqui oque precisa.",
        label_visibility="collapsed",
)

btn_col1, btn_col2, btn_col3 = st.columns([2, 0.5, 2])
with btn_col2:
    if st.button("Gerar Script Terraform", disabled=(not openrouter_llm)):
        if prompt:
            with st.spinner("O Agente de IA está construindo o código... Por favor, aguarde."):
                try:
                    # Define a tarefa para o agente com base no prompt do usuário
                    terraform_task = Task(
                    description=(
                     f"Como um Especialista Sênior em Engenharia de Dados e Automação de Nuvem, com uma década de experiência prática e um profundo conhecimento em AWS, Azure e GCP, você domina a programação e a lógica de banco de dados. Sua expertise técnica abrange HCL (Terraform), SQL, PL/SQL, Python, Shell Scripting (Linux), Docker e Docker-Compose. Além disso, você é um especialista em ETL, com vasta experiência em análise, tratamento e orquestração de dados usando ferramentas como Apache Airflow e Apache NiFi, e proficiência no design e gerenciamento de Data Lakes, Data Warehouses e Lakehouses."
                     f"Sua missão é traduzir a solicitação de alto nível do usuário em um script ou código completo, funcional, otimizado, seguro e pronto para produção, aplicando sempre as melhores práticas de engenharia de dados, modularidade e reusabilidade."
                     f"A saída deve ser estritamente o bloco de código na linguagem solicitada (HCL, SQL, PL/SQL, Python, Shell, Dockerfile, docker-compose.yml, etc.), sem qualquer texto explicativo, introdução ou conclusão. O código deve ser formatado corretamente e pronto para ser salvo diretamente em um arquivo apropriado para a linguagem."
                     f"Solicitação do Usuário: {prompt}"
                    ),
                    expected_output="Um bloco de código completo, validado e sem placeholders, na linguagem apropriada (HCL, SQL, PL/SQL, Python, Shell, Dockerfile, docker-compose.yml, etc.), representando uma solução de engenharia de dados pronta para produção. O código deve ser limpo, modular, seguro e otimizado, aderindo às melhores práticas da linguagem e do domínio de engenharia de dados.",
                    agent=terraform_expert(openrouter_llm)
                    )

                # Cria e executa a equipe (Crew)
                    terraform_crew = Crew(
                        agents=[terraform_expert(openrouter_llm)],
                        tasks=[terraform_task],
                        process=Process.sequential,
                    )

                # Inicia o processo e obtém o resultado
                    result = terraform_crew.kickoff()
                
                # Exibe o resultado
                    st.header("✅ Script Terraform Gerado")
                    st.code(result, language='terraform', line_numbers=True)
                    st.success("Script gerado com sucesso!")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante a execução: {e}")
        else:
            st.warning("Por favor, insira uma descrição da infraestrutura para gerar o script.")