import json
import os

def salvar_cenarios_em_arquivo(dados_json: str, nome_arquivo: str = "cenarios_teste.json"):
    """
    Ferramenta (Tool): Salva a string JSON gerada pelo agente em um arquivo físico no disco.
    """
    try:
        # Garante que o texto recebido é um JSON válido antes de salvar
        dados_convertidos = json.loads(dados_json)
        
        # Salva o arquivo na máquina
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_convertidos, f, ensure_ascii=False, indent=4)
            
        return f"Sucesso: O arquivo '{nome_arquivo}' foi gerado e salvo na máquina."
    except Exception as e:
        return f"Erro ao salvar o arquivo: {str(e)}"