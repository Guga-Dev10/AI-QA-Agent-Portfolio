import json
import os
import subprocess

def salvar_cenarios_em_arquivo(dados_json: str, nome_arquivo: str = "cenarios_teste.json"):
    """
    Ferramenta (Tool): Salva a string JSON gerada pelo agente em um arquivo físico no disco.
    """
    try:
        dados_convertidos = json.loads(dados_json)
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_convertidos, f, ensure_ascii=False, indent=4)
        return f"Sucesso: O arquivo '{nome_arquivo}' foi gerado e salvo na máquina."
    except Exception as e:
        return f"Erro ao salvar o arquivo: {str(e)}"

def executar_comando_terminal(comando: str):
    """
    Ferramenta (Tool): Executa um comando no terminal do Windows tratando a codificação de caracteres.
    """
    try:
        # No Windows, usamos errors='replace' para evitar que caracteres especiais quebrem o agente
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding="cp1252", 
            errors="replace"
        )
        
        if resultado.returncode != 0:
            return f"O comando falhou com o erro:\n{resultado.stderr}"
            
        return f"Comando executado com sucesso:\n{resultado.stdout}"
    except Exception as e:
        return f"Erro crítico ao executar o comando: {str(e)}"