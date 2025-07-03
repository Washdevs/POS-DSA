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

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header">Mistral está Aqui</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Descreva a infraestrutura desejada de forma clara e detalhada. O agente de IA irá traduzir sua necessidade em código Terraform pronto para uso.</p>', unsafe_allow_html=True)

@st.cache_resource
def get_llm():
    try:
        llm = ChatOpenAI(
            model="openrouter/mistralai/mistral-7b-instruct:free",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
    )
        return llm 
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo de linguagem: {e}. Verifique se a sua OPENAI_API_KEY está configurada no arquivo .env.")
    return None

openrouter_llm = get_llm()

# Define o Agente de IA 
@st.cache_resource
def terraform_expert(openrouter_llm):
    return Agent(
        role='Especialista Sênior em Infraestrutura como Código',
        goal='Criar scripts Terraform precisos, eficientes e seguros com base nos requisitos do usuário.',
        backstory=(
    "Você é um Engenheiro de DataOps altamente experiente com uma década de experiência na automação "
    "de provisionamento de infraestrutura na nuvem usando Terraform. Você tem um profundo conhecimento "
    "dos provedores de nuvem como AWS, Azure e GCP, e é mestre em escrever código HCL (HashiCorp "
    "Configuration Language) limpo, modular e reutilizável. Sua missão é traduzir "
    "descrições de alto nível da infraestrutura desejada em código Terraform pronto para produção."
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
        placeholder="Exemplo: Crie o código IaC com Terraform para criar um bucket S3 na AWS com o nome 'dsa-bucket-super-seguro-12345', com versionamento e criptografia SSE-S3 habilitados.",
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
                            f"Com base na seguinte solicitação do usuário, gere um script Terraform completo e funcional. "
                            f"A saída deve ser APENAS o bloco de código HCL, sem nenhuma explicação ou texto adicional. "
                            f"O código deve ser bem formatado e pronto para ser salvo em um arquivo .tf.\n\n"
                            f"Solicitação do Usuário: '{prompt}'"
                        ),
                        expected_output='Um bloco de código contendo o script Terraform (HCL). O código deve ser completo e não deve conter placeholders como "sua_configuracao_aqui".',
                        agent=terraform_expert
                    )   

                # Cria e executa a equipe (Crew)
                    terraform_crew = Crew(
                        agents=[terraform_expert],
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
