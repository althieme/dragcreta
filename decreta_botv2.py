#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot decretador version 2.5
Created on Tue Feb 21 09:49:01 2023
Last update Sat Jul 29 17:31:34 2023

@author: andrethieme
"""
from telegram import Update 
from time import sleep
import logging
import string
import config
# from duckduckgo_search import ddg #Brincar de escolher uma música automática (também teria que incluir o choice)
from datetime import datetime, date
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = config.TOKEN
grupo = config.grupo
testes = config.testes

async def enviar_mensagem(chat_id: str, context: ContextTypes.DEFAULT_TYPE, texto: str):
    await context.bot.send_message(chat_id=chat_id, text= texto) #Não é parse_mode = 'MarkdownV2, pois dá erro de ponto final (.)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensagem(update.effective_chat.id, context, "Vamos adicionar uma resolução ao decreto desta semana! Basta enviar uma frase em estilo de uma resolução que ela será incluída no Decreto.\nUm item de um decreto geralmente começa com um verbo flexionado em impessoal, indicando alguma informação de coisas estabelecidas, definidas ou indicadas. Exemplo: \nEstimula-se a postagem de pets, fofices, drinks, nuvens, roupinhas de bebês e o que mais achar fofo e que trará sorrisos para o grupo.\n(Não há necessidade de colocar Art ou nada do tipo, isso será adicionado automaticamente)")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensagem(update.effective_chat.id, context, """Funciona assim:
Em um chat privado comigo, após o /start você pode me enviar o seu texto, diretamente, sem precisar de nenhum comando.
Seu texto será adicionado ao decreto da semana. O Decreto será emitido assim que um dos admins decretar no grupo geral.
Um item de um decreto geralmente começa com um verbo flexionado em impessoal, indicando alguma informação de coisas estabelecidas, definidas ou indicadas. Um exemplo:
Libera-se passar o fim de semana aproveitando para botar jogos, séries e filmes em dia e viver a base de delivery pra não ter que se preocupar com afazeres domésticos

Os artigos são definidos por mim, você não precisa escrever artigo nem colocar ponto-e-vírgula (;) após o item. Quem faz a enumeração sou eu mesma, para o Decreto que acontece semanalmente. O seu item será salvo apenas até o próximo decreto.
""")

async def salvaItem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update._effective_message.text
    quem = update.effective_user.first_name
    hoje = datetime.today()
    ff = [4,3,2,1,0,6,5]
    dia_semana = hoje.weekday()
    diaordinal = date.toordinal(hoje) + ff[dia_semana]
    if str(update.effective_chat.id) not in [grupo, testes]:     
        doc = f'./itensde_{diaordinal}' 
        documento = open(doc, 'a')
        item = item + '\n'
        documento.write(item)
        documento.close()
        sleep(1)
        await enviar_mensagem(update.effective_chat.id, context, f'Hey {quem}, que contribuição phodástica, você é incrível! Já registrei aqui')
    else:
        doc = f'./figde_{diaordinal}' 
        documento = open(doc, 'a')
        item = item + ' '
        documento.write(item)
        documento.close()
        contador(quem, context.chat_data)

def contador(quem, lista):
	if quem in lista:
		lista[quem] += 1
	else:
		lista[quem] = 1
	


def conta_palavras(doc):
    s = open(doc, 'r')
    texto = s.read()
    texto = texto.lower()
    contador_de_palavras = {}
    lista_exclusao = 'uma,que,por,como,com,não,porque,assim,então,quem,sobre,atrás,ume,hoje,hora,ontem,amanhã,mas,também,talvez,até,seu,sua,meu,minha,meus,minhas,seus,suas,para,mais,mesmo,nenhum,nada,ser,porem,porquê,para,foi,ele,ela'.split(',')
    texto = texto.replace('\n', ' ')
    for c in string.punctuation:
        texto = texto.replace(c, '')
    
    palavras = list(filter(lambda p: p not in lista_exclusao and len(p) > 3, texto.split(' ')))
    
    for palavra in palavras:
        if palavra not in contador_de_palavras:
            contador_de_palavras[palavra] = 1
        else:
           contador_de_palavras[palavra] += 1
    duplas = sorted(contador_de_palavras.items(), key=lambda dupla: dupla[1], reverse = True)
    figura = duplas[3][0]
    return figura

def maior_palavra(doc):
    s = open(doc, 'r')
    text = s.read()
    texto = text.lower()
    texto = texto.replace('\n', ' ')
    for c in string.punctuation:
        texto = texto.replace(c, '')
    
    palavras = list(filter(lambda p: len(p) > 3 and p[:3] not in 'httpwwwberthmastwi', texto.split(' ')))
    maior = ''
    for palavra in palavras:
        if len(palavra) > len(maior):
            maior = palavra
    return maior

async def decreta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_group_id = update.effective_chat.id
    if str(chat_group_id) not in [testes, grupo]:
        await enviar_mensagem(chat_group_id, context, 'Esse comando só pode ser usado no grupo do Dragões de Garagem!')
        return
    
    hoje = datetime.now()
    dragoes = 'alThieme,eltonfc,mahideia,tupag,mvcortezi,LucasDdG,gabi_sobral,moleculoide,pedrotaucce,gracieleao,nataliapessoni,TabataBohlen,knicolasdias,rogbitt,nataliaguiar'.split(',')
    if not dia_decreto(hoje) and update.effective_user.username not in dragoes:
        await enviar_mensagem(chat_group_id, context, 'Você está querendo fazer festa antes do tempo! Por favor, procure um dos admins')
        return
    
    dia_semana = 4 - hoje.weekday()
    diaordinal = date.toordinal(hoje) + dia_semana
    try:
    	docItens = open(f'./itensde_{diaordinal}', 'r')
    	itens = docItens.readlines()
    except:
    	itens = ['Relembra aos agremiados que este decreto só é possível com a contribuição de cada um de vocês, sus lindes, envie seu item de decreto para mim, me pergunte como em privado ']
    
    docFig = f'./figde_{diaordinal}'
    dia = hoje.day
    mes = nome_mes(hoje, 0)
    ano = hoje.year
    numeroDec = str(update.effective_message.id)[-3:]
    numeroArt = 2
    lista = context.chat_data

    if context.args == []:
        due = 2
    else:
        due = int(context.args[0])
        
    decreto = f""" DECRETO Nº {numeroDec}/{ano},  {mes} de {ano}

