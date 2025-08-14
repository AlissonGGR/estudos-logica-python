#Criar algumas rotinas basicas em Python

def soma(a, b):
    """Retorna a soma de dois números."""
    return a + b

def eh_par(n):
    """Verifica se um número é par."""
    return n % 2 == 0

def maior_elemento(lista):
    """Retorna o maior elemento de uma lista."""
    if not lista:
        return None
    return max(lista)

def inverter_string(s):
    """Inverte uma string."""
    return s[::-1]

def contar_vogais(s):
    """Conta o número de vogais em uma string."""
    vogais = 'aeiouAEIOU'
    return sum(1 for char in s if char in vogais)