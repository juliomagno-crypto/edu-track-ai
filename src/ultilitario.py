import re

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
    erros = []
    if len(senha) < 8:
        erros.append('A senha deve ter no mínimo 8 caracteres.')
    if not any(char.isupper() for char in senha):
        erros.append('A senha deve conter pelo menos uma letra maiúscula.')
    if not any(char.islower() for char in senha):
        erros.append('A senha deve conter pelo menos uma letra minúscula.')
    if not any(char.isdigit() for char in senha):
        erros.append('A senha deve conter pelo menos um número.')
    if not any(not char.isalnum() for char in senha):
        erros.append('A senha deve conter pelo menos um caractere especial.')
    return erros

def valida_nome(nome):
    """Valida se o nome do usuário é válido (para cadastro de conta)."""
    erros = []
    if len(nome) > 255:
        erros.append('O nome não pode passar de 255 caracteres.')
    espacos = nome.count(' ')
    if espacos < 1:
        erros.append('O nome deve conter pelo menos um sobrenome, coloque seu nome completo.')
    if espacos > 15:
        erros.append('O nome não pode conter mais de 15 espaços.')
    return erros

def valida_email(email):
    """Valida o formato do e-mail: sem espaços, sem vírgulas, e formato correto."""
    if not email:
        return False

    # Verifica se tem espaços ou vírgulas
    if ' ' in email or ',' in email:
        return False

    if email.count('@') != 1:
        return False
    
    partes = email.split('@')
    usuario = partes[0]
    dominio_completo = partes[1]

    # Garante que haja pelo menos 2 caracteres antes do @
    if len(usuario) < 2:
        return False
    
    # Verifica se tem ponto no domínio e se há algo entre o @ e o primeiro ponto
    if '.' not in dominio_completo:
        return False
    
    # Divide o domínio para verificar a "palavra" entre @ e .
    nome_dominio = dominio_completo.split('.')[0]
    if len(nome_dominio) < 1:
        return False
        
    return True

def main():
    print('É uma lib')


if __name__ == '__main__':
    main()
