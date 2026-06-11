import re
import time
import streamlit as st
def valida_caixa(nome):
    if nome =="":
        return False
    else:
        return True
def contar_caracteres(texto):
    """Conta quantos caracteres tem no parâmetro e retorna o valor como inteiro."""
    if not texto:
        return 0
    return len(texto)

def exclui_espaco(texto):
    """Remove espaços no começo e no final da string."""
    if not texto:
        return ""
    return texto.strip()

def limpar_texto(texto):
    """Remove espaços em branco extras do texto (múltiplos espaços internos e bordas)."""
    if not texto:
        return ""
    return re.sub(r'\s+', ' ', texto).strip()

def valida_senha(senha):
    """Valida se a senha atende aos requisitos de segurança."""
     
    if contar_caracteres(senha) > 255:
        st.error('A senha não pode passar de 255 caracteres.')
        return
    if len(senha) < 8:
        st.error('A senha deve ter no mínimo 8 caracteres.')
        return
    if not any(char.isupper() for char in senha):
        st.error('A senha deve conter pelo menos uma letra maiúscula.')
        return
    if not any(char.islower() for char in senha):
        st.error('A senha deve conter pelo menos uma letra minúscula.')
        return
    if not any(char.isdigit() for char in senha):
        st.error('A senha deve conter pelo menos um número.')
        return
    if not any(not char.isalnum() for char in senha):
        st.error('A senha deve conter pelo menos um caractere especial.')
        return
    return True

def valida_nome(nome):
    """Valida se o nome do usuário é válido (para cadastro de conta)."""
    
    if contar_caracteres(nome) > 255:
         st.error('O nome não pode passar de 255 caracteres.')
         return

    espacos = nome.count(' ')
    if espacos < 1:
        st.error('O nome deve conter pelo menos um sobrenome, coloque seu nome completo.')
        return
    if espacos > 15:
        st.error('O nome não pode conter mais de 15 espaços.')
        return 
    return True

def valida_email(email):
    """Valida o formato do e-mail: sem espaços, sem vírgulas, e formato correto."""
    
    if not  valida_caixa(email):
        erro=st.error('Erro ao cadastrar usuário; Necessário inserir um e-mail ')
        return
    if contar_caracteres(email) > 255:
        st.error('Email não pode passar de 255 caracteres')
        return 
    # Verifica se tem espaços ou vírgulas
    if ' ' in email or ',' in email:
        nomErro=st.error('Não é permitido inserir espaços ou vírgulas no email' )
        return
    
    if email.count('@') != 1:
        nomErro=st.error('Pemitido no máximo 1 "@" no email ')
        return
    
    partes = email.split('@')
    usuario = partes[0]
    dominio_completo = partes[1]

    # Garante que haja pelo menos 2 caracteres antes do @
    if len(usuario) < 2:
        nomErro=st.error('Necessário pelo menos 2 caracteres antes do @ ')
        return
    # Verifica se tem ponto no domínio e se há algo entre o @ e o primeiro ponto
    if '.' not in dominio_completo:
        nomErro=st.error('Necessário inserir um ou mais "." no email')
        return
    # Divide o domínio para verificar a "palavra" entre @ e .
    nome_dominio = dominio_completo.split('.')[0]
    if len(nome_dominio) < 1:
        nomErro=st.error('Não é possível menos de 1 @ no email')
        return
    return True

def main():
    print('É uma lib')


if __name__ == '__main__':
    main()
