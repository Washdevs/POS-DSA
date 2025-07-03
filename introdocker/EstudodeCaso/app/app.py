# Estudo de Caso - Deploy de App com Docker e Agente de IA Para Provisionamento de Infraestrutura com IaC
#=================================================
# ARQUIVO: app/app.py
#=================================================
# Este é o script da aplicação para criar a interface de usuário e gerenciar a interação com o Agente de IA.
import os
import streamlit as st
# Removendo CrewAI, Agent, Task, Crew, Process, OpenAI, dotenv, requests, json
# Se você não for usar CrewAI, essas importações não são necessárias.
# Se você for usar requests e json para outras coisas, mantenha.
from dotenv import load_dotenv
import requests
import json

# Carrega as variáveis de ambiente. Essencial para o Docker.
load_dotenv()

# --- Configuração da Página do Streamlit ---
st.set_page_config(
    page_title="Data Science Academy",
    page_icon=":100:",
    layout="wide"
)

st.title("🤖 Gerador de Scripts Terraform com Agente de IA")
st.markdown("""
Esta ferramenta utiliza um Agente de IA especializado para converter suas descrições de infraestrutura
em código Terraform (HCL) pronto para uso.
""")

# --- Configuração do Agente IA OpenRouter Gemini---
# A ideia aqui é criar uma função ou classe que encapsule a chamada ao OpenRouter
# para que o "agente" (que agora será uma função simples) possa usá-la.

def call_openrouter_gemini(prompt_text: str) -> str:
    """
    Faz uma chamada à API do OpenRouter usando o modelo Gemini para gerar texto.
    """
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY não configurada no arquivo .env")

    # O modelo Gemini no OpenRouter geralmente espera um formato de mensagem específico.
    # Para geração de texto simples, um único role 'user' com o conteúdo é suficiente.
    # O modelo "google/gemini-2.0-flash-exp:free" que você mencionou é um modelo experimental
    # e pode ter sido renomeado ou descontinuado.
    # Recomendo usar "google/gemini-pro" ou "google/gemini-1.5-flash" para estabilidade.
    # Verifique a lista de modelos no site do OpenRouter.
    model_name = os.getenv("OPENROUTER_MODEL_NAME", "google/gemini-1.5-flash") # Modelo padrão

    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }

    # O formato de mensagens para a API de chat é uma lista de dicionários.
    # Cada dicionário tem um 'role' (user, assistant, system) e 'content'.
    # Para o seu caso, o 'content' é o prompt do usuário.
    data = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt_text}
        ]
    })

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=data
         )
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        response_json = response.json()

        # A resposta da API do OpenRouter (e OpenAI-like) para chat completions
        # geralmente tem o texto gerado em response_json['choices'][0]['message']['content']
        if response_json and response_json.get('choices') and response_json['choices'][0].get('message'):
            return response_json['choices'][0]['message']['content']
        else:
            return "Não foi possível obter uma resposta do modelo."

    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API do OpenRouter: {e}")
        return f"Erro de conexão: {e}"
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta JSON da API do OpenRouter.")
        return "Erro ao processar a resposta da API."
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao chamar o OpenRouter: {e}")
        return f"Erro inesperado: {e}"

# Não precisamos mais de openrouter_llm como um objeto global se não estamos usando CrewAI.
# A função call_openrouter_gemini será chamada diretamente.

# --- Interface do Usuário ---
st.header("Descreva a Infraestrutura Desejada")

prompt = st.text_area(
    "Forneça um prompt claro e detalhado. Quanto mais específico você for, melhor será o resultado.",
    height=150,
    placeholder="Exemplo: Crie o código IaC com Terraform para criar um bucket S3 na AWS com o nome 'dsa-bucket-super-seguro-12345', com versionamento e criptografia SSE-S3 habilitados."
)

# O botão estará sempre habilitado, mas a chamada à API só ocorrerá se a chave estiver presente.
if st.button("Gerar Script Terraform", type="primary"):
    if prompt:
        # Verifica se a chave API está configurada antes de tentar chamar a função
        if not os.getenv("OPENROUTER_API_KEY"):
            st.error("OPENROUTER_API_KEY não configurada no arquivo .env. Por favor, configure-a.")
        else:
            with st.spinner("O Agente de IA está trabalhando... Pratique a paciência e aguarde."):
                try:
                    # A "tarefa" agora é simplesmente chamar a função que interage com o OpenRouter
                    # e passar o prompt do usuário diretamente.
                    # Você pode adicionar instruções adicionais ao prompt aqui, se desejar,
                    # para guiar o Gemini a gerar apenas o código HCL.
                    full_prompt = (
                        f"Com base na seguinte solicitação do usuário, gere um script Terraform completo e funcional. "
                        f"A saída deve ser APENAS o bloco de código HCL, sem nenhuma explicação ou texto adicional. "
                        f"O código deve ser bem formatado e pronto para ser salvo em um arquivo .tf.\n\n"
                        f"Solicitação do Usuário: '{prompt}'"
                    )
                    result = call_openrouter_gemini(full_prompt)

                    # Exibe o resultado
                    st.header("Resultado Gerado")
                    st.code(result, language='terraform')
                    st.success("Script gerado com sucesso! Obrigado DSA.")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante a execução: {e}")
    else:
        st.warning("Por favor, insira uma descrição da infraestrutura para gerar o script.")

st.markdown("---")
st.markdown("Construído com [Streamlit](https://streamlit.io/ ) na [Data Science Academy](https://www.datascienceacademy.com.br/ )")
