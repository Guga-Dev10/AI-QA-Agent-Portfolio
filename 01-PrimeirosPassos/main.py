import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import salvar_cenarios_em_arquivo, executar_comando_terminal

# 1. Carrega as variáveis de ambiente
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Instrução do Sistema focado em Self-Healing (Auto-Cura)
instrucao_sistema = """
Você é um Engenheiro de QA Sênior e um Agente Autônomo de Self-Healing.
Sua missão é rodar o script de teste 'teste_alvo.py' usando a ferramenta de terminal.
Se o teste falhar (retornar erro), você DEVE analisar o erro, reescrever/consertar o arquivo 'teste_alvo.py' 
(você pode usar a ferramenta de salvamento ou comandos) e executar novamente até que o teste passe com sucesso.
"""

print("🚀 Iniciando o Ciclo ReAct / Self-Healing do Agente...")

# 3. Prompt inicial para o Agente começar a trabalhar
prompt_inicial = 'Execute o arquivo "teste_alvo.py" no terminal. Se falhar, analise o erro, corrija o código do teste e execute novamente até passar.'

response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents=prompt_inicial,
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[salvar_cenarios_em_arquivo, executar_comando_terminal],
    )
)

# 4. Processamento do ciclo de ferramentas
print("\n🤖 Resposta Inicial do Agente:")
if response.function_calls:
    for call in response.function_calls:
        print(f"👉 Ferramenta acionada: {call.name}")
        print(f"📥 Argumentos: {call.args}")
        
        # Executa a primeira ferramenta escolhida pela IA
        if call.name == "executar_comando_terminal":
            resultado = executar_comando_terminal(**call.args)
            print(f"📤 Resultado:\n{resultado}")
        elif call.name == "salvar_cenarios_em_arquivo":
            resultado = salvar_cenarios_em_arquivo(**call.args)
            print(f"📤 Resultado:\n{resultado}")
else:
    print(response.text)