import telebot
import configbot
from threading import Thread
import datetime
import requests
import time


import botoes
from gerarid import gerar_identificador



token_bot = configbot.bot_principal_token
perc_btccred = float(configbot.taxa_porcentagem / 100)
taxa_servico = configbot.taxa_servico_config
parcelas = configbot.parcelas_config
acrescimo_price = configbot.spread_cotacao
par01 = "BTCBRL"



bot = telebot.TeleBot(token_bot)


# Comando /start
@bot.message_handler(commands=['start'])
def handle_pix_command(message):

    mensagem_resposta = f"*Bem-vindo, escolha uma das opções abaixo!*\n\n"
    mensagem_resposta += f"• *[BTC]* - Faça uma simulação de preço.\n"
    mensagem_resposta += f"• *[Fees]* - Veja a taxa estimada da rede Bitcoin\n"
    mensagem_resposta += f"• *[Informações]* - Veja as nossas informações principais\n"
    mensagem_resposta += f"• *[Empréstimo]* - Simule um empréstimo colateralizado em BTC\n"
        
    bot.send_message(message.chat.id,
                    mensagem_resposta,
                    parse_mode="Markdown",
                    reply_markup=botoes.menu_01())
        
# Função para responder a qualquer mensagem recebida com uma mensagem padrão
@bot.message_handler(func=lambda message: True)
def responder_mensagem_padrao(message):
    mensagem_resposta = f"*Bem-vindo, escolha uma das opções abaixo!*\n\n"
    mensagem_resposta += f"• *[BTC]* - Faça uma simulação de preço.\n"
    mensagem_resposta += f"• *[Fees]* - Veja a taxa estimada da rede Bitcoin\n"
    mensagem_resposta += f"• *[Informações]* - Veja as nossas informações principais\n"
    mensagem_resposta += f"• *[Empréstimo]* - Simule um empréstimo colateralizado em BTC\n"
    bot.send_message(message.chat.id,
                     mensagem_resposta,
                     parse_mode="Markdown",
                     reply_markup=botoes.menu_01())
    
    
    
@bot.callback_query_handler(func=lambda call: call.data == 'btn_btc')
def btn_chamar_pricebtc(call):
    ask_for_value(call.message)

def ask_for_value(mensagem):
    mensagem00 = f'💯 *Informe um valor que deseja comprar em BRL e a taxa %.*\n'
    mensagem00 += f'*Ex:* _100.99 10_\n'
    bot.send_message(mensagem.chat.id,
                    mensagem00,
                    parse_mode="Markdown")

    # Utilize 'mensagem' diretamente ao invés de 'mensagem.chat' para acessar as informações corretas.
    bot.register_next_step_handler(mensagem, lambda msg: responder_BTC(msg, mensagem.chat.id, mensagem.chat.username))

def responder_BTC(mensagem, user_id, username):
    try:
        a, b = mensagem.text.split()
        valor_compra = float(a)
        taxa_perc = float(b)

        if not b.replace('.', '').isdigit():
            # 'isdigit()' não permite pontos decimais, por isso, removemos os pontos e verificamos se é numérico.
            raise ValueError()

        if taxa_perc < 0:
            # Se a taxa for negativa, levanta um erro para tratamento.
            raise ValueError()

        url = f"https://www.binance.com/api/v3/ticker/price?symbol={par01}"
        requisicao = requests.get(url)

        if requisicao.status_code == 200:
            resposta = requisicao.json()
            data = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            cotacao01 = float(resposta["price"])

            # O cálculo da cotação P2P estava incorreto, substituí pelo valor correto.
            price_compra = cotacao01 + (cotacao01 * taxa_perc / 100)
            quantidade = valor_compra / price_compra

            mensagem_resposta = "   🟢    *Dados da consulta*   🟢   \n\n\n"
            mensagem_resposta += f"• *Usuário:* _@{username}_\n"
            mensagem_resposta += f"• *Valor R$:* `{valor_compra:.2f}`\n"
            mensagem_resposta += f"• *Cotação:* R$ `{cotacao01:.2f}`\n"
            mensagem_resposta += f"• *Cotação P2P:* R$ `{price_compra:.2f}`\n"
            mensagem_resposta += f"• *Qtd. BTC:* `{quantidade:.8f}`\n"
            mensagem_resposta += f"• *Taxa P2P %:* `{taxa_perc:.2f}`\n"
            mensagem_resposta += f"• *Data:* _{data}_\n\n\n"
            mensagem_resposta += f"• *Para fazer uma nova consulta, clique em um dos botões abaixo!*"

            # Utilize 'user_id' ao invés de 'mensagem.chat.id', pois 'mensagem' agora é uma Message, não um Chat.
            bot.send_message(mensagem.chat.id,
                         mensagem_resposta,
                         parse_mode="Markdown",
                         reply_markup=botoes.menu_01())
        else:
            bot.send_message(mensagem.chat.id,
                         "*🚫 Desculpe-me, não consegui acessa a API*",
                         parse_mode="Markdown",
                         reply_markup=botoes.menu_01())

    except ValueError:
        bot.send_message(user_id,
                         "\nValor inválido!\n\n✅ Forma correta ex: R$ 10.00\n- Exemplos: 10 | 10.00 | 10.50\n\n❌ Forra errada ex: R$ 10,00\n- Exemplos: 10,00 | 10,50 \n\n👉🏼 Clique em um dos botões para recomeçar\n",
                         parse_mode="Markdown",
                         reply_markup=botoes.menu_01())


