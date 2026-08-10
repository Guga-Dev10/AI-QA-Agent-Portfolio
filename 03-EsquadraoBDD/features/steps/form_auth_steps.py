# -*- coding: utf-8 -*-
import os
from behave import given, when, then

@given('que o usuário acessa a página de login do Herokuapp')
def step_acessa_login_herokuapp(context):
    context.page.goto("https://the-internet.herokuapp.com/login")

@when('ele preenche o usuário "{usuario}" e a senha "{senha}" no Herokuapp')
def step_preenche_credenciais_herokuapp(context, usuario, senha):
    context.page.fill('#username', usuario)
    context.page.fill('#password', senha)

@when('clica no botão de login do Herokuapp')
def step_clica_login_herokuapp(context):
    context.page.click('button[type="submit"]')

@then('ele deve ver a mensagem de sucesso "{mensagem}"')
def step_valida_mensagem_sucesso_herokuapp(context, mensagem):
    flash_element = context.page.locator('#flash')
    assert flash_element.is_visible(), "Mensagem flash não encontrada na página"
    flash_text = flash_element.text_content()
    assert mensagem in flash_text, f"Esperado '{mensagem}' no texto, mas obteve '{flash_text}'"

@then('um screenshot de sucesso do Herokuapp deve ser salvo em "{caminho_arquivo}"')
def step_salva_screenshot_sucesso(context, caminho_arquivo):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    context.page.screenshot(path=caminho_arquivo)
    assert os.path.exists(caminho_arquivo), f"Arquivo de screenshot não encontrado em {caminho_arquivo}"

@then('ele deve ver a mensagem de erro no Herokuapp "{mensagem}"')
def step_valida_mensagem_erro_herokuapp(context, mensagem):
    flash_element = context.page.locator('#flash')
    assert flash_element.is_visible(), "Mensagem flash não encontrada na página"
    flash_text = flash_element.text_content()
    assert mensagem in flash_text, f"Esperado '{mensagem}' no texto, mas obteve '{flash_text}'"

@then('um screenshot de falha do Herokuapp deve ser salvo em "{caminho_arquivo}"')
def step_salva_screenshot_falha(context, caminho_arquivo):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    context.page.screenshot(path=caminho_arquivo)
    assert os.path.exists(caminho_arquivo), f"Arquivo de screenshot não encontrado em {caminho_arquivo}"
