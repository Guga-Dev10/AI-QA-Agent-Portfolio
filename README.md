# 🤖 AI QA Agent - Autonomous Test Engineering

## 🎯 Visão Geral
Este projeto implementa um **Agente Autônomo de Quality Assurance (QA)** utilizando a arquitetura ReAct (Reasoning + Acting). O objetivo do sistema não é apenas gerar código de teste, mas atuar como um engenheiro virtual capaz de ler requisitos, escrever scripts de automação, executá-los no terminal e corrigir o próprio código (Self-Healing) com base em logs de falhas.

## 📐 Arquitetura do Sistema
O projeto adota uma abordagem híbrida e desacoplada, separando o "cérebro" de tomada de decisão da "linha de montagem" de execução de testes.

*   **Orquestração e Lógica (O Cérebro):** Python. Escolhido pela maturidade do ecossistema de IA e facilidade de integração com frameworks de agentes (ex: LangChain, CrewAI).
*   **Automação e Execução (As Mãos):** TypeScript + Playwright. Padrão ouro da indústria moderna para testes E2E, garantindo estabilidade via *auto-wait* e operando na mesma linguagem do frontend moderno.
*   **LLM Engine (O Motor Cognitivo):** Google Gemini (via API). O sistema foi desenhado de forma agnóstica a provedores, permitindo a troca rápida para Claude, OpenAI ou modelos locais (Ollama) alterando apenas variáveis de ambiente.

## ⚙️ O Ciclo de Vida do Agente (ReAct Flow)
1. **Thought:** O agente analisa a User Story.
2. **Action:** Utiliza a ferramenta `File Tool` para gerar o script TypeScript.
3. **Observation:** Aciona a `Terminal Tool` para executar `npx playwright test`.
4. **Feedback Loop:** Analisa os logs de saída (stdout/stderr). Se houver falha, corrige o script e repete o ciclo até a aprovação total.

## ⚖️ Decisões de Engenharia (Trade-offs)
*   **Python vs. Java/C# para IA:** Redução extrema de *boilerplate*. Python permite iterar o ciclo de raciocínio da IA com menos sobrecarga estrutural.
*   **Playwright vs. Selenium:** Eliminação de *flaky tests* causados por lentidão de rede, fornecendo feedback determinístico e confiável para a IA não entrar em loops falsos de correção.

## 📐 Arquitetura do Sistema
O projeto adota uma abordagem desacoplada e agnóstica, separando rigorosamente o cérebro cognitivo da camada de execução operacional.

*   **Orquestração e Cérebro (O Core):** Python + Google GenAI SDK. Escolhido pela alta velocidade de integração com modelos de linguagem modernos e suporte nativo a chamadas de ferramentas (*Function Calling*).
*   **Motor Cognitivo (LLM):** Google Gemini 3.5 Flash. Selecionado por sua alta performance em baixa latência e eficiência computacional.
*   **Camada de Execução (As Ferramentas / Tools):** Funções nativas em Python customizadas para manipulação segura de I/O em disco e execução de subprocessos do sistema operacional com tratamento robusto de codificação de caracteres (`cp1252/UTF-8`).

## ⚙️ Funcionalidades e Capacidades Atuais (Tool Use)
O agente possui autonomia para selecionar e acionar ferramentas de forma independente com base na intenção do usuário:
1. **`salvar_cenarios_em_arquivo`**: Converte e persiste dados gerados pela IA em arquivos estruturados (JSON) de forma segura no disco local.
2. **`executar_comando_terminal`**: Dispara comandos no terminal do sistema operacional (como inspeção de diretórios ou futuros testes de regressão), capturando logs de sucesso ou falhas (stdout/stderr).

## 🛡️ Segurança e Boas Práticas (DevSecOps)
*   **Gerenciamento de Segredos:** O projeto utiliza variáveis de ambiente (`.env`) para isolar chaves de API, impedindo o vazamento de credenciais no código-fonte.
*   **Controle de Versão Limpo:** O arquivo `.gitignore` é configurado para excluir ambientes virtuais (`venv/`), arquivos de cache e artefatos gerados dinamicamente em tempo de execução (`*.json`), mantendo o repositório focado exclusivamente no código-estrutura.

## 🧬 Ciclo ReAct e Self-Healing (Auto-Cura)
O grande diferencial desta arquitetura é a sua capacidade de operar em um **Loop ReAct (Reason + Act)** acoplado à memória de sessão contínua. 
Quando o agente recebe a tarefa de executar um script de teste:
1. Ele aciona o terminal e roda o script (ex: `teste_alvo.py`).
2. Se o interpretador retornar um erro (Stacktrace), o agente **analisa a causa raiz**.
3. Ele reescreve o código-fonte corrigindo o erro sem intervenção humana.
4. Ele reexecuta o teste repetidamente até atingir o *status* de sucesso, finalizando com a entrega de um relatório gerencial de execução