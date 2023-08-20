import requests
import json
import xmltodict

class Main:
    def __init__(self) -> None:
        pass
    
    def obter_partner_id_meliuz(self, nome_loja: str):

        url = 'https://customer.meliuz.com.br/partners'

        resultado = requests.get(url=url)

        if resultado.status_code in (200, 304):
            dict_partners = json.loads(resultado.content)
            
            partners_data = dict_partners['data']

            for index in partners_data:
                partners_index = index['partners']
                for partner in partners_index:
                    
                    if partner['name'] == nome_loja:
                        id_partner = partner['id']
                        print(id_partner)
                        return id_partner

            raise Exception(f"loja {nome_loja} nao localizada")

        else:
            print(resultado.status_code)
            print(resultado.reason)

    def obter_cashback_partner_id_meliuz(self, partner_id: str):

        url = f'https://customer.meliuz.com.br/partners/{partner_id}'
        
        resultado = requests.get(url=url)

        if resultado.status_code == 200:
            dict_cashback = json.loads(resultado.content)
            
            cashback_valor = dict_cashback['active_cashback_offer']['value']

            return cashback_valor
        else:
            print(resultado.status_code)
            print(resultado.reason)

    def obter_cashback_inter(self, nome_loja: str):

        nome_loja = nome_loja.lower()
        nome_loja = nome_loja.replace(' ', '-')
        
        url = f'https://intershop.bancointer.com.br/lojas/{nome_loja}'

        resultado = requests.get(url=url)

        if resultado.status_code == 200:
            
            dict_pagina = resultado.content
            dict_pagina = xmltodict.parse(dict_pagina)

            titulo_pagina = dict_pagina['html']['head']['title']

            titulo_pagina = titulo_pagina.split(' ')
            valor_cashback = titulo_pagina[1].replace('%', '')
            print(valor_cashback)

        else:
            print(resultado.status_code)
            print(resultado.reason)


if __name__ == "__main__":
    teste = Main()

    nome_loja = "Dafiti"

    inter = teste.obter_cashback_inter(nome_loja)

    partner_id = teste.obter_partner_id_meliuz(nome_loja=nome_loja)

    resultado = teste.obter_cashback_partner_id_meliuz(partner_id=partner_id)

    print(f"Cashback: {resultado}%")