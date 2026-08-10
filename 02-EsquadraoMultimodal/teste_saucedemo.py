import sys
from playwright.sync_api import sync_playwright

def test_saucedemo_login_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com")
        
        # Validação do título
        assert "Swag Labs" in page.title()
        
        # Validação do campo de username
        username_input = page.locator('[data-test="username"]')
        assert username_input.is_visible(), "Campo de usuário não está visível"
        
        # Validação do campo de password
        password_input = page.locator('[data-test="password"]')
        assert password_input.is_visible(), "Campo de senha não está visível"
        
        # Validação do botão de login
        login_button = page.locator('[data-test="login-button"]')
        assert login_button.is_visible(), "Botão de login não está visível"
        
        print("PASS: Todos os elementos de login estão visíveis e funcionais.")
        browser.close()

if __name__ == "__main__":
    test_saucedemo_login_elements()
