import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import salvar_codigo_arquivo, executar_comando_terminal

# 1. Carrega as variáveis de ambiente
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Instrução do Sistema para o Esquadrão
instrucao_sistema = """
Você é um Arquiteto de QA Sênior e Líder de um Esquadrão de Automação.
Seu objetivo é:
1. Analisar o pedido do usuário para criar um teste automatizado usando Playwright em Python.
2. Usar a ferramenta 'salvar_codigo_arquivo' para salvar o script gerado com o nome 'teste_automatico.py'.
3. Usar a ferramenta 'executar_comando_terminal' para rodar o script salvo ('python teste_automatico.py').
4. Se houver falha, analisar o erro, corrigir o código e salvar novamente até o teste passar com sucesso.
"""

print("🤖 Esquadrão de QA acionado! Inicializando o modelo gemini-2.0-flash...")

# 3. Inicializa o Chat COM O NOME FIXO (Ignorando a lista bugada do Google)
chat = client.chats.create(
    model="gemini-flash-latest", 
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[salvar_codigo_arquivo, executar_comando_terminal],
        temperature=0.1
    )
)

# 4. Desafio inicial para o Esquadrão
prompt_usuario = (
    "Crie um teste automatizado em Playwright (Python) que acesse o site 'https://example.com', "
    "valide se o título da página é exatamente 'Example Domain', salve o script em 'teste_automatico.py', "
    "execute-o no terminal e reporte o resultado."
)

resposta = chat.send_message(prompt_usuario)

# 5. O Loop ReAct
while resposta.function_calls:
    for call in resposta.function_calls:
        print(f"\n⚙️ Agente acionou a ferramenta: {call.name}")
        
        if call.name == "executar_comando_terminal":
            resultado = executar_comando_terminal(**call.args)
        elif call.name == "salvar_codigo_arquivo":
            resultado = salvar_codigo_arquivo(**call.args)
        else:
            resultado = "Ferramenta desconhecida."
            
        print(f"📤 Retorno da Execução:\n{resultado}")
        print("⏳ Pausa de segurança...")
        time.sleep(5)
        
        resposta = chat.send_message(
            types.Part.from_function_response(
                name=call.name,
                response={"resultado": resultado}
            )
        )

print(f"\n✅ Relatório Final do Esquadrão:\n{resposta.text}")