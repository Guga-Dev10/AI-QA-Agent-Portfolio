# -*- coding: utf-8 -*-
import os
import json
import requests
from behave import given, when, then

EVIDENCE_FILE = "reports/api_evidence.json"

def registrar_evidencia(url, method, payload, status_code, response_json):
    os.makedirs(os.path.dirname(EVIDENCE_FILE), exist_ok=True)
    evidencias = []
    if os.path.exists(EVIDENCE_FILE):
        try:
            with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
                evidencias = json.load(f)
                if not isinstance(evidencias, list):
                    evidencias = [evidencias]
        except Exception:
            evidencias = []

    nova_evidencia = {
        "method": method,
        "url": url,
        "payload": payload,
        "status_code": status_code,
        "response_body": response_json
    }
    evidencias.append(nova_evidencia)

    with open(EVIDENCE_FILE, "w", encoding="utf-8") as f:
        json.dump(evidencias, f, indent=2, ensure_ascii=False)

@given('que a URL base da API é "{url_base}"')
def step_define_base_url(context, url_base):
    context.base_url = url_base

@when('eu envio uma requisição GET para "{endpoint}"')
def step_requisicao_get(context, endpoint):
    url = context.base_url + endpoint
    response = requests.get(url)
    context.response = response
    
    try:
        resp_json = response.json()
    except Exception:
        resp_json = response.text

    registrar_evidencia(
        url=url,
        method="GET",
        payload=None,
        status_code=response.status_code,
        response_json=resp_json
    )

@then('o código de status HTTP da resposta deve ser {status_code:d}')
def step_valida_status_code(context, status_code):
    assert context.response.status_code == status_code, \
        f"Esperado status {status_code}, mas recebeu {context.response.status_code}"

@then('a resposta da API deve conter uma lista de usuários')
def step_valida_lista_usuarios(context):
    data = context.response.json()
    assert isinstance(data, list), f"Esperado uma lista na resposta, recebeu {type(data)}"
    assert len(data) > 0, "A lista de usuários veio vazia"

@when('eu envio uma requisição POST para "{endpoint}" com o seguinte corpo:')
def step_requisicao_post(context, endpoint):
    url = context.base_url + endpoint
    row = context.table[0]
    payload = {
        "name": row["name"],
        "username": row["username"],
        "email": row["email"]
    }
    response = requests.post(url, json=payload)
    context.response = response

    try:
        resp_json = response.json()
    except Exception:
        resp_json = response.text

    registrar_evidencia(
        url=url,
        method="POST",
        payload=payload,
        status_code=response.status_code,
        response_json=resp_json
    )

@then('a resposta da API deve conter o id gerado')
def step_valida_id_gerado(context):
    data = context.response.json()
    assert "id" in data, f"Campo 'id' não encontrado na resposta: {data}"
