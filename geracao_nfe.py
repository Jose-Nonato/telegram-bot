import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import jinja2
import pdfkit

def envio_teste(dados_teste, para, cco):
    variavel_dados = ""
    if type(dados_teste['Prestador']) == str and type(dados_teste['Cliente']) == dict:
        variavel_dados += """
            <h1>Informações Gerais</h1>
            <p>Prestador: {0}</p>
            <hr/>
            <p>Cliente: {1} | {2}</p>
            <p>Informações extras:</p>
            <p>{3} | {4}</p>
        """.format(dados_teste['Prestador'], dados_teste['Cliente']['CNPJ'], dados_teste['Cliente']['Nome'], dados_teste['Cliente']['Telefone'], dados_teste['Cliente']['Atividade Principal'])
    elif type(dados_teste['Prestador']) == dict and type(dados_teste['Cliente']) == str:
        variavel_dados += """
            <h1>Informações Gerais</h1>
            <p>Prestador: {0} | {1}</p>
            <p>Informações extras:</p>
            <p>{2} | {3}</p>
            <hr/>
            <p>Cliente: {4}</p>
        """.format(dados_teste['Prestador']['CNPJ'], dados_teste['Prestador']['Nome'], dados_teste['Prestador']['Telefone'], dados_teste['Prestador']['Atividade Principal'], dados_teste['Cliente'])
    elif type(dados_teste['Prestador']) == str and type(dados_teste['Cliente']) == str:
        variavel_dados += """
            <h1>Informações Gerais</h1>
            <p>Prestador: {0}</p>
            <hr/>
            <p>Cliente: {1}</p>
        """.format(dados_teste['Prestador'], dados_teste['Cliente'])
    elif type(dados_teste['Prestador']) == dict and type(dados_teste['Cliente']) == dict:
        variavel_dados += """
            <h1>Informações Gerais</h1>
            <p>Prestador: {0}</p>
            <p>Informações extras:</p>
            <p>{1} | {2}</p>
            <hr/>
            <p>Cliente: {3} | {4}</p>
            <p>Informações extras:</p>
            <p>{5} | {6}</p>
        """.format(dados_teste['Prestador']['CNPJ'], dados_teste['Prestador']['Nome'], dados_teste['Prestador']['Telefone'], dados_teste['Cliente']['CNPJ'], dados_teste['Cliente']['Nome'], dados_teste['Cliente']['Telefone'], dados_teste['Cliente']['Atividade Principal'])

    template = """
        <!DOCTYPE html>
        <html lang='pt-br'>
            <head>
                <meta charset="UTF-8">
                <title>Nota Fiscal Eletrônica</title>
            </head>
            <body>
                <h1>Nota Fiscal Eletrônica - Em Homologação</h1>
                {{ variavel_pdf }}
                <hr/>
                <table>
                    <tr>
                        <th>Produto</th>
                        <th>Quantidade</th>
                        <th>Valor Unitário</th>
                        <th>Valor Total
                    </tr>
                    {% for item in dados_teste['Itens'] %}
                    <tr>
                        <td>{{ item['Produto'] }}</td>
                        <td>{{ item['Quantidade'] }}</td>
                        <td>R$ {{ item['Valor Unitário'] }}</td>
                        <td>R$ {{ item['Valor Total'] }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </body>
        </html>
    """

    template_env = jinja2.Environment()
    template = template_env.from_string(template)
    html = template.render(dados_teste=dados_teste, variavel_pdf=variavel_dados)

    pdf_file = pdfkit.from_string(html, False)

    # Configurações do servidor de e-mail
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = '' # Adicionar email para envio
    smtp_password = '' # Adicionar senha para envio

    # Cria a mensagem de e-mail
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = para
    msg['Bcc'] = cco
    msg['Subject'] = 'Nota Fiscal'

    # Adiciona o corpo do e-mail (opcional)
    msg.attach(MIMEText('Segue em anexo a fatura gerada pelo ChatFatura!', 'plain'))

    # Adiciona o anexo (PDF em memória)
    attachment = MIMEApplication(pdf_file, _subtype="pdf")
    attachment.add_header('Content-Disposition', 'attachment', filename='fatura.pdf')
    msg.attach(attachment)

    # Envia o e-mail
    try:
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)
        smtp.quit()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print('Erro ao enviar o e-mail:', str(e))