# language: pt
Funcionalidade: Testes de API na rota de Usuários do JSONPlaceholder
  Como um analista de testes de API
  Eu quero realizar requisições HTTP GET e POST na API de usuários
  Para garantir que os endpoints respondem corretamente e salvar evidências de teste

  Cenário: Consultar a lista de usuários via GET
    Dado que a URL base da API é "https://jsonplaceholder.typicode.com"
    Quando eu envio uma requisição GET para "/users"
    Então o código de status HTTP da resposta deve ser 200
    E a resposta da API deve conter uma lista de usuários

  Cenário: Criar um novo usuário via POST
    Dado que a URL base da API é "https://jsonplaceholder.typicode.com"
    Quando eu envio uma requisição POST para "/users" com o seguinte corpo:
      | name          | username | email                |
      | Mario Andrade | mandrade | mario@teste.com.br   |
    Então o código de status HTTP da resposta deve ser 201
    E a resposta da API deve conter o id gerado
