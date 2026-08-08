import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
# Importamos as duas ferramentas que construímos
from tools import salvar_cenarios_em_arquivo, executar_comando_terminal

# 1. Carrega as variáveis de ambiente
load_dotenv()

# 2. Inicializa o cliente
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Definimos a Regra Mestra (System Instruction)
instrucao_sistema = """
Você é um Engenheiro de QA Autônomo e Sênior. 
Analise a solicitação do usuário e decida qual ferramenta utilizar para cumprir o objetivo:
- Use 'salvar_cenarios_em_arquivo' se precisar persistir dados estruturados (JSON).
- Use 'executar_comando_terminal' se precisar rodar comandos no sistema operacional.
"""

print("O Agente está analisando a tarefa e escolhendo as ferramentas...")

# 4. Enviamos a requisição passando as duas ferramentas na lista 'tools'
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Liste os arquivos da pasta atual rodando o comando "dir" no terminal e salve o resultado em um arquivo chamado relatorio_diretorio.json.',
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[salvar_cenarios_em_arquivo, executar_comando_terminal],
    )
)

# 5. Tratamento de Múltiplas Chamadas de Ferramentas (Function Calling)
print("\n🤖 Resposta do Agente:")
if response.function_calls:
    print(f"O Agente decidiu acionar {len(response.function_calls)} ferramenta(s) de forma autônoma!\n")
    
    for call in response.function_calls:
        print(f"👉 Função escolhida: {call.name}")
        print(f"📥 Argumentos enviados pela IA: {call.args}")
        
        # Executando a função dinamicamente com base na escolha da IA
        if call.name == "executar_comando_terminal":
            resultado = executar_comando_terminal(**call.args)
            print(f"📤 Resultado da Execução:\n{resultado}\n")
            
        elif call.name == "salvar_cenarios_em_arquivo":
            resultado = salvar_cenarios_em_arquivo(**call.args)
            print(f"📤 Resultado da Execução:\n{resultado}\n")
else:
    print(response.text)