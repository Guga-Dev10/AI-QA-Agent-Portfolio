import pytest
from playwright.sync_api import Page, expect

def test_validate_example_domain_interface(page: Page):
    # 1. Navegar até o site https://example.com
    page.goto("https://example.com")
    
    # 2. Validar o título da página
    expect(page).to_have_title("Example Domain")
    
    # 3. Validar o cabeçalho h1
    h1 = page.locator("h1")
    expect(h1).to_be_visible()
    expect(h1).to_have_text("Example Domain")
    
    # 4. Validar o conteúdo do parágrafo principal
    paragraph = page.locator("p").first
    expect(paragraph).to_contain_text("documentation examples")
    
    # 5. Validar o link de mais informações
    link = page.locator("a")
    expect(link).to_be_visible()
    expect(link).to_have_text("Learn more")
    expect(link).to_have_attribute("href", "https://iana.org/domains/example")
