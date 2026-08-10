from playwright.sync_api import sync_playwright

def test_titulo_principal_example_domain():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Valida se o título principal (h1) está presente e contém "Example Domain"
        h1_element = page.locator("h1")
        assert h1_element.is_visible(), "O elemento H1 não está visível na página."
        
        titulo_texto = h1_element.inner_text()
        assert titulo_texto == "Example Domain", f"Esperado 'Example Domain', porém foi encontrado '{titulo_texto}'"
        
        browser.close()

if __name__ == "__main__":
    test_titulo_principal_example_domain()
    print("Sucesso: O título principal 'Example Domain' foi validado corretamente na página!")
