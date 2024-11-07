import hashlib
from datetime import datetime, timedelta
import re

def makeUniqueHash(input_string):
    # Cria um objeto de hash SHA-256
    sha256 = hashlib.sha256()
    
    # Atualiza o objeto de hash com a string de entrada codificada
    sha256.update(input_string.encode('utf-8'))
    
    # Retorna o hash hexadecimal gerado
    return sha256.hexdigest()

def getData():
    # Obter a data e hora atuais
    agora = datetime.now()
    
    # Formatar a data e hora no formato desejado
    data_hora_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')
    
    return data_hora_formatada

def is_password_strong(password):
    # Verifica se a senha tem pelo menos 8 caracteres
    if len(password) < 8:
        return False, "The password must be at least 8 characters long."

    # Verifica se a senha contém pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', password):
        return False, "The password must contain at least one uppercase letter."

    # Verifica se a senha contém pelo menos uma letra minúscula
    if not re.search(r'[a-z]', password):
        return False, "The password must contain at least one lowercase letter."

    # Verifica se a senha contém pelo menos um dígito
    if not re.search(r'\d', password):
        return False, "The password must contain at least one digit."

    # Verifica se a senha contém pelo menos um caractere especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "The password must contain at least one special character."
    
    return True, ""

def are_fields_empty(fields):
    for field_name, field_value in fields.items():
        if field_value is None:
            return True, f"The field {field_name} cannot be empty."
        if not field_value.strip():
            return True, f"The field {field_name} cannot be empty."
    return False, ""