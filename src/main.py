import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import api # Lib local
import ultilitario as util # Lib local
import time
import requests
from datetime import datetime, timedelta

def set_cookie(name, value, days=30):
    dt = datetime.now() + timedelta(days=days)
    expires = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    js_code = f"""
        <script>
        document.cookie = "{name}={value}; expires={expires}; path=/";
        </script>
    """
    components.html(js_code, height=0)

def delete_cookie(name):
    js_code = f"""
        <script>
        document.cookie = "{name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
        window.parent.location.reload();
        </script>
    """
    components.html(js_code, height=0)

# ------------------------------------------------
# SISTEMA DE AUTENTICAÇÃO
# ------------------------------------------------

def tela_acesso():
    st.title('Portal Acadêmico Personalizado')
    tab_login, tab_cadastro = st.tabs(['Entrar', 'Criar Minha Conta'])

    with tab_login:
        with st.form('login_form'):
            email = st.text_input('E-mail')
            senha = st.text_input('Senha', type='password')
            if st.form_submit_button('Acessar Meu Painel'):
                if not util.valida_email(email):
                    placeholder = st.empty()
                    placeholder.error('E-mail inválido. Deve conter pelo menos 2 caracteres antes do "@" e exatamente um "@"')
                    time.sleep(10)
                    placeholder.empty()
                else:
                    res = requests.post(f'{api.BASE_URL}/auth/login', json={'email': email, 'password': senha})
                    if res.status_code == 200:
                        token = res.json().get('authToken')
                        st.session_state.auth_token = token
                        st.session_state.logged_in = True
                        st.session_state.login_time = datetime.now()
                        set_cookie('auth_token', token)
                        st.rerun()
                    else:
                        placeholder = st.empty()
                        placeholder.error('Credenciais inválidas.')
                        time.sleep(10)
                        placeholder.empty()

    with tab_cadastro:
        with st.form('cadastro_form'):
            nome = st.text_input('Nome')
            email_c = st.text_input('E-mail')
            pass_c = st.text_input('Senha', type='password')

            if st.form_submit_button('Cadastrar'):
                nome = util.limpar_texto(nome)
                email_c = util.limpar_texto(email_c)
                pass_c = util.limpar_texto(pass_c)

                erros_nome = util.valida_nome(nome)
                if erros_nome:
                    placeholder_nome = st.empty()
                    with placeholder_nome.container():
                        for erro in erros_nome:
                            st.error(erro)
                    time.sleep(10)
                    placeholder_nome.empty()
                elif not util.valida_email(email_c):
                    placeholder_email = st.empty()
                    placeholder_email.error('E-mail inválido. Deve conter no minimo 2 caracteres antes do arroba (@), exatamente um arroba (@) e pelo menos um ponto (.)')
                    time.sleep(10)
                    placeholder_email.empty()
                else:
                    erros = util.valida_senha(pass_c)
                    if erros:
                        placeholder_erros = st.empty()
                        with placeholder_erros.container():
                            for erro in erros:
                                st.error(erro)
                        time.sleep(10)
                        placeholder_erros.empty()
                    else:
                        res = requests.post(f'{api.BASE_URL}/auth/signup', json={'name': nome, 'email': email_c, 'password': pass_c})
                        if res.status_code == 200:
                            st.success('Conta criada! Agora faça o login.')
                            time.sleep(2)
                            js_code = """
                                <script>
                                window.parent.location.reload();
                                </script>
                            """
                            components.html(js_code, height=0)
                        else:
                            placeholder_signup = st.empty()
                            placeholder_signup.error('Erro ao cadastrar usuário.')
                            time.sleep(10)
                            placeholder_signup.empty()

# ------------------------------------------------
# MÓDULOS CRUD PARA PROFESSORES, DISCIPLINAS
# E TAREFAS
# ------------------------------------------------

# GESTÃO DE PROFESSORES

