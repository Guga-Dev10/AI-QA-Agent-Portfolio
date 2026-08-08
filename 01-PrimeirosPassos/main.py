import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import salvar_cenarios_em_arquivo # Importamos a nossa ferramenta

# 1. Carrega as variáveis de ambiente
load_dotenv()

# 2. Inicializa o cliente
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Definimos a Regra Mestra (System Instruction)
instrucao_sistema = """
Você é um Engenheiro de QA Autônomo. 
Sua tarefa é analisar a solicitação do usuário, gerar cenários de teste estruturados 
e utilizar obrigatoriamente a ferramenta 'salvar_cenarios_em_arquivo' para persistir os dados.
"""

print("O Agente está pensando e processando a tarefa...")

# 4. Enviamos a requisição passando a função diretamente na lista de 'tools'
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Gere os 3 cenários de teste mais críticos para um campo de "Senha" no momento de cadastro e salve-os em um arquivo.',
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        # Aqui é onde a mágica acontece: registramos a função Python para a IA
        tools=[salvar_cenarios_em_arquivo],
    )
)

# 5. O Agente executou a ferramenta? Vamos verificar a resposta
print("\n🤖 Resposta do Agente:")
if response.function_calls:
    print("O Agente decidiu chamar a ferramenta de forma autônoma!")
    for call in response.function_calls:
        print(f"Função acionada: {call.name}")
        print(f"Argumentos passados pela IA: {call.args}")
else:
    print(response.text)