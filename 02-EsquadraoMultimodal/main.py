import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.tools import salvar_codigo_arquivo, executar_comando_terminal, tirar_screenshot_web

# 1. Carrega as variáveis de ambiente
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Instrução do Sistema para o Esquadrão Multimodal
instrucao_sistema = """
Você é um Arquiteto de QA Sênior e Líder de um Esquadrão de Automação Multimodal.
Você possui habilidades de visão computacional e programação.
Seu objetivo é:
1. Usar 'tirar_screenshot_web' para capturar e "ver" a interface de um site.
2. Analisar a imagem recebida para descobrir os textos, cores ou layouts presentes na tela.
3. Usar 'salvar_codigo_arquivo' para escrever um teste automatizado Playwright baseado no que você VIU.
4. Usar 'executar_comando_terminal' para rodar o script salvo.
5. Se o teste falhar, analise o erro do terminal e a imagem novamente (se necessário) para se auto-curar.
"""

print("🤖 Esquadrão Multimodal acionado! Inicializando cérebro (gemini-flash-latest)...")

# 3. Inicializa o Chat
chat = client.chats.create(
    model="gemini-flash-latest", 
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[salvar_codigo_arquivo, executar_comando_terminal, tirar_screenshot_web],
        temperature=0.1
    )
)

# 4. O Desafio Multimodal
prompt_usuario = (
    "Acesse o site 'https://example.com' usando a ferramenta de screenshot para validar a interface. "
    "Em seguida, execute um teste de carga utilizando a ferramenta 'criar_e_executar_load_test' "
    "com 5 usuários por 10 segundos, e me traga o relatório final de performance."
)

resposta = chat.send_message(prompt_usuario)

# 5. O Loop ReAct com Injeção de Imagem (Visão Computacional)
while resposta.function_calls:
    for call in resposta.function_calls:
        print(f"\n⚙️ Agente acionou a ferramenta: {call.name}")
        
        # Lista para armazenar as partes da resposta (texto + imagem)
        partes_resposta = []
        
        if call.name == "executar_comando_terminal":
            resultado = executar_comando_terminal(**call.args)
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
        elif call.name == "salvar_codigo_arquivo":
            resultado = salvar_codigo_arquivo(**call.args)
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
        elif call.name == "tirar_screenshot_web":
            # 1. Tira o print da tela
            resultado = tirar_screenshot_web(**call.args)
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
            # 2. SE A IMAGEM FOI GERADA, ANEXA ELA PARA O AGENTE VER!
            nome_imagem = call.args.get("nome_imagem", "screenshot.png")
            if os.path.exists(nome_imagem):
                print(f"📸 Injetando imagem visual '{nome_imagem}' no cérebro do Agente...")
                with open(nome_imagem, "rb") as f:
                    image_bytes = f.read()
                # Adiciona a imagem junto com a resposta da função
                partes_resposta.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                )
        else:
            resultado = "Ferramenta desconhecida."
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
        print(f"📤 Retorno do Sistema:\n{resultado}")
        print("⏳ Pausa estratégica para Rate Limit...")
        time.sleep(5)
        
        # Envia a resposta (que pode conter a IMAGEM) de volta para o agente processar
        resposta = chat.send_message(partes_resposta)

print(f"\n✅ Relatório Final do Esquadrão Multimodal:\n{resposta.text}")