def modulo_professores():
    st.header('‍Meus Professores')
    # [C]REATE
    with st.expander('➕ Adicionar Professor'):
        nome = st.text_input('Nome do Professor')
        email = st.text_input('E-mail de Contato')
        if st.button('Cadastrar Professor'):
            nome = util.limpar_texto(nome)
            email = util.limpar_texto(email)

            if not nome:
                st.error('O nome do professor é obrigatório.')
            elif email and not util.valida_email(email):
                st.error('E-mail inválido. Se fornecido, deve ser um e-mail válido.')
            else:
                # Validação de e-mail único
                profs_existentes = api.api_get('professores')
                email_duplicado = any(p.get('email') == email for p in profs_existentes if email and p.get('email'))
                
                if email_duplicado:
                    st.error(f'O e-mail "{email}" já está cadastrado para outro professor.')
                else:
                    api.api_post('professores', {'nome': nome, 'email': email if email else None})
                    st.success('Professor cadastrado com sucesso!')
                    time.sleep(1)
                    st.rerun()

    # [R]EAD & [U]PDATE & [D]ELETE
    dados = api.api_get('professores')
    if dados:
        df = pd.DataFrame(dados)
        st.subheader('Seus Professores Cadastrados')

        if 'edit_prof' not in st.session_state:
            st.session_state.edit_prof = False

        # Editor de dados para facilitar a vida do aluno
        df_editado = st.data_editor(
            df[['id', 'nome', 'email']],
            column_config={
                'id': st.column_config.TextColumn("ID", disabled=True, width="small"),
            },
            use_container_width=True,
            hide_index=True,
            num_rows='dynamic' if st.session_state.edit_prof else None,
            disabled=not st.session_state.edit_prof,
            key="prof_editor"
        )

        # Container para os botões
        col_del_prof, col_espaco, col_save, col_cancel = st.columns([0.2, 0.4, 0.2, 0.2])
        
        with col_del_prof:
            if st.session_state.edit_prof:
                # Mostra seletor de ID para exclusão apenas em modo edição
                id_excluir = st.number_input('ID p/ Excluir', min_value=1, step=1, key='id_del_prof')
                if st.button('Excluir Professor 🗑️', type='primary', use_container_width=True):
                    api.api_delete('professores', id_excluir)
                    st.success('Professor excluído!')
                    time.sleep(1)
                    st.rerun()

        with col_save:
            if not st.session_state.edit_prof:
                if st.button('Editar ✏️', use_container_width=True):
                    st.session_state.edit_prof = True
                    st.rerun()
            else:
                if st.button('Salvar ✅', use_container_width=True):
                    erros_validacao = []
                    profs_atuais = api.api_get('professores')
                    
                    # Validação dos dados editados
                    for index, row in df_editado.iterrows():
                        nome_val = util.limpar_texto(str(row['nome']))
                        email_val = util.limpar_texto(str(row['email'])) if row['email'] else ""
                        id_atual = row.get('id')

                        if not nome_val:
                            erros_validacao.append(f"Linha {index + 1}: O nome do professor não pode ser vazio.")
                        if email_val and not util.valida_email(email_val):
                            erros_validacao.append(f"Linha {index + 1}: E-mail '{email_val}' é inválido.")
                        
                        # Validação de e-mail único (não pode ser igual ao de outro ID)
                        if email_val:
                            email_em_uso = any(p.get('email') == email_val and p.get('id') != id_atual for p in profs_atuais)
                            if email_em_uso:
                                erros_validacao.append(f"Linha {index + 1}: O e-mail '{email_val}' já está em uso por outro professor.")
                        else:
                            # Nova validação: Nome duplicado quando não há e-mail na edição
                            nome_em_uso_sem_email = any(p.get('nome').lower() == nome_val.lower() and not p.get('email') and p.get('id') != id_atual for p in profs_atuais)
                            if nome_em_uso_sem_email:
                                erros_validacao.append(f"Linha {index + 1}: Já existe outro professor com o nome '{nome_val}' sem e-mail.")

                    if erros_validacao:
                        for erro in erros_validacao:
                            st.error(erro)
                    else:
                        # Mostra uma barra de progresso simples ou mensagem de espera
                        with st.spinner('Sincronizando dados com o servidor...'):
                            sucesso_total = True
                            for index, row in df_editado.iterrows():
                                prof_id = row.get('id')
                                if prof_id:
                                    # Limpa os dados antes de enviar
                                    nome_final = util.limpar_texto(str(row['nome']))
                                    email_raw = str(row['email']) if row['email'] else ""
                                    email_final = util.limpar_texto(email_raw) if email_raw and email_raw.lower() != 'none' else None
                                    
                                    res = api.api_patch('professores', prof_id, {
                                        'nome': nome_final,
                                        'email': email_final
                                    })
                                    
                                    if res.status_code != 200:
                                        sucesso_total = False
                                        st.error(f"Erro ao atualizar professor ID {prof_id}: {res.text}")
                            
                            if sucesso_total:
                                st.success('Todos os dados foram sincronizados com sucesso!')
                                st.session_state.edit_prof = False
                                time.sleep(1.5)
                                st.rerun()
                if st.button('Cancelar ❌', use_container_width=True):
                    st.session_state.edit_prof = False
                    st.rerun()
    else:
        st.info('Nenhum professor cadastrado ainda.')

