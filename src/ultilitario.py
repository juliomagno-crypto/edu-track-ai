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
    """Valida o formato do e-mail."""
    if not email:
        return False

    exclui_espaco(email)

    if email.count('@') != 1:
        return False
    # Garante que haja pelo menos 2 caracteres antes do @
    if len(email.split('@')[0]) < 2:
        return False
    if '.' not in email:
        return False
    return True

def main():
    print('É uma lib')


if __name__ == '__main__':
    main()
