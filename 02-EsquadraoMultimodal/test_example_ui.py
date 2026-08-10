import pytest
from playwright.sync_api import Page, expect

def test_validate_example_domain_interface(page: Page):
    page.goto("https://example.com")
    
    # Validar título e heading visual
    expect(page).to_have_title("Example Domain")
    heading = page.locator("h1")
    expect(heading).to_be_visible()
    expect(heading).to_have_text("Example Domain")
    
    # Validar link de mais informações
    more_info_link = page.locator("a")
    expect(more_info_link).to_be_visible()
    expect(more_info_link).to_have_attribute("href", "https://www.iana.org/domains/example")
