import telebot

chave_api = '6152742111:AAFzhe-BpRLXQhuRRNi5qO66lPLtI00Apt8'

bot = telebot.TeleBot(chave_api)

@bot.message_handler(commands=['afazeres'])
def todo(message):
    texto_do = '''
    Segue a lista de afazeres:\n
    Impostos que devem ser pagos por entidades sem fins lucrativos:\n
    - PIS / COFINS sobre a Folha de Pagamento (quando há folha)\n
    - INSS retido na Fonte\n
    - INSS retido na Folha\n
    - INSS Patronal\n
    - INSS sobre outras Entidades\n
    - IRFF (Imposto de Renda Retido pela Fonte)\n
    - Alvará (em Belém pode ser reconhecido por TLPL)\n
    ⚠️ Observações ⚠️\n
    👀 Os demais tributos são isentos, incluindo o IPTU! Caso a entidade pague IPTU, deve solicitar a isenção para a prefeitura de Belém!
    '''
    bot.send_message(message.chat.id, texto_do)

def checkMessage(message):
    return True

@bot.message_handler(func=checkMessage)
def answer(message):
    texto = '''
    🤖Olá, sou a representante do ChatFatura, Jéssica!🤖\n
    ✔️ Escolha uma das opções a seguir para continuar: ✔️\n
    📖 Verificar Lista de Afazeres Fiscais: /afazeres\n
    📃 Gerar Nota Fiscal: /gerarNFE\n
    📂 Gerar Planilha de Gestão: /gestao\n
    '''
    bot.send_message(message.chat.id, texto)


bot.polling()