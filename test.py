#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import time
from datetime import datetime

grupo = "111"

def conta_palavras(s: str, contador_de_palavras: dict):
    texto = s
    lista_exclusao = 'a,e,o,um,uma,de,que,por,se,em,ou,como,é,da,com,me,do,não,eu,no,na,porque,assim,então'.split(',')
    
    for c in string.punctuation:
        texto = texto.replace(c, '')
    
    palavras = list(filter(lambda p: p not in lista_exclusao and not p.isdigit(), texto.split(' ')))
    
    for palavra in palavras:
        if palavra not in contador_de_palavras:
            contador_de_palavras[palavra] = 1
        else:
           contador_de_palavras[palavra] += 1

def testa_conta_palavras():
    artigo = "texto do artigo do decreto que está sendo gravado. Esse decreto tem a palavra decreto 3 vezes e a palavra artigo 2 vezes. Fora outras tantas. 100"
    contador = dict()
    conta_palavras(artigo, contador)
    expected = {'texto': 1, 'artigo': 2, 'decreto': 3, 'está': 1, 'sendo': 1, 'gravado': 1, 'Esse': 1, 'tem': 1, 'palavra': 2, 'vezes': 2, 'Fora': 1, 'outras': 1, 'tantas': 1}
    print('testa_conta_palavras\t\t', contador == expected)
         

def dia_decreto(chat_id: str, data: datetime):
    SEXTA = 4
    return chat_id == grupo and SEXTA == data.weekday()

def testa_dia_decreto():
    semana_de_sabado_a_quinta = ['2023-02-25', '2023-02-26', '2023-02-27', '2023-02-28', '2023-03-01', '2023-03-02']
    semana_sem_sexta = list(map(lambda d: datetime.fromisoformat(d), semana_de_sabado_a_quinta))
    uma_sexta = datetime.fromisoformat('2023-03-03')
    
    for s in semana_sem_sexta:
        if dia_decreto("111", s):
            print('testa_dia_decreto\t\t', False)
            return

    print('testa_dia_decreto\t\t', dia_decreto("111", uma_sexta))

if __name__ == '__main__':
    testa_conta_palavras()
    testa_dia_decreto()
