# language: pt
Funcionalidade: Autenticação via Formulário no Herokuapp
  Como um usuário do site
  Eu quero me autenticar no formulário
  Para acessar a área restrita do sistema

  Cenário: Autenticação com credenciais válidas
    Dado que o usuário acessa a página de login do Herokuapp
    Quando ele preenche o usuário "tomsmith" e a senha "SuperSecretPassword!" no Herokuapp
    E clica no botão de login do Herokuapp
    Então ele deve ver a mensagem de sucesso "You logged into a secure area!"
    E um screenshot de sucesso do Herokuapp deve ser salvo em "reports/auth_sucesso.png"

  Cenário: Autenticação com credenciais inválidas
    Dado que o usuário acessa a página de login do Herokuapp
    Quando ele preenche o usuário "usuario_invalido" e a senha "senha_invalida" no Herokuapp
    E clica no botão de login do Herokuapp
    Então ele deve ver a mensagem de erro no Herokuapp "Your username is invalid!"
    E um screenshot de falha do Herokuapp deve ser salvo em "reports/auth_falha.png"
