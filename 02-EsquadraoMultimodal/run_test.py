import sys
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # Validations
        title = page.title()
        assert title == "Example Domain", f"Expected 'Example Domain', got '{title}'"
        
        h1_text = page.locator("h1").inner_text()
        assert h1_text == "Example Domain", f"Expected 'Example Domain', got '{h1_text}'"
        
        p_text = page.locator("p").first.inner_text()
        assert "documentation examples" in p_text, f"Text not in paragraph: {p_text}"
        
        link = page.locator("a")
        link_text = link.inner_text()
        link_href = link.get_attribute("href")
        assert link_text == "Learn more", f"Link text mismatch: {link_text}"
        assert link_href == "https://iana.org/domains/example", f"Href mismatch: {link_href}"
        
        print("[SUCESSO] TODOS OS TESTES DE INTERFACE PASSARAM COM SUCESSO!")
        print(f"- Titulo: '{title}'")
        print(f"- Cabecalho H1: '{h1_text}'")
        print(f"- Texto do Paragrafo: '{p_text}'")
        print(f"- Link: '{link_text}' -> '{link_href}'")
        
        browser.close()

if __name__ == "__main__":
    run_test()
