import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import salvar_cenarios_em_arquivo, executar_comando_terminal

# 1. Carrega o ambiente
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. A Regra Mestra: Focada em persistência e auto-cura
instrucao_sistema = """
Você é um Engenheiro de QA Sênior e um Agente Autônomo de Self-Healing.
Sua missão é:
1. Roda o script 'teste_alvo.py' no terminal.
2. Se falhar, você deve analisar o erro, reescrever o código correto usando 'salvar_cenarios_em_arquivo' (sobrescrevendo o 'teste_alvo.py'), e executar de novo.
3. Repita isso até que o teste passe com sucesso. Só pare quando não houver mais erros.
"""

# 3. Criação do Chat (Isso dá MEMÓRIA ao agente)
chat = client.chats.create(
    model='gemini-flash-latest', # <-- ALTERADO PARA O CURINGA
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[salvar_cenarios_em_arquivo, executar_comando_terminal],
        temperature=0.1
    )
)

print("🚀 Iniciando o Ciclo de Self-Healing...")

# 4. O primeiro comando que dispara o ciclo
resposta = chat.send_message('Inicie o ciclo: execute "teste_alvo.py" e conserte-o se necessário.')

# 5. O Coração do Agente: O Loop ReAct (Reason -> Act -> Observe)
while resposta.function_calls:
    for call in resposta.function_calls:
        print(f"\n🧠 IA decidiu usar a ferramenta: {call.name}")
        
        # Executa a ferramenta escolhida
        if call.name == "executar_comando_terminal":
            resultado = executar_comando_terminal(**call.args)
        elif call.name == "salvar_cenarios_em_arquivo":
            # Força salvar no formato .py em vez de .json para corrigir o script
            nome_arquivo = call.args.get("nome_arquivo", "teste_alvo.py")
            texto_codigo = call.args.get("dados_json", "")
            
            # Uma adaptação rápida na ferramenta para salvar código Python
            try:
                with open(nome_arquivo, "w", encoding="utf-8") as f:
                    f.write(texto_codigo)
                resultado = f"Sucesso: Arquivo '{nome_arquivo}' atualizado."
            except Exception as e:
                resultado = f"Erro ao salvar: {str(e)}"
                
        print(f"📤 Resultado do Sistema (devolvido para a IA):\n{resultado}")
        
        # O PULO DO GATO: Devolvemos o resultado para a IA pensar no próximo passo!
        resposta = chat.send_message(
            types.Part.from_function_response(
                name=call.name,
                response={"resultado": resultado}
            )
        )

# Quando o `while` termina (a IA parou de pedir ferramentas), ela nos dá o relatório final.
print(f"\n✅ Conclusão do Agente:\n{resposta.text}")