@bot.callback_query_handler(func=lambda call: call.data == 'btn_fees')
def btn_chamar_fees(call):
    get_fees(call.message)

def get_fees(message):
    # Faça uma solicitação GET à API
    response = requests.get('https://mempool.space/api/v1/fees/recommended')
        
    if response.status_code == 200:
        data = response.json()
            
        # Extrair os dados relevantes da resposta da API
        fastest_fee = data['fastestFee']
        half_hour_fee = data['halfHourFee']
        hour_fee = data['hourFee']
        par01 = "BTCBRL"
        url = f"https://www.binance.com/api/v3/ticker/price?symbol={par01}"
        requisicao = requests.get(url)
        resposta = requisicao.json()
        data = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        cotacao01 = float(resposta["price"])

        taxa_media_btc = 226

        taxa_price_fast = int(fastest_fee * taxa_media_btc)
        taxa_price_half = int(half_hour_fee * taxa_media_btc)
        taxa_price_hour = int(hour_fee * taxa_media_btc)

        valorbrltaxa01 = float((taxa_price_fast / 100000000) * (cotacao01))
        valorbrltaxa02 = float((taxa_price_half / 100000000) * (cotacao01))
        valorbrltaxa03 = float((taxa_price_hour / 100000000) * (cotacao01))

            # Enviar a resposta ao usuário do Telegram
            
        reply = f"💰*TAXAS DE TRANSAÇÃO APROXIMADA*\n\n"
        reply += f"📊*Cotação BTC:* R$"+ format(cotacao01, ".2f") + "\n\n"
        reply += f"🟢 *Rápida:* "+ str(fastest_fee) + " sat/vB - " + str(taxa_price_fast ) + " sats - R$ " + format(valorbrltaxa01, ".2f") + "\n"
        reply += f"🟡 *Média:* "+ str(half_hour_fee) + " sat/vB - " + str(taxa_price_half ) + " sats - R$ " + format(valorbrltaxa02, ".2f") + "\n"
        reply += f"🔴 *Lenta:* "+ str(hour_fee) + " sat/vB - " + str(taxa_price_hour ) + " sats - R$ " + format(valorbrltaxa03, ".2f") + "\n\n"
        reply += f"📅 *Data:* _{data}_\n\n"
        reply += f"👉🏻 _Os valores levam em consideração a taxa média de 226 bytes_\n\n"

        bot.send_message(message.chat.id,
                        reply,
                        parse_mode="Markdown",
                        reply_markup=botoes.menu_01())

    else:
        bot.send_message(message.chat.id,
                         "*🚫 Não foi possível obter os dados da API*", 
                         parse_mode="Markdown",
                         reply_markup=botoes.menu_01())



@bot.callback_query_handler(func=lambda call: call.data == 'btn_info')
def btn_chamar_informacoes(call):
    chamar_informacoes(call.message)

def chamar_informacoes(mensagem):
    mensagem0 = f"• *{configbot.msg_txt01}*\n\n"
    mensagem0 += f"• {configbot.msg_txt02}\n"
    mensagem0 += f"• {configbot.msg_txt03}\n\n"
    mensagem0 += f"• *Telegram:* _{configbot.contato_telegram}_\n"
    mensagem0 += f"• *{configbot.nome_rede_social}:* [Clique aqui]({configbot.link_redesocial})"
    
    # Enviar a mensagem
    sent_message = bot.send_message(mensagem.chat.id,
                                    mensagem0,
                                    parse_mode="Markdown")
    
    # Aguardar 60 segundos antes de excluir a mensagem
    time.sleep(60)
    # Excluir a mensagem
    bot.delete_message(mensagem.chat.id,
                       sent_message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'btn_btccred')
