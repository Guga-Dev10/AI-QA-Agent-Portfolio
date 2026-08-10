import sys
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tools import (
    salvar_codigo_arquivo, 
    executar_comando_terminal, 
    ler_arquivo,
    listar_diretorio
)

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

instrucao_sistema = """
Você é um Arquiteto de QA Sênior especialista em BDD (Behavior-Driven Development) com Python, Behave e Playwright.
Seu objetivo é:
1. Analizar arquivos de features Gherkin (.feature).
2. Escrever a implementação dos passos (step definitions) em Python dentro da pasta 'features/steps/login_steps.py' usando Playwright.
3. Executar os testes via terminal usando o comando 'behave'.
4. SE HOUVER FALHAS: Use 'ler_arquivo' para investigar o código do step definition, corrija a lógica ou os seletores do Playwright usando 'salvar_codigo_arquivo' e re-execute até que todos os cenários passem com sucesso.
"""

print("🥒 Esquadrão BDD & Gherkin acionado! Inicializando cérebro...")

chat = client.chats.create(
    model="gemini-flash-latest", 
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[
            salvar_codigo_arquivo, 
            executar_comando_terminal, 
            ler_arquivo,
            listar_diretorio
        ],
        temperature=0.1
    )
)

prompt_usuario = (
    "Inicie um ciclo de descoberta e automação BDD totalmente autônomo com foco em evidências visuais:\n"
    "1. Acesse o site 'https://the-internet.herokuapp.com/' e navegue até a funcionalidade de 'Form Authentication'.\n"
    "2. Crie o arquivo Gherkin 'features/form_auth.feature' cobrindo cenários de sucesso e falha.\n"
    "3. Crie o arquivo 'features/steps/form_auth_steps.py' usando Playwright. ATENÇÃO: Garanta que em cada cenário "
    "   ele utilize a ferramenta de screenshot para salvar imagens na pasta 'reports/' (ex: 'reports/auth_sucesso.png' e 'reports/auth_falha.png').\n"
    "4. Execute o comando 'behave' no terminal.\n"
    "5. Se houver falhas, aplique o Self-Healing até que tudo passe.\n"
    "6. Leia a estrutura do diretório usando 'listar_diretorio'.\n"
    "7. O arquivo 'features/api_users.feature' foi criado para testar a API pública 'https://jsonplaceholder.typicode.com/users'.\n"
    "8. Crie o arquivo de implementação correspondente em 'features/steps/api_steps.py' utilizando a biblioteca 'requests' do Python "
    "   para traduzir os steps em chamadas HTTP reais (GET e POST), validando status codes e JSON.\n"
    "9. Execute o comando 'behave features/api_users.feature' no terminal para validar os testes.\n"
    "10. Se houver falhas, aplique o Self-Healing no código Python dos steps.\n"
    "1. Garanta que todas as suítes (Web Form Auth, SauceDemo e API JSONPlaceholder) executem com sucesso via 'behave'.\n"
    "2. Para os testes de API em 'features/steps/api_steps.py', atualize a implementação para que cada requisição (GET e POST) "
    "   grave um log detalhado de evidência (contendo URL, Payload, Status Code e JSON de resposta) na pasta 'reports/api_evidence.json'.\n"
    "3. Crie uma automação ou instrua o agente a compilar todas as métricas, status e caminhos das evidências visuais e de API "
    "   em um arquivo físico na raiz chamado 'reports/relatorio_executivo.md'.\n"
    "4. Entregue a confirmação de que os arquivos de evidência de API e o relatório executivo físico foram gravados com sucesso."
)

resposta = chat.send_message(prompt_usuario)

funcoes_disponiveis = {
    "salvar_codigo_arquivo": salvar_codigo_arquivo,
    "executar_comando_terminal": executar_comando_terminal,
    "ler_arquivo": ler_arquivo,
    "listar_diretorio": listar_diretorio
}

while resposta.function_calls:
    for call in resposta.function_calls:
        print(f"\n⚙️ Agente acionou a ferramenta: {call.name}")
        
        if call.name in funcoes_disponiveis:
            resultado = funcoes_disponiveis[call.name](**call.args)
        else:
            resultado = "Ferramenta desconhecida solicitada."
            
        print(f"📤 Retorno do Sistema:\n{resultado}")
        print("⏳ Pausa estratégica para Rate Limit (5s)...")
        time.sleep(5)
        
        resposta = chat.send_message([
            types.Part.from_function_response(name=call.name, response={"resultado": resultado})
        ])

print(f"\n✅ Relatório Final do Agente BDD:\n{resposta.text}")