# GESTÃO DE DISCIPLINAS

def modulo_disciplinas():
    st.header('Minhas Disciplina')
    profs = api.api_get('professores')

    if not profs:
        st.warning('Cadastre um professor antes de criar disciplinas.')
        return

    # [C]REATE
    with st.expander('➕ Nova Disciplina'):
        with st.form('form_nova_disciplina'):
            nome_d = st.text_input('Nome da Matéria')
            
            profs = api.api_get('professores')
            # Formata o rótulo para exibir Nome | Email
            opcoes_p = {f"{p['nome']} | {p.get('email', 'S/ E-mail')}": p['id'] for p in profs} if profs else {}
            p_escolhido = st.selectbox('Professor Responsável', options=list(opcoes_p.keys()))
            
            col1, col2 = st.columns(2)
            with col1:
                carga_horaria = st.number_input('Carga Horária (horas)', min_value=1, step=1)
                dia_semana = st.selectbox('Dia da Semana', options=['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'])
                faltas = st.number_input('Faltas Atuais', min_value=0, step=1)
            with col2:
                max_faltas = st.number_input('Limite de Faltas', min_value=0, step=1)
                horario = st.time_input('Horário da Aula')
                nota = st.number_input('Nota Final/Atual', 0.0, 10.0, 0.0)
            
            anotacoes = st.text_area('Anotações (Opcional)')
            
            if st.form_submit_button('Salvar Disciplina'):
                if not nome_d:
                    st.error('O nome da disciplina é obrigatório.')
                elif not p_escolhido:
                    st.error('Selecione um professor.')
                else:
                    api.api_post('disciplinas', {
                        'nome': nome_d, 
                        'prof_id': opcoes_p[p_escolhido],
                        'carga_horaria': carga_horaria,
                        'max_faltas': max_faltas,
                        'faltas': faltas,
                        'nota': nota,
                        'dia_semana': dia_semana,
                        'horario': horario.strftime('%H:%M'),
                        'anotacoes': anotacoes
                    })
                    st.success('Disciplina cadastrada com sucesso!')
                    time.sleep(1)
                    st.rerun()

    # [R]EAD
    discs = api.api_get('disciplinas')
    if discs:
        df_d = pd.DataFrame(discs)
        df_p = pd.DataFrame(profs)
        
        # Verifica se a coluna 'prof_id' existe para evitar erro no merge
        if 'prof_id' in df_d.columns:
            # Junta os nomes para exibição
            df_view = df_d.merge(df_p[['id', 'nome']], left_on='prof_id', right_on='id', suffixes=('', '_prof'))
            
            # Reorganiza as colunas conforme solicitado
            # nome da disciplina, nome do professor, carga horaria, limite de faltas, faltas, nota e horario
            cols_to_show = ['nome', 'nome_prof', 'carga_horaria', 'max_faltas', 'faltas', 'nota', 'horario']
            
            # Filtra apenas as colunas que realmente existem no DataFrame resultante para evitar novos erros
            cols_existentes = [c for c in cols_to_show if c in df_view.columns]
            
            st.dataframe(df_view[cols_existentes], use_container_width=True, hide_index=True)
        else:
            st.warning('Aviso: Os dados das disciplinas parecem estar incompletos (faltando prof_id).')
            st.dataframe(df_d, use_container_width=True, hide_index=True)

        # [D]ELETE
        id_del = st.number_input('ID para remover', min_value=1, step=1)
        if st.button('Remover Disciplina', type='primary'):
            api.api_delete('disciplinas', id_del)
            st.rerun()