A ministra robótica dracônica da República Draconiana, desenvolvida para organizar os assuntos de lazer, no uso da atribuição que lhe confere o artigo 6 das leis draconianas decreta: 

Art. 1º Suspende-se o poder de veto dos agremiados desta nobre instituição enquanto perdurar este decreto\n"""
    if len(lista) > 0:
    	duplas = sorted(lista.items(), key=lambda dupla: dupla[1], reverse = True)
    	nome = duplas[0][0]
    	decreto += f'Art. {numeroArt}º Parabeniza {nome} por sua submissão numerosa de informações revisadas por pares a este grupo, segundo o Artigo 17º da Constituição (lei Sarzi-Couto);\n'
    	numeroArt += 1
    for art in itens:
        decreto += f'Art. {numeroArt}º {art[:-1]};\n'
        numeroArt += 1
    dataFim = hoje.day + due
    figura = conta_palavras(docFig)
    if dataFim > 28 and mes == 'fevereiro':
        dataFim = dataFim - 28
        mes = 'março'
        decreto += f'Art. {numeroArt}º Orienta-se a escrita élfica de \"{figura}\" como o símbolo para todas as tatuagens a serem realizadas nesse período;\n'
    elif dataFim > 30 and mes in ['abril', 'junho','setembro','novembro']:
        dataFim = dataFim - 30
        mes = nome_mes(hoje, 1)
        decreto += f'Art. {numeroArt}º Determina-se o que se utilize a palavra \"{figura}\" em lettering para todas as tatuagens a serem realizadas nesse período;\n'
    elif dataFim > 31 and mes in ['janeiro', 'março', 'maio', 'julho', 'agosto', 'outubro']:
        dataFim = dataFim - 31
        mes = nome_mes(hoje, 1)
        decreto += f'Art. {numeroArt}º Determina-se a palavra \"{figura}\" em chinês como o símbolo para todas as tatuagens a serem realizadas nesse período;\n'
    elif dataFim > 31 and mes == 'dezembro':
        decreto += f'Art. {numeroArt}º Estão liberadas as aberturas de garrafa de espumantes com pompa e circunstância!\n'
        dataFim = 1
        mes = 'janeiro'
    else:
        figura = maior_palavra(docFig)
        decreto += f'Art. {numeroArt}º Determina-se a palavra (ou o desenho de) \"{figura}\" como inspiração para todas as tatuagens a serem realizadas neste período;\n'
    decreto += f"""\nEste decreto entra em vigor na data de sua publicação e encerra-se às 23:59 de {dataFim} de {mes} de {ano}.

Decreto liberado, cumpra-se
#DecretoRobotico"""
    await enviar_mensagem(chat_group_id, context, decreto)
    context.chat_data = {}
    

def dia_decreto(data: datetime):
    SEXTA = 4
    return SEXTA == data.weekday()

def nome_mes(data: datetime, n: int):
    nomes_dos_meses = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }
    
    return nomes_dos_meses[data.month + n]

if __name__ == '__main__':
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    decreta_handler = CommandHandler('decreta', decreta)
    salvaItem_handler = MessageHandler(filters.TEXT, salvaItem)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(decreta_handler)
    application.add_handler(salvaItem_handler)
    
    application.run_polling()

