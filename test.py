#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from decreta_bot_v1_semtoken import ttt
import string

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

if __name__ == '__main__':
    artigo = "texto do artigo do decreto que está sendo gravado. Esse decreto tem a palavra decreto 3 vezes e a palavra artigo 2 vezes. Fora outras tantas. 100"
    contador = dict()
    conta_palavras(artigo, contador)
    expected = {'texto': 1, 'artigo': 2, 'decreto': 3, 'está': 1, 'sendo': 1, 'gravado': 1, 'Esse': 1, 'tem': 1, 'palavra': 2, 'vezes': 2, 'Fora': 1, 'outras': 1, 'tantas': 1}
    print(contador == expected) 
    