# GESTÃO DE TAREFAS ---

def modulo_tarefas():
    st.header('Minhas Tarefas e Notas')
    discs = api.api_get('disciplinas')

    if not discs:
        st.warning('Cadastre uma disciplina primeiro.')
        return

    # [C]REATE
    with st.expander('➕ Lançar Atividade/Nota'):
        nome_t = st.text_input('Nome da Atividade')
        opcoes_d = {d['nome']: d['id'] for d in discs}
        d_escolhida = st.selectbox('Selecione a Disciplina', options=list(opcoes_d.keys()))
        nota = st.number_input('Nota Obtida', 0.0, 10.0, 0.0)
        if st.button('Registrar Nota'):
            api.api_post('tarefas', {'nome': nome_t, 'disc_id': opcoes_d[d_escolhida], 'nota': nota})
            st.rerun()

    # [R]EAD
    tarefas = api.api_get('tarefas')
    if tarefas:
        df_t = pd.DataFrame(tarefas)
        st.subheader('Quadro de Notas')
        st.dataframe(df_t[['id', 'nome', 'nota']], use_container_width=True, hide_index=True)

        # [D]ELETE
        id_del_t = st.number_input('ID da Tarefa para remover', min_value=1, step=1)
        if st.button('Remover Tarefa'):
            api.api_delete('tarefas', id_del_t)
            st.rerun()

# --- DASHBOARD ---

def modulo_dashboard():
    st.header('Resumo de Desempenho')
    tarefas = api.api_get('tarefas')
    discs = api.api_get('disciplinas')
    if not tarefas or not discs:
        st.info('Cadastre dados para visualizar seu desempenho gráfico.')
        return

    df_t = pd.DataFrame(tarefas)
    df_d = pd.DataFrame(discs)
    df_plot = df_t.merge(df_d, left_on='disc_id', right_on='id', suffixes=('_t', '_d'))
    # Re-enabled plotly if available, else fallback
    try:
        import plotly.express as px
        fig = px.bar(df_plot, x='nome_t', y='nota', color='nome_d',
                     title='Minhas Notas por Matéria', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.bar_chart(df_plot.set_index('nome_t')['nota'])

# ------------------------------------------
# ESTRUTURA PRINCIPAL DE NAVEGAÇÃO
# ------------------------------------------

def main():
    st.set_page_config(page_title='EduTrack AI', layout='wide')

    # Tenta recuperar o token do cookie NO INÍCIO do script
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        cookie_token = st.context.cookies.get('auth_token')
        if cookie_token:
            st.session_state.auth_token = cookie_token
            st.session_state.logged_in = True
            st.session_state.login_time = datetime.now()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Verifica se a sessão expirou (24 horas)
    if st.session_state.get('logged_in') and 'login_time' in st.session_state:
        if datetime.now() - st.session_state.login_time > timedelta(hours=24):
            st.session_state.clear()
            delete_cookie('auth_token')
            st.stop()

    if not st.session_state.logged_in:
        tela_acesso()
    else:
        # Garante que o cookie esteja presente no navegador se estivermos logados
        if not st.context.cookies.get('auth_token'):
            set_cookie('auth_token', st.session_state.auth_token)

        with st.sidebar:
            st.title('EduTrack AI')
            menu = st.radio('Gerenciar:', ['Painel Geral', 'Professores', 'Disciplinas', 'Tarefas/Notas'])
            st.markdown('---')
            if st.button('Sair'):
                st.session_state.clear()
                delete_cookie('auth_token')
                st.stop()

        match menu:
            case 'Painel Geral': modulo_dashboard()
            case 'Professores': modulo_professores()
            case 'Disciplinas': modulo_disciplinas()
            case 'Tarefas/Notas': modulo_tarefas()

if __name__ == "__main__":
    main()
