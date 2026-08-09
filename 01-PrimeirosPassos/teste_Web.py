# teste_web.py
from playwright.sync_api import sync_playwright

def testar_titulo_site():
    print("Iniciando o navegador...")
    with sync_playwright() as p:
        # Lança o navegador Chromium em modo invisível (headless=True)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Acessando o site Example.com...")
        page.goto("https://example.com")
        
        titulo_real = page.title()
        print(f"Título encontrado: {titulo_real}")
        
        # ERRO PROPOSITAL: O título correto do site é 'Example Domain' (em inglês)
        # Estamos afirmando erroneamente que é em português para forçar a falha do teste
        assert titulo_real == "Example Domain", f"Erro: O título esperado não confere. Título real: {titulo_real}"
        
        print("Teste Web passou com sucesso!")
        browser.close()

if __name__ == "__main__":
    testar_titulo_site()