# language: pt
Funcionalidade: Validação de Contrato e Comportamento da API de Usuários
  Como um Engenheiro de Qualidade
  Eu quero testar os endpoints da API JSONPlaceholder
  Para garantir que os dados e status HTTP estão corretos

  Cenário: Consultar a lista de usuários com sucesso
    Dado que a API de usuários "https://jsonplaceholder.typicode.com/users" está disponível
    Quando eu envio uma requisição GET para o endpoint
    Então o código de status HTTP da resposta deve ser 200
    E o contrato JSON retornado deve conter uma lista com usuários

  Cenário: Criar um novo usuário com sucesso (POST)
    Dado que a API de usuários "https://jsonplaceholder.typicode.com/users" está disponível
    Quando eu envio uma requisição POST com o nome "Agente QA" e o email "agente@qa.com"
    Então o código de status HTTP da resposta deve ser 201
    E o corpo da resposta deve retornar o ID do usuário criado