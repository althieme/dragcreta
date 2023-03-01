#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import decreta_bot_v1_semtoken as bot

def testa_conta_palavras():
    artigo = "texto do artigo do decreto que está sendo gravado. Esse decreto tem a palavra decreto 3 vezes e a palavra artigo 2 vezes. Fora outras tantas. 100"
    contador = dict()
    bot.conta_palavras(artigo, contador)
    expected = {'texto': 1, 'artigo': 2, 'decreto': 3, 'está': 1, 'sendo': 1, 'gravado': 1, 'Esse': 1, 'tem': 1, 'palavra': 2, 'vezes': 2, 'Fora': 1, 'outras': 1, 'tantas': 1}
    print('testa_conta_palavras\t\t', contador == expected)
         
def testa_dia_decreto():
    semana_de_sabado_a_quinta = ['2023-02-25', '2023-02-26', '2023-02-27', '2023-02-28', '2023-03-01', '2023-03-02']
    semana_sem_sexta = list(map(lambda d: datetime.fromisoformat(d), semana_de_sabado_a_quinta))
    uma_sexta = datetime.fromisoformat('2023-03-03')
    
    for s in semana_sem_sexta:
        if bot.dia_decreto(s):
            print('testa_dia_decreto\t\t', False)
            return

    print('testa_dia_decreto\t\t', bot.dia_decreto(uma_sexta))

def testa_redige_decreto():
    data = datetime.fromisoformat('2023-03-03')
    data_fim = datetime.fromisoformat('2023-03-07')
    decreto = bot.redige_decreto(['artigo A', 'artigo B'], 4, data, data_fim)
    
    deve_conter = ['DECRETO Nº 4/2023, 3 de março de 2023', 'artigo A\nartigo B', 'às 23:59 de 7 de março de 2023.']

    print('testa_redige_decreto\t\t', False not in list(map(lambda f:  f in decreto, deve_conter)))

def testa_gera_decreto():
    data = datetime.fromisoformat('2023-03-03')
    data_fim = datetime.fromisoformat('2023-03-08')

    decreto = bot.gera_decreto(['artigo A', 'artigo B'], 4,'borboleta', data)

    deve_conter = ['DECRETO Nº 4/2023', '3 de março de 2023', 'Art. 2º artigo A;\nArt. 3º artigo B;\nArt. 4º Determina-se a', 'às 23:59 de 5 de março de 2023.', '(ou o desenho de) borboleta como inspiração']
    print('testa_gera_decreto\t\t', False not in list(map(lambda f:  f in decreto, deve_conter)))

def testa_gera_decreto_fim_de_ano():
    data = datetime.fromisoformat('2023-12-31')

    decreto = bot.gera_decreto(['artigo A', 'artigo B'], 4,'borboleta', data)

    deve_conter = ['DECRETO Nº 4/2023', '31 de dezembro de 2023', 'Art. 2º artigo A;\nArt. 3º artigo B;\nArt. 4º Determina-se a', 'às 23:59 de 2 de janeiro de 2024.', '(ou o desenho de) borboleta como inspiração', 'Art. 5º Estão liberadas']
    print('testa_gera_decreto_fim_de_ano\t', False not in list(map(lambda f:  f in decreto, deve_conter)))


if __name__ == '__main__':
    testa_conta_palavras()
    testa_dia_decreto()
    testa_redige_decreto()
    testa_gera_decreto()
    testa_gera_decreto_fim_de_ano()