def btn_chamar_pricebtc(call):
    ask_for_btccred(call.message)

def ask_for_btccred(mensagem):
    bot.reply_to(mensagem,
                 f"💯 *Digite um valor que gostaria de pegar emprestado de{par01}.*\n*Ex: R$ 500.00*",
                 parse_mode="Markdown")
    bot.register_next_step_handler(mensagem,
                                   lambda msg: responder9(msg, mensagem.chat.id,
                                                          mensagem.chat.username))


def responder9(mensagem, user_id, username): # PEGANDO A MENSAGEM, ID, NOME DE USUÁRIO
    txid = gerar_identificador()
    try:
        url = f"https://www.binance.com/api/v3/ticker/price?symbol=BTCBRL"
        requisicao = requests.get(url)
        resposta = requisicao.json()
        if requisicao.status_code == 200: #CODIGO DE SUCESSO
            cotacao_binance = float(resposta["price"])
            cotacao = float(cotacao_binance + acrescimo_price)# COTAÇÃO
            data = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            valor1 = float(mensagem.text) # VALOR PASSADO PELO USUÁRIO
            a_pagar = float((valor1 + (valor1 * perc_btccred)) + taxa_servico)
            btc_colateral = float(a_pagar / cotacao) # QUANTIDADE DE BTC EM COLATERAL
            sats = float(btc_colateral * 100000000) # CONVERTENDO SAT   
            liquidacao_mansal = float(btc_colateral / parcelas) 
            parcela_fiat = (a_pagar / parcelas)
            message_resposta = f"*EMPRÉSTIMO COLATERALIZADO EM ₿ITCOIN*\n\n" 
            message_resposta += f"• *Dados usuário*\n"
            message_resposta += f"• *seu ID:* `{user_id}`\n"
            message_resposta += f"• *Usuário:* @{username}\n\n"
            message_resposta += f"*=====================================*\n\n"
            message_resposta += f"• *Dados da Operação*\n"
            message_resposta += f"• *ID transação:* `{txid}`\n"
            message_resposta += f"• *Par Moedas:* `{par01}`\n"
            message_resposta += f"• *Cotação R$:* `{cotacao:.2f}`\n"
            message_resposta += f"• *Valor solicitado R$:* `{valor1:.2f}`\n"
            message_resposta += f"• *Taxa de serviço R$:* `{taxa_servico:.2f}`\n"
            message_resposta += f"• *Total a pagar R$:* `{a_pagar:.2f}`\n"
            message_resposta += f"• *Colateral Sats:* `{sats:.0f}` ⚡️\n"
            message_resposta += f"• *Colateral BTC:* `{btc_colateral:.8f}` ₿\n"
            message_resposta += f"• *Parcelas {parcelas}X de R$:* `{parcela_fiat:.2f}`\n"
            message_resposta += f"• *Parcelas {parcelas}X de ₿:* `{liquidacao_mansal:.8f}`\n"            
            message_resposta += f"• *Data*: `{data}`\n\n"
            message_resposta += f"⚠️ _Obs: Caso haja atraso de alguma parcela por parte do tomador do empréstimo, o custodiante/fornecedor do crédito estará autorizado a liquidar o proporcional de cada mês em BTC. Nesse caso ele poderá liquidar o equivalente a_ *{liquidacao_mansal:.8f}* ₿ _/ mês.\n\n• Cabe as partes decidirem a data e hora do vencimento, posterior a isso, a liquidação proporcional pode ser feita sem aviso prévio!_\n"
    
            sent_message02 = bot.send_message(mensagem.chat.id,
                            message_resposta,
                            parse_mode="Markdown",
                            reply_markup=botoes.menu_01())
            
            # Aguardar 60 segundos antes de excluir a mensagem
            time.sleep(300)
            # Excluir a mensagem
            bot.delete_message(mensagem.chat.id,
                            sent_message02.message_id)
            
    except ValueError:
            bot.send_message(mensagem.chat.id,
                         "\n🚫*Valor inválido!*\n\n✅ Forma correta ex: R$ 10.00\n- Exemplos: 10 | 10.00 | 10.50\n\n❌ Forma errada ex: R$ 10,00\n- Exemplos: 10,00 | 10,50 \n\n",
                         parse_mode="Markdown",
                         reply_markup=botoes.menu_01())




while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Ocorreu uma exceção: {str(e)}")
        continue

