import telebot
from consultor import consulta_cnpj, CriandoItems
from geracao_nfe import envio_teste

chave_api = '6152742111:AAFzhe-BpRLXQhuRRNi5qO66lPLtI00Apt8'

bot = telebot.TeleBot(chave_api)

@bot.message_handler(commands=['gestao'])
def gestao(message):
    excel_url = 'https://1drv.ms/x/s!Avx6BD-7UZhEuSDUwEN4WwWm4wNs?e=45eWKe'
    texto_do = f'''
    Segue a planilha de gestão em excel:\n
    {excel_url}
    \nA senha para acesso/edição à planilha é "mmib2023"❗❗
    '''
    bot.reply_to(message, texto_do)

@bot.message_handler(commands=['gerarNFE'])
def NFGenerator(message):
    lista_perguntas = [
        'Informe o CPF ou CNPJ de quem fez o serviço!\nSem pontuação!',
        'Informe o CPF ou CNPJ do cliente!\nSem pontuação!',
        'Lista de produtos.\nSepare o preço do produto por "," e o produto por "/".\n Por exemplo:\nNome do Produto , Quantidade do Produto , Valor Unitário / Nome do Produto , Quantidade do Produto , Valor Unitário\nObs.: Os espaços entre os valores são necessários!',
        'Informe o email do cliente que irá receber a nota fiscal na caixa eletrônica de seu email.',
        'Informe o seu email para receber uma cópia.'
    ]
    respostas = []
    
    def ask_question(question):
        bot.reply_to(message, question)
        bot.register_next_step_handler(message, process_answer)

    def process_answer(answer):
        respostas.append(answer.text)
        if len(respostas) == len(lista_perguntas):
            # aqui pode processar as respostas
            # e gerar a nota fiscal
            bot.reply_to(message, 'Nota fiscal gerada!')
            arrayDados = {}
            if len(respostas[0]) == 11:
                print("É um CPF")
                arrayDados['Prestador'] = respostas[0]
            else:
                print("É um CNPJ")
                consulta_de_cnpj = consulta_cnpj(respostas[0])
                if consulta_de_cnpj != "CNPJ Inválido!":
                    arrayDados['Prestador'] = consulta_de_cnpj

            if len(respostas[1]) == 11:
                print("É um CPF")
                arrayDados["Cliente"] = respostas[1]
            else:
                consulta_de_cnpj = consulta_cnpj(respostas[1])
                if consulta_de_cnpj != "CNPJ Inválido!":
                    arrayDados['Cliente'] = consulta_de_cnpj
                print("É um CNPJ")
            
            arrayItens = CriandoItems(respostas[2])
            arrayDados['Itens'] = arrayItens

            print(respostas)
            print(arrayDados)

            envio_teste(arrayDados, respostas[3], respostas[4])
        else:
            ask_question(lista_perguntas[len(respostas)])
    
    bot.reply_to(message, 'Irei gerar a sua nota fiscal, preciso que me responda algumas perguntas!\nVamos lá!')
    ask_question(lista_perguntas[0])

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
    bot.reply_to(message, texto_do)

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
    bot.reply_to(message, texto)

bot.polling()