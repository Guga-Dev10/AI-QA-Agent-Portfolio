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
