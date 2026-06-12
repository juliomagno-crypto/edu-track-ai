import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import api   #Lib local
import ultilitario as util # Lib local
import time
import requests
from datetime import datetime, timedelta
BASE_URL = 'https://x8ki-letl-twmt.n7.xano.io/api:FzC8bz6B'

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
                v_nome=util.valida_nome(nome)
                v_email=util.valida_email(email_c)
                v_pass=util.valida_senha(pass_c)

                if v_nome and v_email and v_pass:

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

           

def modulo_projetos():
    st.header('‍Meus Projetos')
    # [C]REATE
    with st.expander('➕ Adicionar Projetos Acadêmicos'):
        nome = st.text_input('Nome do Projeto ')
        tipo = st.text_input('Tipo do Projeto ')
        link = st.text_input('Link do Projeto ')
        descricao = st.text_input('Descrição do Projeto ')
        Disciplina = st.text_input('ID da disciplina cadastrada')
        data_inicial = st.date_input('Data de inicial')
        data_final= st.date_input('Data de Final')
        if st.button('Cadastrar Projeto'):

            if not nome:
                st.error('O nome do projeto é obrigatório.')
                st.rerun()
           
            if not Disciplina:
                st.error('A disciplina é obrigatória.')
                st.rerun()
            else:
                response = api.api_post('projetos', {
                            'nome': nome,
                            'tipo': tipo,
                            'dataInicial': data_inicial.isoformat(),
                            'dataFinal': data_final.isoformat(),
                            'link': link,
                            'descricao': descricao,
                            'disciplinas_id': Disciplina,
                            'user_id': st.session_state.get('user_id')
                            })
            time.sleep(1)
            erro=response.status_code
            if erro == 200:
                st.success("Projeto cadastrado com sucesso!")
           
            elif erro ==400:
                st.error("Projetos devem ter nomes diferentes.")
                time.sleep(3)
                st.rerun()
    
    

        

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
                api.api_post('professores', {'nome': nome, 'email': email if email else None, 'user_id': st.session_state.get('user_id')})
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

        # Container para os botões no canto inferior direito
        col_espaco, col_save, col_del, col_cancel = st.columns([0.4, 0.2, 0.2, 0.2])
        with col_save:
            if not st.session_state.edit_prof:
                if st.button('Editar ✏️', use_container_width=True):
                    st.session_state.edit_prof = True
                    st.rerun()
            else:
                if st.button('Salvar ✅', use_container_width=True):
                    erros_validacao = []
                    # Validação dos dados editados
                    for index, row in df_editado.iterrows():
                        nome_val = util.limpar_texto(str(row['nome']))
                        email_val = util.limpar_texto(str(row['email'])) if row['email'] else ""

                        if not nome_val:
                            erros_validacao.append(f"Linha {index + 1}: O nome do professor não pode ser vazio.")
                        if email_val and not util.valida_email(email_val):
                            erros_validacao.append(f"Linha {index + 1}: E-mail '{email_val}' é inválido.")

                    if erros_validacao:
                        for erro in erros_validacao:
                            st.error(erro)
                    else:
                        # Atualiza apenas os que permaneceram
                        for _, row in df_editado.iterrows():
                            if 'id' in row and row['id']:
                                api.api_patch('professores', row['id'], {
                                    'nome': util.limpar_texto(str(row['nome'])),
                                    'email': util.limpar_texto(str(row['email'])) if row['email'] else None
                                })
                        st.success('Dados sincronizados!')
                        st.session_state.edit_prof = False
                        time.sleep(1)
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
        nome_d = st.text_input('Nome da Matéria')
        opcoes_p = {p['nome']: p['id'] for p in profs}
        p_escolhido = st.selectbox('Professor Responsável', options=list(opcoes_p.keys()))

        if st.button('Salvar Disciplina'):
            api.api_post('disciplinas', {'nome': nome_d, 'professores_id': opcoes_p[p_escolhido]})
            st.rerun()

    # [R]EAD
    discs = api.api_get('disciplinas')
    profs = api.api_get('professores')
    if discs:
    # Garante a criação correta dos DataFrames convertendo os dados da API
        df_d = pd.DataFrame(list(discs))
        df_p = pd.DataFrame(list(profs)) 

        # Validação de segurança: verifica se as colunas realmente existem no df_p
        if 'id' in df_p.columns and 'nome' in df_p.columns:
            df_view = df_d.merge(
                df_p[['id', 'nome']], 
                left_on='professores_id',  
                right_on='id',           
                suffixes=('', '-Professor')
            )
            # Exibe os nomes na tela
            st.dataframe(df_view[['nome', 'nome-Professor']], use_container_width=True, hide_index=True)
        else:
            # Se as colunas não forem encontradas, mostra o que veio da API para diagnosticar
            st.error("As colunas 'id' e 'nome' não foram encontradas na tabela de professores.")
            st.write("Colunas detectadas em professores:", list(df_p.columns))
            st.write("Dados brutos de professores:", profs)

    # UPDATE    
    if 'edit_disc' not in st.session_state:
        st.session_state.edit_disc = False

    
    # Mostramos ID, Nome da Matéria, ID do Professor e o Nome do Professor Atual
    df_editado = st.data_editor(
        df_view[['id', 'nome', 'professores_id', 'nome-Professor']],
        column_config={
            'id': st.column_config.NumberColumn("ID", disabled=True, width="small"),
            'nome': st.column_config.TextColumn("Nome da Disciplina"),
            'professores_id': st.column_config.NumberColumn("ID do Professor"),
            'nome-Professor': st.column_config.TextColumn("Professor Atual", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        num_rows='dynamic' if st.session_state.edit_disc else None,
        disabled=not st.session_state.edit_disc,
        key="disc_editor"
    )

    # Captura o estado do editor para gerenciar os Deletes da lixeira
    mudar_estado = st.session_state.get("disc_editor", {"deleted_rows": []})

    # Container para os botões no canto inferior direito
    col_espaco, col_save, col_del, col_cancel = st.columns([0.4, 0.2, 0.2, 0.2])
    with col_save:
        if not st.session_state.edit_disc:
            if st.button('Editar ✏️', use_container_width=True):
                st.session_state.edit_disc = True
                st.rerun()
        else:
            if st.button('Salvar ✅', use_container_width=True):
                erros_validacao = []
                
                # 1. Validação dos dados que restaram na tabela
                for index, row in df_editado.iterrows():
                    nome_val = util.limpar_texto(str(row['nome']))
                    
                    if not nome_val or nome_val == "none":
                        erros_validacao.append(f"Linha {index + 1}: O nome da disciplina não pode ser vazio.")

                if erros_validacao:
                    for erro in erros_validacao:
                        st.error(erro)
                else:
                    # 2. Processa as exclusões (Lixeira) primeiro
                    if mudar_estado and mudar_estado.get("deleted_rows"):
                        for linha_index in mudar_estado["deleted_rows"]:
                            id_para_deletar = df_view.iloc[linha_index]["id"]
                            api.api_delete('disciplinas', id_para_deletar)

                    # 3. Atualiza os registros que continuam na tabela (Update/PATCH)
                    for _, row in df_editado.iterrows():
                        if 'id' in row and row['id']:
                            # Garante que o ID do professor seja um número inteiro válido ou nulo
                            prof_id_val = int(row['professores_id']) if pd.notna(row['professores_id']) else None
                            
                            api.api_patch('disciplinas', row['id'], {
                                'nome': util.limpar_texto(str(row['nome'])),
                                'professores_id': prof_id_val
                            })
                            
                    st.success('Dados sincronizados!')
                    st.session_state.edit_disc = False
                    time.sleep(1)
                    st.rerun()
                    
            if st.button('Cancelar ❌', use_container_width=True):
                st.session_state.edit_disc = False
                st.rerun()
            else:
                st.info('Nenhuma disciplina cadastrada ainda.')

# GESTÃO DE TAREFAS ---

def modulo_tarefas():
    st.header('Minhas Tarefas')
    discs = api.api_get('disciplinas')

    if not discs:
        st.warning('Cadastre uma disciplina primeiro.')
        return

    # [C]REATE
    with st.expander('➕ Nova Tarefa'):
        nome = st.text_input('Nome da Tarefa')
        tipo = st.selectbox('Tipo', ['Acadêmico', 'Pessoal'])
        status = st.selectbox('Status', ['Pendente', 'Em andamento', 'Entregue', 'Atrasado'])
        descricao = st.text_area('Descrição')
        data_atribuicao = st.date_input('Data de Atribuição')
        data_entrega = st.date_input('Data de Entrega')
        link = st.text_input('Link (opcional)')

        opcoes_d = {d['nome']: d['id'] for d in discs}
        d_escolhida = st.selectbox('Disciplina', options=list(opcoes_d.keys()))

        projetos_id = None
        projetos =api.api_get('projetos')
        if projetos:
            opcoes_p = {p['nome']: p['id'] for p in projetos}
            p_escolhido = st.selectbox('Projeto Vinculado', options=['(nenhum)'] + list(opcoes_p.keys()))
            if p_escolhido != '(nenhum)':
                projetos_id = opcoes_p[p_escolhido]

        pontuacao = st.number_input('Pontuação', min_value=0.0, max_value=10.0, step=0.1)

        if st.button('Cadastrar Tarefa'):
            if not nome:
                st.error('O nome da tarefa é obrigatório.')
            else:
                api.api_post('tarefas', {
                    'nome': nome,
                    'tipo': tipo,
                    'status': status,
                    'descricao': descricao,
                    'data_atribuicao': data_atribuicao.isoformat(),
                    'data_entrega': data_entrega.isoformat(),
                    'link': link,
                    'pontuacao': pontuacao,
                    'disc_id': opcoes_d[d_escolhida],
                    'projetos_id': projetos_id
                })
                st.success('Tarefa cadastrada com sucesso!')
                st.rerun()

    # [R]EAD
    tarefas = api.api_get('tarefas')
    if tarefas:
        df = pd.DataFrame(tarefas)
        st.subheader('Suas Tarefas')

        # [U]PDATE
        df_visualizacao = df[['id', 'nome', 'tipo', 'status', 'pontuacao', 'data_entrega', 'link']].copy()
        df_visualizacao['data_entrega'] = pd.to_datetime(df_visualizacao['data_entrega']).dt.date
        
        df_editado = st.data_editor(
            df_visualizacao,
            column_config={
                'id': st.column_config.NumberColumn('ID', disabled=True, width='small'),
                'status': st.column_config.SelectboxColumn(
                    'Status', options=['Pendente', 'Em andamento', 'Entregue', 'Atrasado']
                ),
                'tipo': st.column_config.SelectboxColumn(
                    'Tipo', options=['Acadêmico', 'Pessoal']
                ),
                'data_entrega': st.column_config.DateColumn('Data de Entrega'),
                'pontuacao': st.column_config.NumberColumn('Pontuação', min_value=0.0, max_value=10.0),
            },
            use_container_width=True,
            hide_index=True,
            num_rows='dynamic',
            key="editor_tarefas"
        )

        if st.button('Salvar Alterações em Tarefas'):
            estado_editor = st.session_state.get("editor_tarefas", {})
            linhas_editadas = estado_editor.get("edited_rows", {})

            if linhas_editadas:
                for idx_linha, alteracoes in linhas_editadas.items():
                    tarefa_id = int(df_visualizacao.iloc[idx_linha]['id'])
                    if 'data_entrega' in alteracoes and alteracoes['data_entrega']:
                        alteracoes['data_entrega'] = str(alteracoes['data_entrega'])
                    api.api_patch('tarefas', tarefa_id, alteracoes)
                st.success('Tarefas atualizadas!')
                st.rerun()
            else:
                st.info('Nenhuma alteração detectada.')

        # [D]ELETE
        id_del = st.number_input('ID da tarefa para remover', min_value=1, step=1)
        if st.button('Remover Tarefa', type='primary'):
            api.api_delete('tarefas', id_del)
            st.success('Tarefa removida!')
            st.rerun()
    else:
        st.info('Nenhuma tarefa cadastrada ainda.')

# GESTÃO DE PROVAS
def modulo_provas():
    st.header('Minhas Provas')
    discs = api.api_get('disciplinas')

    if not discs:
        st.warning('Cadastre uma disciplina primeiro.')
        return

    # [C]REATE
    with st.expander('➕ Nova Prova'):
        conteudo = st.text_area('Conteúdo da Prova')
        data = st.date_input('Data da Prova')
        horario = st.text_input('Horário (ex: 19:30)')
        
        opcoes_d = {d['nome']: d['id'] for d in discs}
        d_escolhida = st.selectbox('Disciplina', options=list(opcoes_d.keys()))
        
        nota = st.number_input('Nota', min_value=0.0, max_value=10.0, step=0.1)

        if st.button('Cadastrar Prova'):
            if not conteudo:
                st.error('O conteúdo da prova é obrigatório.')
            else:
                api.api_post('provas', {
                    'conteudo': conteudo,
                    'data': data.isoformat(),
                    'horario': horario,
                    'nota': nota,
                    'disciplinas_id': opcoes_d[d_escolhida]
                })
                st.success('Prova cadastrada com sucesso!')
                st.rerun()

    # [R]EAD
    provas = api.api_get('provas')
    if provas:
        df = pd.DataFrame(provas)
        st.subheader('Suas Provas')

        # [U]PDATE
        df_visualizacao = df[['id', 'conteudo', 'data', 'horario', 'nota']].copy()
        df_visualizacao['data'] = pd.to_datetime(df_visualizacao['data']).dt.date
        
        df_editado = st.data_editor(
            df_visualizacao,
            column_config={
                'id': st.column_config.NumberColumn('ID', disabled=True, width='small'),
                'conteudo': st.column_config.TextColumn('Conteúdo'),
                'data': st.column_config.DateColumn('Data'),
                'horario': st.column_config.TextColumn('Horário'),
                'nota': st.column_config.NumberColumn('Nota', min_value=0.0, max_value=10.0),
            },
            use_container_width=True,
            hide_index=True,
            num_rows='dynamic',
            key="editor_provas"
        )

        if st.button('Salvar Alterações em Provas'):
            estado_editor = st.session_state.get("editor_provas", {})
            linhas_editadas = estado_editor.get("edited_rows", {})

            if linhas_editadas:
                for idx_linha, alteracoes in linhas_editadas.items():
                    prova_id = int(df_visualizacao.iloc[idx_linha]['id'])
                    if 'data' in alteracoes and alteracoes['data']:
                        alteracoes['data'] = str(alteracoes['data'])
                    api.api_patch('provas', prova_id, alteracoes)
                st.success('Provas updated!')
                st.rerun()
            else:
                st.info('Nenhuma alteração detectada.')

        # [D]ELETE
        id_del = st.number_input('ID da prova para remover', min_value=1, step=1)
        if st.button('Remover Prova', type='primary'):
            api.api_delete('provas', id_del)
            st.success('Prova removida!')
            st.rerun()
        else:
            st.info('Nenhuma prova cadastrada ainda.')

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
            st.session_state.logged_in = False
            st.rerun()

    if not st.session_state.logged_in:
        tela_acesso()
    else:
        # Garante que o cookie esteja presente no navegador se estivermos logados
        if not st.context.cookies.get('auth_token'):
            set_cookie('auth_token', st.session_state.auth_token)

        with st.sidebar:
            st.title('EduTrack AI')
            menu = st.radio('Gerenciar:', ['Painel Geral', 'Professores', 'Disciplinas', 'Tarefas/Notas', 'Projetos'])
            st.markdown('---')
            if st.button('Sair'):
                st.session_state.clear()
                delete_cookie('auth_token')
                st.rerun()

        match menu:
           case 'Projetos': modulo_projetos()
           case 'Painel Geral': modulo_dashboard()
           case 'Professores': modulo_professores()
           case 'Disciplinas': modulo_disciplinas()
           case 'Tarefas/Notas': modulo_tarefas()
            


if __name__ == "__main__":
    main()
