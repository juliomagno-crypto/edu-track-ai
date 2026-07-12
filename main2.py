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
col_botao, _ = st.columns([0.2, 0.8])

def aplicar_tema_claro():
    st.markdown("""
    <style>
    /* Botões */
.stButton > button,
div[data-testid="stFormSubmitButton"] > button {

    background-color: #D9DCE1 !important;
    color: white !important;
    border: 1px solid #BFC5CC !important;
}

/* Hover */
.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {

    background-color: #D9DCE1 !important;
    color: white !important;
    border: 1px solid #BFC5CC !important;
}

/* Clique */
.stButton > button:active,
div[data-testid="stFormSubmitButton"] > button:active {

    background-color: #D9DCE1 !important;
    color: white !important;
}

/* Foco */
.stButton > button:focus,
div[data-testid="stFormSubmitButton"] > button:focus {

    background-color: #D9DCE1 !important;
    color: white !important;
    box-shadow: none !important;
}

    /* Fundo da aplicação */
    .stApp {
        background-color: #F0F2F6;
    }

    /* Caixa de texto */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: #E6E8EB;
        color: #000000;
        border: 1px solid #BFC5CC;
        border-radius: 8px;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #E6E8EB;
        color: #000000;
        border: 1px solid #BFC5CC;
        border-radius: 8px;
    }

    /* Botões */
    .stButton button {
        background-color: #D9DCE1;
        color: black;
        border-radius: 8px;
        border: 1px solid #BFC5CC;
    }

    /* Data Editor */
    .stDataFrame {
        background-color: #FFFFFF;
    }
    .stTextInput input,
    .stTextArea textarea {
    caret-color: black !important;
    }
    /* Texto das abas */
    button[data-baseweb="tab"] {
        color: black !important;
        font-weight: bold;
    }
    
    div[data-testid="stTextInput"] label {
        color: black !important;
    }
                
    /* Aba selecionada */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: black !important;
    }
    <style>

/* Botão do formulário */
div[data-testid="stForm"] button {
    background-color: #D9DCE1 !important;
    color: white !important;
    border: 1px solid #BFC5CC !important;
}

/* Hover: mantém exatamente a mesma aparência */
div[data-testid="stForm"] button:hover {
    background-color: #D9DCE1 !important;
    color: white !important;
    border: 1px solid #BFC5CC !important;
}

/* Clique */
div[data-testid="stForm"] button:active {
    background-color: #D9DCE1 !important;
    color: white !important;
}

/* Foco */
div[data-testid="stForm"] button:focus {
    background-color: #D9DCE1 !important;
    color: white !important;
    box-shadow: none !important;
}
/* Botões comuns */
.stButton > button{
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
}

/* Botões de formulário */
div[data-testid="stFormSubmitButton"] > button{
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
}

/* Hover */
.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover{
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #000000 !important;
}

/* Clique */
.stButton > button:active,
div[data-testid="stFormSubmitButton"] > button:active{
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

/* Foco */
.stButton > button:focus,
div[data-testid="stFormSubmitButton"] > button:focus{
    background-color: #000000 !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}

    /* Alvo definitivo para texto preto no botão da barra lateral */
    section[data-testid="stSidebar"] div.stButton > button,
    section[data-testid="stSidebar"] div.stButton > button p,
    section[data-testid="stSidebar"] div.stButton > button span,
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

def aplicar_tema_claro_user():
 st.markdown("""
<style>

/* Fundo geral */
.stApp{
    background:white;
    color:black;
}

/* Header */
header[data-testid="stHeader"]{
    background:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:black !important;
}

/* Texto da sidebar */
section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Warning */
div[data-baseweb="notification"]{
    color:black !important;
}

div[data-baseweb="notification"] *{
    color:black !important;
}

/* Títulos */
h1, h2, h3, h4, h5, h6{
    color:black !important;
}

/* Botões */
.stButton button{
    background:white !important;
    color:black !important;
    border:1px solid black !important;
    border-radius:8px;
}

.stButton button:hover{
    background:#f5f5f5 !important;
    color:black !important;
}

/* Campos de texto */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input{
    background:white !important;
    color:black !important;
    border:1px solid black !important;
    border-radius:8px;
    caret-color:black !important;
}

/* Selectbox */
div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
    border:1px solid black !important;
}

