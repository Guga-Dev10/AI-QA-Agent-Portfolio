import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.tools import (
    salvar_codigo_arquivo, 
    executar_comando_terminal, 
    tirar_screenshot_web, 
    criar_e_executar_load_test,
    ler_arquivo,
    listar_diretorio
)

# 1. Carrega as variáveis de ambiente
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Instrução do Sistema (Cérebro com foco em Self-Healing)
instrucao_sistema = """
Você é um Arquiteto de QA Sênior e um Engenheiro de Software Autônomo com capacidades de Self-Healing.
Seu objetivo é:
1. Executar testes, validações visuais e de performance.
2. SE ALGO FALHAR (erro no terminal, erro de sintaxe, AssertionError): Você DEVE usar a ferramenta 'ler_arquivo' para investigar o código-fonte do arquivo que causou o erro.
3. Após ler e encontrar o erro, você DEVE reescrever o arquivo corrigido usando 'salvar_codigo_arquivo' e executar o terminal novamente para confirmar a cura.
4. Use 'listar_diretorio' se precisar saber quais arquivos existem no projeto.
Nunca desista no primeiro erro. Leia o código, entenda o erro do terminal, corrija o arquivo e re-execute.
"""

print("🤖 Esquadrão Multimodal & Self-Healing acionado! Inicializando cérebro...")

# 3. Inicializa o Chat com as 6 ferramentas
chat = client.chats.create(
    model="gemini-flash-latest", 
    config=types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        tools=[
            salvar_codigo_arquivo, 
            executar_comando_terminal, 
            tirar_screenshot_web, 
            criar_e_executar_load_test,
            ler_arquivo,
            listar_diretorio
        ],
        temperature=0.1
    )
)

# 4. O Desafio de Self-Healing
prompt_usuario = (
    "Vamos realizar uma auditoria avançada em um novo ambiente de testes.\n"
    "1. Acesse o site de e-commerce de testes 'https://www.saucedemo.com'.\n"
    "2. Tire um screenshot da tela de login usando 'tirar_screenshot_web' para validarmos visualmente a interface inicial.\n"
    "3. Crie um script Playwright chamado 'teste_saucedemo.py' que valide a presença do campo de login e do botão de acesso.\n"
    "4. Execute um teste de carga avançado usando 'criar_e_executar_load_test' contra 'https://www.saucedemo.com' "
    "com 15 usuários simultâneos por 15 segundos, simulando navegação em múltiplas rotas.\n"
    "5. Entregue um relatório consolidado com a análise visual, o status do teste E2E e as métricas de performance do Locust."
)

resposta = chat.send_message(prompt_usuario)

# Dicionário dinâmico para rodar qualquer função sem precisar de dezenas de IFs
funcoes_disponiveis = {
    "salvar_codigo_arquivo": salvar_codigo_arquivo,
    "executar_comando_terminal": executar_comando_terminal,
    "tirar_screenshot_web": tirar_screenshot_web,
    "criar_e_executar_load_test": criar_e_executar_load_test,
    "ler_arquivo": ler_arquivo,
    "listar_diretorio": listar_diretorio
}

# 5. O Loop ReAct
while resposta.function_calls:
    for call in resposta.function_calls:
        print(f"\n⚙️ Agente acionou a ferramenta: {call.name}")
        
        partes_resposta = []
        
        if call.name in funcoes_disponiveis:
            funcao_selecionada = funcoes_disponiveis[call.name]
            
            try:
                # Executa a função passando os argumentos recebidos da IA
                resultado = funcao_selecionada(**call.args)
            except Exception as e:
                resultado = f"Erro estrutural ao rodar a ferramenta localmente: {str(e)}"
            
            # Adiciona o resultado textual para a IA
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
            # Se for a ferramenta visual, anexa a imagem física também
            if call.name == "tirar_screenshot_web":
                nome_imagem = call.args.get("nome_imagem", "screenshot.png")
                if os.path.exists(nome_imagem):
                    print(f"📸 Injetando imagem visual '{nome_imagem}' no cérebro do Agente...")
                    with open(nome_imagem, "rb") as f:
                        image_bytes = f.read()
                    partes_resposta.append(
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    )
        else:
            resultado = "Ferramenta desconhecida solicitada."
            partes_resposta.append(types.Part.from_function_response(name=call.name, response={"resultado": resultado}))
            
        print(f"📤 Retorno do Sistema:\n{resultado}")
        print("⏳ Pausa estratégica para Rate Limit (5s)...")
        time.sleep(5)
        
        # Devolve os dados (texto/imagem/erro) para o Agente continuar o fluxo
        resposta = chat.send_message(partes_resposta)

print(f"\n✅ Relatório Final do Agente:\n{resposta.text}")