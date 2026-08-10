import os
import subprocess
from playwright.sync_api import sync_playwright

def salvar_codigo_arquivo(codigo: str, nome_arquivo: str):
    """
    Ferramenta: Salva código ou texto gerado pelo agente em um arquivo físico no disco.
    """
    try:
        # Garante que diretórios intermediários existam se necessário
        diretorio = os.path.dirname(nome_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
            
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo)
        return f"Sucesso: O arquivo '{nome_arquivo}' foi gravado com sucesso."
    except Exception as e:
        return f"Erro ao salvar o arquivo: {str(e)}"

def executar_comando_terminal(comando: str):
    """
    Ferramenta: Executa comandos no sistema operacional (como rodar o behave) e retorna o log.
    """
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding="utf-8", 
            errors="replace"
        )
        if resultado.returncode != 0:
            return f"O comando falhou com o erro:\n{resultado.stderr}\nSaída padrão:\n{resultado.stdout}"
        return f"Comando executado com sucesso:\n{resultado.stdout}"
    except Exception as e:
        return f"Erro crítico ao executar o comando: {str(e)}"

def ler_arquivo(caminho_arquivo: str):
    """
    Ferramenta: Lê o conteúdo de qualquer arquivo no diretório para o agente analisar (Self-Healing).
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        return f"Conteúdo do arquivo '{caminho_arquivo}':\n\n{conteudo}"
    except Exception as e:
        return f"Erro ao ler o arquivo '{caminho_arquivo}': {str(e)}"

def listar_diretorio(caminho: str = "."):
    """
    Ferramenta: Lista todos os arquivos e pastas do diretório atual.
    """
    try:
        arquivos = os.listdir(caminho)
        return f"Arquivos no diretório '{caminho}': {', '.join(arquivos)}"
    except Exception as e:
        return f"Erro ao listar diretório: {str(e)}"