import json
import os
import subprocess

def salvar_codigo_arquivo(codigo: str, nome_arquivo: str = "teste_gerado.py"):
    """
    Ferramenta: Salva código Python gerado pelo agente em um arquivo físico no disco.
    """
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo)
        return f"Sucesso: O arquivo '{nome_arquivo}' foi gravado com sucesso."
    except Exception as e:
        return f"Erro ao salvar o arquivo: {str(e)}"

def executar_comando_terminal(comando: str):
    """
    Ferramenta: Executa comandos no sistema operacional (como rodar testes) e retorna o log.
    """
    try:
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