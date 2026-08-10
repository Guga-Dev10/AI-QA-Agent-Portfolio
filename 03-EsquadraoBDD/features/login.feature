# language: pt
Funcionalidade: Autenticação de Usuário no E-commerce
  Como um cliente da loja virtual
  Eu quero fazer o login no sistema
  Para que eu possa acessar o catálogo de produtos

  Cenário: Login com credenciais válidas
    Dado que o usuário acessa a página de login do SauceDemo
    Quando ele preenche o usuário "standard_user" e a senha "secret_sauce"
    E clica no botão de login
    Então ele deve ser redirecionado para a página de inventário com sucesso
    E um screenshot da tela logada deve ser salvo

  Cenário: Tentativa de login com senha incorreta
    Dado que o usuário acessa a página de login do SauceDemo
    Quando ele preenche o usuário "standard_user" e a senha "senha_errada"
    E clica no botão de login
    Então uma mensagem de erro de autenticação deve ser exibida