/* Labels */
label{
    color:black !important;
}

/* Abas */
button[data-baseweb="tab"]{
    color:black !important;
    font-weight:bold;
}
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] .stButton > button p,
section[data-testid="stSidebar"] .stButton > button span {
    color: black !important;
    -webkit-text-fill-color: black !important;
    opacity: 1 !important;
}
button[data-baseweb="tab"][aria-selected="true"]{
    color:black !important;
    border-bottom:2px solid black !important;
}

/* DataFrame */
.stDataFrame{
    background:white;
}

/* Barra lateral preta */
section[data-testid="stSidebar"]{
    background-color: black !important;
}

/* Todo o texto da barra lateral branco */
section[data-testid="stSidebar"] *{
    color: white !important;
}

/* Ícones da barra lateral */
section[data-testid="stSidebar"] svg{
    fill: white !important;
}


</style>
""", unsafe_allow_html=True)
def aplicar_tema_escuro():
    return st.markdown( """
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            </style>
            """,
            unsafe_allow_html=True)
            
# ------------------------------------------------
# SISTEMA DE AUTENTICAÇÃO
# ------------------------------------------------
def tela_acesso():
    st.markdown("<h1 style='text-align: center; color: #5F50BF;'>Portal Acadêmico Personalizado</h1>", unsafe_allow_html=True)
    col_botao, col_espaco = st.columns([0.15, 1.5])
    
    
    if 'tema_claro_ativo' not in st.session_state:
         st.session_state.tema_claro_ativo = True  # Começa no claro por padrão

    # 3. Aplica o tema atual baseado no estado da sessão
    if st.session_state.tema_claro_ativo:
        aplicar_tema_claro()
    else:
        aplicar_tema_escuro()

    # 4. O Botão no canto superior esquerdo para alternar o tema

    with col_botao:
        if st.session_state.tema_claro_ativo:
            # Se está claro, mostra a opção de mudar para o escuro
            if st.button('🌙 Tema Escuro', use_container_width=True):
                st.session_state.tema_claro_ativo = False
                st.rerun()
        else:
            # Se está escuro, mostra a opção de mudar para o claro
            if st.button('☀️ Tema Claro', use_container_width=True):
                st.session_state.tema_claro_ativo = True
                st.rerun()
             
        
    

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
                v_nome = util.valida_nome(nome)
                if not v_nome:
                    return

                v_email = util.valida_email(email_c)
                if not v_email:
                    return

                v_pass = util.valida_senha(pass_c)
                if not v_pass:
                    return
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
    
    disc=api.api_get('disciplinas')
    if disc:
        # [C]REATE
        with st.expander('➕ Adicionar Projetos Acadêmicos'):
            nome = st.text_input('Nome do Projeto ')
            tipo = st.selectbox('Tipo', ['Acadêmico', 'Pessoal'])
            link = st.text_input('Link do Projeto ')
            descricao = st.text_input('Descrição do Projeto ')
            data_inicial = st.date_input('Data de inicial')
            data_final= st.date_input('Data de Final')
            
            Disciplina = {p['nome']: p['id'] for p in disc}
            p_escolhido = st.selectbox('Nome da disciplina',options=list(Disciplina.keys()))
            id_disciplina = Disciplina[p_escolhido]
            
            

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
                                'disciplinas_id': id_disciplina,
                                'user_id': st.session_state.get('user_id'),
                            
                                })
                
                time.sleep(1)
                erro=response.status_code
                if erro == 200:
                    st.success("Projeto cadastrado com sucesso!")
            
                elif erro ==400:
                    st.error("Projetos devem ter nomes diferentes.")
                    time.sleep(3)
                    st.rerun()
        
            # [R]EAD 
            dados = api.api_get('projetos')
            if dados:
                df = pd.DataFrame(dados)
                st.subheader('Seus projetos Cadastrados')

                if 'edit_proj' not in st.session_state:
                    st.session_state.edit_proj = False

                
                df_editado = st.data_editor(
                    df[['nome',
                        'tipo',
                        'dataInicial',
                        'dataFinal',  
                        'link' ,
                        'descricao',
                        'disciplinas_id']],
                    column_config={
                        'id': st.column_config.TextColumn("ID", disabled=True, width="small"),
                    },
                    use_container_width=True,
                    hide_index=True,
                    num_rows='dynamic' if st.session_state.edit_proj else None,
                    disabled=not st.session_state.edit_proj,
                    key="proj_editor"
                    )
                # [U]PDATE & [D]ELETE
    
                col_espaco, col_save, col_del, col_cancel = st.columns([0.4, 0.2, 0.2, 0.2])
                with col_save:
                    if not st.session_state.edit_proj:
                        if st.button('Editar ✏️', use_container_width=True):
                            st.session_state.edit_proj = True
                            st.rerun()
                    else:
                        if st.button('Salvar ✅', use_container_width=True):
                            erros_validacao = []

                            for _, row in df_editado.iterrows():
                                    nome= util.limpar_texto(str(row['nome']))
                                    tipo= util.limpar_texto(str(row['tipo']))
                                    data_inicial = util.limpar_texto(str(row['dataInicial']))
                                    data_final = util.limpar_texto(str(row['dataFinal']))
                                    link = util.limpar_texto(str(row['link']))
                                    descricao = util.limpar_texto(str(row['descricao']))
                                    id_disciplinas = util.limpar_texto(str(row['disciplinas_id']))

                                
                        else:
                                # Atualiza apenas os que permaneceram
                                for _, row in df_editado.iterrows():
                                    if 'id' in row and row['id']:
                                        api.api_patch('disciplinas', row['id'], {
                                            'nome': util.limpar_texto(str(row['nome'])),
                                            'tipo': util.limpar_texto(str(row['tipo'])),
                                            'dataInicial': util.limpar_texto(str(row['dataInicial'])),
                                            'dataFinal': util.limpar_texto(str(row['dataFinal'])),
                                            'link': util.limpar_texto(str(row['link'])),
                                            'descricao': util.limpar_texto(str(row['descricao'])),
                                            'disciplinas_id': util.limpar_texto(str(row['disciplinas_id'])),
                                            'user_id': st.session_state.get('user_id')
                                        })
                                st.success('Dados sincronizados!')
                                st.session_state.edit_prof = False
                                time.sleep(1)
                                st.rerun()
                        if st.button('Cancelar ❌', use_container_width=True):
                            st.session_state.edit_prof = False
                            st.rerun()
            else:
                st.info('Nenhum projeto cadastrado ainda.')
            
        
    else:
        st.info('Cadastre uma disciplina primeiro.')
    

# ------------------------------------------------
# MÓDULOS CRUD PARA PROFESSORES, DISCIPLINAS,
# PROJETOS E TAREFAS
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
                res= api.api_post('professores', {'nome': nome, 'email': email if email else None, 'user_id': st.session_state.get('user_id')})
                if res.status_code == 200:
                    st.success('Professor cadastrado com sucesso!')
                elif res.status_code == 500:
                    st.error('Não é permitido e-mails já cadastrados.')
                else:
                    st.error('Erro ao cadastrar professor.')
                time.sleep(1)
                st.rerun()

    # [R]EAD 
    dados = api.api_get('professores')
    if dados:
        df = pd.DataFrame(dados)
        st.subheader('Seus Professores Cadastrados')

        if 'edit_prof' not in st.session_state:
            st.session_state.edit_prof = False

        
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
        #[U]PDATE
        if st.button('Salvar Alterações em Professores'):
            estado_editor = st.session_state.get("prof_editor", {})
            linhas_editadas = estado_editor.get("edited_rows", {})

            if linhas_editadas:
                for idx_linha, alteracoes in linhas_editadas.items():
                    tarefa_id = int(df_editado.iloc[idx_linha]['id'])
                    if 'nome' in alteracoes and alteracoes['nome']:
                        alteracoes['nome'] = str(alteracoes['nome'])
                    api.api_patch('professores', tarefa_id, alteracoes)
                st.success('Tarefas atualizadas!')
                st.rerun()
            else:
                st.info('Nenhuma alteração detectada.')

        # [D]ELETE
        id_del = st.number_input('ID da tarefa para remover', min_value=1, step=1)
        if st.button('Remover professores', type='primary'):
            api.api_delete('professores', id_del)
            st.success('Professor removido!')
            st.rerun()
    else:
        st.info('Nenhum professor cadastrado ainda.')

# GESTÃO DE DISCIPLINAS

def modulo_disciplinas():
    st.header('Minhas Disciplinas')
    profs = api.api_get('professores')
    if not profs:
        st.warning('Cadastre um professor antes de cadastrar uma disciplina.')
        return

    # [C]REATE - Nova Disciplina
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

        # CORREÇÃO DO AVISO AMARELO: Injeta o prof_id esperado pelo resto do sistema
        if 'professores_id' in df_d.columns:
            df_d['prof_id'] = df_d['professores_id']

        # Validação de segurança: verifica se as colunas realmente existem no df_p
        if 'id' in df_p.columns and 'nome' in df_p.columns:
            df_view = df_d.merge(
                df_p[['id', 'nome']], 
                left_on='professores_id',  
                right_on='id',           
                suffixes=('', '-Professor')
            )
            
            # Gerencia o estado de edição
            if 'edit_disc' not in st.session_state:
                st.session_state.edit_disc = False
            
            # [U]PDATE

            if st.session_state.edit_disc:
                st.subheader('Modo de Edição de Disciplinas')
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
                    num_rows='dynamic',
                    key="disc_editor"
                )
            
            else:
                # Filtra apenas as colunas amigáveis ao usuário
                colunas_para_mostrar = ['id', 'nome', 'carga_horaria', 'limite_falta', 'faltas', 'nota', 'dia', 'horario']
                colunas_validas = [col for col in colunas_para_mostrar if col in df_view.columns]
                
                df_filtrado = df_view[colunas_validas].copy()

                # Renomeia os cabeçalhos para o português correto
                df_filtrado = df_filtrado.rename(columns={
                    'nome': 'Nome da Disciplina',
                    'carga_horaria': 'Carga Horária',
                    'limite_falta': 'Limite de Faltas',
                    'faltas': 'Faltas Atuais',
                    'nota': 'Nota',
                    'dia': 'Dia da Semana',
                    'horario': 'Horário'
                })

                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

            # --- PAINEL DE BOTÕES DE CONTROLE ---
            mudar_estado = st.session_state.get("disc_editor", {"deleted_rows": []})
            col_espaco, col_save, col_del, col_cancel = st.columns([0.4, 0.2, 0.2, 0.2])
           
            #[D]ELETE
            if st.button('Salvar Alterações em Disciplinas  '):
                estado_editor = st.session_state.get("disc_editor", {})
                linhas_editadas = estado_editor.get("edited_rows", {})

                if linhas_editadas:
                    for idx_linha, alteracoes in linhas_editadas.items():
                        tarefa_id = int(df_editado.iloc[idx_linha]['id'])
                        if 'nome' in alteracoes and alteracoes['nome']:
                            alteracoes['nome'] = str(alteracoes['nome'])
                        api.api_patch('disciplinas', tarefa_id, alteracoes)
                    st.success('Tarefas atualizadas!')
                    st.rerun()
                else:
                    st.info('Nenhuma alteração detectada.')

            # [D]ELETE
            id_del = st.number_input('ID da tarefa para remover', min_value=1, step=1)
            if st.button('Remover disciplinas', type='primary'):
                api.api_delete('disciplinas', id_del)
                st.success('disciplinas removida!')
                st.rerun()
                            
        else:
            st.error("As colunas 'id' e 'nome' não foram encontradas na tabela de disciplinas.")
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
                response=api.api_post('provas', {
                    'conteudo': conteudo,
                    'data': data.isoformat(),
                    'horario': horario,
                    'nota': nota,
                    'disciplinas_id': opcoes_d[d_escolhida]

                })
            time.sleep(1)
            erro= response.status_code
            if erro == 200:
                st.success('Prova cadastrada com sucesso!')
                st.rerun()
            else:
                st.warning(erro )
                st.error('Erro ao cadastrar prova.')
                

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
    st.set_page_config(
        page_title="EduTrack AI",
        layout="wide"
    )

    # -----------------------------
    # Inicialização do session_state
    # -----------------------------
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "tema_claro_ativo" not in st.session_state:
        st.session_state.tema_claro_ativo = True
    if st.session_state.tema_claro_ativo:
        aplicar_tema_claro_user()
    else:
        aplicar_tema_escuro()

    # -----------------------------
    # Recupera login pelo cookie
    # -----------------------------
    if not st.session_state.logged_in:
        cookie_token = st.context.cookies.get("auth_token")

        if cookie_token:
            st.session_state.auth_token = cookie_token
            st.session_state.logged_in = True
            st.session_state.login_time = datetime.now()

    # -----------------------------
    # Expiração da sessão
    # -----------------------------
    if (
        st.session_state.logged_in
        and "login_time" in st.session_state
    ):
        if datetime.now() - st.session_state.login_time > timedelta(hours=24):
            st.session_state.clear()
            delete_cookie("auth_token")
            st.session_state.logged_in = False
            st.rerun()

    # -----------------------------
    # Tela de login
    # -----------------------------
    if not st.session_state.logged_in:
        tela_acesso()
        return

    # -----------------------------
    # Garante que o cookie exista
    # -----------------------------
    if not st.context.cookies.get("auth_token"):
        set_cookie("auth_token", st.session_state.auth_token)

    # -----------------------------
    # Sidebar
    # -----------------------------
    with st.sidebar:

        st.title("EduTrack AI")

        menu = st.radio(
            "Gerenciar:",
            [
                "Painel Geral",
                "Professores",
                "Disciplinas",
                "Tarefas/Notas",
                "Projetos",
                "Minhas provas",
            ],
        )

        st.markdown("---")

        # Botão de tema
        if st.session_state.tema_claro_ativo:

            if st.button(
                "🌙 Tema Escuro",
                use_container_width=True,
            ):
                st.session_state.tema_claro_ativo = False
                st.session_state.tema_escuro_ativo = True
                st.rerun()

        else:

            if st.button(
                "☀️ Tema Claro",
                use_container_width=True,
            ):
                st.session_state.tema_escuro_ativo = False              
                st.session_state.tema_claro_ativo = True
                st.rerun()

        st.markdown("---")

        # Logout
        if st.button(
            "Sair",
            use_container_width=True,
        ):
            st.session_state.clear()
            delete_cookie("auth_token")
            st.rerun()

    # -----------------------------
    # Navegação
    # -----------------------------
    match menu:

        case "Painel Geral":
            modulo_dashboard()

        case "Disciplinas":
            modulo_disciplinas()

        case "Professores":
            modulo_professores()

        case "Projetos":
            modulo_projetos()

        case "Tarefas/Notas":
            modulo_tarefas()


        case "Minhas provas":
            modulo_provas()
           

if __name__ == "__main__":
    main()
