import requests 

# def consulta_cep(cep):
#     if len(cep) == 8:
#         link = f"https://viacep.com.br/ws/{cep}/json/"

#         requisicao = requests.get(link)

#         dic_requisicao = requisicao.json()

#         # uf = dic_requisicao['uf']
#         # cidade = dic_requisicao['localidade']
#         # bairro = dic_requisicao['bairro']
#         # print(dic_requisicao)
#         # print(cidade, bairro, uf, sep=" / ")
#         array_cep = {
#             'CEP': dic_requisicao['cep'],
#             'Logradouro': dic_requisicao['logradouro'],
#             'Complemento': dic_requisicao['complemento'],
#             'Bairro': dic_requisicao['bairro'],
#             'Localidade': dic_requisicao['localidade'],
#             'SIAFI': dic_requisicao['siafi']
#         }

#         return array_cep
#     else:
#         print("CEP Inválido")

# print(consulta_cep("66015090"))
# print(consulta_cep("66050240"))

#=-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-==-=-=

token = "6c1278e6defa13c8d6c4b38f0a0e068bb05f47f731455a88f9c2d2c1d178a878"

def consulta_cnpj(cnpj):
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # processar os dados do CNPJ
        # print(data['nome'], data['telefone'], data['complemento'], data['atividade_principal']['text'], sep=" / ")
        array_dados = {
            'CNPJ': cnpj,
            'Nome': data['nome'],
            'Telefone': data['telefone'],
            'Complemento': data['complemento'],
            'Atividade Principal': data['atividade_principal'][0]['text']
        }
        return array_dados
        # print(data)
    else:
        # lidar com erros de requisição
        return "CNPJ Inválido!"

# print(consulta_cnpj("12528708000107"))
# print(consulta_cnpj("10338320000100"))

def CriandoItems(array_de_itens):
    val = array_de_itens.split(" / ")
    itens = []
    for i in val:
        val2 = i.split(' , ')
        item = {'Produto': val2[0], 'Quantidade': val2[1], 'Valor Unitário': val2[2], 'Valor Total': float(val2[2]) * float(val2[1])}
        itens.append(item)
    return itens