# Edu Track IA

O EduTrack AI é um Web App construído inteiramente em Python conectado a um backend Xano.

A proposta é criar uma ferramenta de dados onde o aluno não apenas registra tarefas, mas visualiza dashboards interativos sobre seu desempenho escolar.

## Stack Tecnológica
- Backend: Xano (Banco de dados e API).
- Frontend: Streamlit (Python puro para UI).
- Orquestração: OpenSpec (para guiar a IA na geração de código Python e Xano).
- IA: Gemini

## Problema Resolvido
- Estudantes perdem o controle de múltiplas disciplinas.
- Falta de visualização clara de dados (Gráficos de progresso).
- Ferramentas atuais são complexas demais ou manuais demais (Planilhas).



# Features

- Gerenciamento de Disciplinas
- Gerenciamento de Tarefas
- Dashboard de Dados
- Cálculo Avançado de Progresso: Script Python (Pandas) que baixa dados do Xano e calcula % de conclusão localmente antes de exibir.
- Busca e Filtros
- Relatórios PDF


# Dependencias
 
- Pandas
- Streamlit
- Watchdog
- Requests
- Plotly