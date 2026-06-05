# EduTrack AI

[![Python version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

## 🌟 Overview

EduTrack AI é uma aplicação web construída em Python com Streamlit, projetada para transformar a gestão acadêmica de alunos. Em vez de apenas ser um registro de tarefas, a ferramenta fornece um **Dashboard de Dados interativo e analítico**, permitindo que o estudante visualize, acompanhe e compreenda o desempenho em múltiplas disciplinas de forma clara e acionável.

Nosso objetivo é empoderar o aprendizado através da visualização de dados, oferecendo uma solução que transcende a complexidade das planilhas e a dispersão de ferramentas manuais.

## 🎯 Problema que Resolvemos

O gerenciamento acadêmico moderno apresenta três desafios principais:

1.  **Perda de Controle dos Estudos:** Estudantes frequentemente perdem o controle do seu desempenho em múltiplas disciplinas devido à falta de um painel centralizado.
2.  **Análise Muito Superficial:** Ferramentas tradicionais (como planilhas) são excelentes para registro, mas falham em oferecer cálculos avançados e visualizações de progresso dinâmico.
3.  **Complexidade Operacional:** Muitas soluções disponíveis são excessivamente complexas ou exigem um esforço manual de alimentação de dados constante.

**EduTrack AI resolve isso** unificando a coleta de dados, o processamento avançado e a visualização em uma única interface intuitiva.

## ✨ Funcionalidades Principais

*   **📊 Dashboard de Desempenho em Tempo Real:** Visualização gráfica de notas e progresso ao longo do tempo por disciplina.
*   **📚 Gerenciamento Completo de Conteúdo:**
    *   **Gestão de Disciplinas:** Cadastro e parametrização de todas as matérias cursadas.
    *   **Gestão de Tarefas e Atividades:** Registro detalhado de tarefas, prazos e notas obtidas.
*   **🚀 Cálculo Avançado de Progresso:** Utiliza um script `Pandas` robusto para baixa de dados em lote via API do Xano. Ele calcula localmente a porcentagem de conclusão e o Índice de Progresso (IP) antes de renderizar os gráficos.
*   **🔍 Busca e Filtragem Inteligente:** Permite filtrar dados por disciplina, período ou tipo de atividade para análises específicas.
*   **📄 Relatórios Profissionais (PDF):** Geração de relatórios resumidos do desempenho acadêmico, ideais para acompanhamento com professores ou pais.

## ⚙️ Arquitetura Tecnológica (Stack)

O projeto adota uma arquitetura desacoplada, garantindo escalabilidade, robustez e facilidade de manutenção.

*   **Backend & Database: Xano**
    *   Responsável pelo armazenamento seguro e pela API de dados (CRUD).
    *   Serve como a fonte única de verdade (Single Source of Truth) para todos os dados acadêmicos.
*   **Frontend & Business Logic: Streamlit (Python)**
    *   A camada de interface do usuário, construída exclusivamente em Python para garantir uma experiência de desenvolvimento rápida e coesa.
    *   Coordena a requisição de dados e a renderização dos componentes visuais.
*   **Data Processing: Pandas, Requests**
    *   **Pandas:** Motor de cálculo de dados. Responsável por consumir os dados brutos do Xano e aplicar lógicas complexas (ex: cálculo ponderado de notas, porcentagem de conclusão).
    *   **Requests:** Biblioteca usada para interagir com a API do Xano.
*   **Orquestração de IA: OpenSpec**
    *   Utilizado para guiar a geração e aprimoramento do código Python e das regras de negócio no Xano.

## 📦 Dependências Principais

Para rodar o projeto, as seguintes bibliotecas Python são necessárias:

```text
- streamlit
- pandas
- plotly
- requests
- watchdog
- time
```

*Desenvolvido com foco em dados e experiência do usuário, transformando informações dispersas em conhecimento acionável.*
