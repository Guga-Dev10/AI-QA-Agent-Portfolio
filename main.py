import os
from dotenv import load_dotenv
from google import genai
from google.genai import types # NOVO: Importamos a biblioteca de tipos e configurações

# 1. Carrega as variáveis de ambiente
load_dotenv()

# 2. Inicializa o cliente
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Definimos a Regra Mestra (System Instruction)
instrucao_sistema = """
Você é um Engenheiro de QA Autônomo. 
Sua tarefa é analisar a pergunta do usuário e devolver uma lista de cenários de teste.
Você DEVE responder ESTRITAMENTE em formato JSON. Não adicione saudações ou textos extras.
"""

print("Solicitando cenários de teste estruturados em JSON...")

# 4. Enviamos a requisição com a configuração ativada
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Quais são os 3 cenários de teste mais críticos para um campo de "Senha" no momento de cadastro?',
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        response_mime_type="application/json" # Obrigamos a API a travar a saída em JSON
    )
)

# 5. Imprime o resultado bruto
print("\n🤖 Dados Estruturados Recebidos:")
print(response.text)