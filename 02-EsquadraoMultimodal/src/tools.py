import subprocess
from playwright.sync_api import sync_playwright

def salvar_codigo_arquivo(codigo: str, nome_arquivo: str = "teste_automatico.py"):
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

def tirar_screenshot_web(url: str, nome_imagem: str = "screenshot.png"):
    """
    Ferramenta: Acessa uma URL via Playwright e salva uma captura de tela (screenshot) em imagem.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=nome_imagem)
            browser.close()
        return f"Sucesso: Screenshot capturado e salvo como '{nome_imagem}'."
    except Exception as e:
        return f"Erro ao capturar screenshot: {str(e)}"

def criar_e_executar_load_test(url_alvo: str, usuarios: int = 10, tempo_segundos: int = 15):
    """
    Ferramenta: Cria um script de teste de carga usando Locust, executa-o contra uma URL
    e retorna o relatório de performance (RPS, falhas, latência).
    """
    codigo_locust = f"""
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def index_page(self):
        self.client.get("/")
"""
    
    try:
        with open("locustfile.py", "w", encoding="utf-8") as f:
            f.write(codigo_locust)
    except Exception as e:
        return f"Erro ao criar o arquivo locustfile.py: {str(e)}"

    comando = f"locust -f locustfile.py --host={url_alvo} --users {usuarios} --spawn-rate 2 --run-time {tempo_segundos}s --headless"
    
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding="utf-8", 
            errors="replace"
        )
        relatorio = resultado.stdout if resultado.stdout else resultado.stderr
        return f"Relatório de Teste de Carga Executado com Sucesso:\n{relatorio}"
    except Exception as e:
        return f"Erro ao executar o teste de carga com Locust: {str(e)}"