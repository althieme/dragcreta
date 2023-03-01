#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot decretador
Created on Tue Feb 21 09:49:01 2023

@author: andrethieme
"""
from telegram import Update
import time
import logging
import string
from datetime import datetime
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
""" Exemplos de output de Update:
Update(message=Message(channel_chat_created=False, chat=Chat(id=-1001887231210, title='Testes e melhorias', type=<ChatType.SUPERGROUP>), date=datetime.datetime(2023, 2, 26, 14, 27, 4, tzinfo=datetime.timezone.utc), delete_chat_photo=False, from_user=User(first_name='André L.', id=157762204, is_bot=False, language_code='pt-br', last_name='Thieme', username='alThieme'), group_chat_created=False, message_id=133, supergroup_chat_created=False, text='já percebi que tinha um typo e arrumei outros detalhes. acho que a gente pode liberar a versão beta semana que vem 😜'), update_id=91245966)
"""

TOKEN =  'TOKEN'# token obtido com o botfather 
itens = []
grupo = 'chat_id'

meses = 'Jan,Feb,Mar,Abr,Mai,Jun,Jul,Set,Out,Nov,Dez'.split(',')

async def enviar_mensagem(chat_id: str, context: ContextTypes.DEFAULT_TYPE, texto: str):
    await context.bot.send_message(chat_id=chat_id, text= texto)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensagem(update.effective_chat.id, context, "Vamos adicionar uma resolução ao decreto desta semana! Basta enviar uma frase em estilo de uma resolução que ela será incluída no Decreto.\nExemplo: \nEstimula-se a postagem de pets, fofices, drinks, nuvens, roupinhas de bebês e o que mais achar fofo e que trará sorrisos para o grupo.\n(Não há necessidade de colocar Art ou nada do tipo, isso será adicionado automaticamente)")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensagem(update.effective_chat.id, context, """Funciona assim:
Seu texto será adicionado ao decreto da semana. O Decreto será emitido assim que um dos admins decretar no grupo geral. 
Os artigos são definidos pelo bot e serão organizados para o Decreto que acontece semanalmente.
""")

async def salvaItem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != grupo:
        item = update._effective_message.text
        context.bot_data[item] = update.effective_user.id
        itens.append(item)
        await enviar_mensagem(update.effective_chat.id, context, f'Obrigada {update.effective_user.first_name}, já anotei seu artigo aqui!')
        print('Novo item!')
    
    else:
        conta_palavras(update._effective_message.text, context.chat_data)

#Criar um contador de palavras dentro do DdG, tirando palavras da lista de exclusão, para gerar uma tatuagem automática.
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

async def decreta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_group_id = update.effective_chat.id
    if chat_group_id != grupo:
        await enviar_mensagem(chat_group_id, context, 'Esse comando só pode ser usado no grupo do Dragões de Garagem!')
        return
    
    hoje = datetime.now()
    if not dia_decreto(hoje):
        await enviar_mensagem(chat_group_id, context, 'Você está querendo fazer festa antes do tempo! Já já chega a sexta')
        print(time.asctime())
        return

    itens = context.bot_data
    palavras = context.chat_data
    duplas = sorted(palavras.items(), key=lambda dupla: dupla[1], reverse = True)
    figura = duplas[0][0]

    mes = nome_mes(hoje)
    ano = hoje.year
    numeroDec = str(update.effective_message.id)[-3:]
    numeroArt = 2
    
    decreto = f""" DECRETO Nº {numeroDec}/{ano},  {mes} de {ano}

A ministra robótica dracônica da República Draconiana, desenvolvida para organizar os assuntos de lazer, no uso da atribuição que lhe confere o artigo 6 das leis draconianas decreta: 

Art. 1º Suspende-se o poder de veto dos agremiados desta nobre instituição enquanto perdurar este decreto\n"""
    for art in itens:
        decreto += f'Art. {numeroArt}º {art};\n'
        numeroArt += 1
        dataFim = int(time.asctime()[8:10]) + 2
    if dataFim > 28 and mes == 'Feb':
        dataFim = dataFim - 28
        mes = 'Mar'
        decreto += f'Art{numeroArt}º Determina-se o desenho de {figura} como o símbolo para todas as tatuagens a serem realizadas nesse períoto;\n'
    elif dataFim > 30 and mes in ['Abr', 'Jun','Set','Nov']:
        dataFim = dataFim - 30
        numMes = meses.idex(mes) + 1
        mes = meses[numMes]
        decreto += f'Art{numeroArt}º Determina-se o desenho de {figura} como o símbolo para todas as tatuagens a serem realizadas nesse períoto;\n'
    elif dataFim > 31 and mes in ['Jan', 'Mar', 'Mai', 'Jul', 'Ago', 'Out']:
        dataFim = dataFim - 31
        numMes = meses.index(mes) + 1
        mes = meses[numMes]
    elif dataFim > 31 and mes == 'Dez':
        decreto += f'Art{numeroArt}º Estão liberadas as aberturas de garrafa de espumantes com pompa e circunstância!\n'
        dataFim = 1
        mes = 'Jan'
    else:
        decreto += f'Art. {numeroArt}º Determina-se a palavra (ou o desenho de) {figura} como inspiração para todas as tatuagens a serem realizadas neste período;\n'
    decreto += f"""\nEste decreto entra em vigor na data de sua publicação e encerra-se às 23:59 de {dataFim} de {mes} de {ano}.

Decreto liberado, cumpra-se
#DecretoRobotico"""
    await enviar_mensagem(chat_group_id, context, decreto)
    print(context.bot_data)
    print(context.chat_data)
    context.bot_data.clear()
    context.chat_data.clear()
    

def dia_decreto(data: datetime):
    SEXTA = 4
    return SEXTA == data.weekday()

def nome_mes(data: datetime):
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
    
    return nomes_dos_meses[data.month]

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
