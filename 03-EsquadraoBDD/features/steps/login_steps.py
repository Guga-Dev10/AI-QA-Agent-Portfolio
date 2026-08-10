# -*- coding: utf-8 -*-
import os
from behave import given, when, then

@given('que o usuário acessa a página de login do SauceDemo')
def step_acessa_login(context):
    context.page.goto("https://www.saucedemo.com")

@when('ele preenche o usuário "{usuario}" e a senha "{senha}"')
def step_preenche_credenciais(context, usuario, senha):
    context.page.fill('input[data-test="username"]', usuario)
    context.page.fill('input[data-test="password"]', senha)

@when('clica no botão de login')
def step_clica_login(context):
    context.page.click('input[data-test="login-button"]')

@then('ele deve ser redirecionado para a página de inventário com sucesso')
def step_valida_inventario(context):
    context.page.wait_for_url("**/inventory.html")
    assert "inventory.html" in context.page.url, f"URL esperada com 'inventory.html', mas recebeu '{context.page.url}'"
    assert context.page.is_visible('.inventory_list'), "A lista de inventário não está visível"

@then('um screenshot da tela logada deve ser salvo')
def step_salva_screenshot(context):
    os.makedirs("reports", exist_ok=True)
    screenshot_path = "reports/screenshot_login.png"
    context.page.screenshot(path=screenshot_path)
    assert os.path.exists(screenshot_path), f"Screenshot não encontrado em {screenshot_path}"

@then('uma mensagem de erro de autenticação deve ser exibida')
def step_valida_mensagem_erro(context):
    error_element = context.page.locator('[data-test="error"]')
    assert error_element.is_visible(), "A mensagem de erro não está visível"
    error_text = error_element.text_content()
    assert "Username and password do not match" in error_text or "Epic sadface" in error_text, f"Texto de erro inesperado: {error_text}"
