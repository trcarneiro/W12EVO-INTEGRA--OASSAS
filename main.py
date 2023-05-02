# This class will be in charge of uploading videos onto tiktok.
from asyncio import exceptions
import os, time
from pydoc import cli
import re
import requests
from requests.auth import HTTPBasicAuth
import os, pickle
from os.path import exists
import json
import datetime
      
class integracao:
    def __init__(self):
        self.bot = None
        self.cookies = None
        #self.busca_clientes_evo()
        #self.gera_cobranca()
        self.busca_vendas_evo()
             
    def busca_clientes_evo(self,idMember):
        
        #print(idMember)
        if (idMember != ''):
            idMember = "/"+str(idMember)  
        
        api_url ='https://evo-integracao.w12app.com.br/api/v1/members'+idMember
        
        #print(api_url)
        
        try:
            response = requests.get(
                api_url, 
                auth=HTTPBasicAuth('evo', '9DE44B2E-7CD5-4346-BCE7-A8A7ECE2AA1A')
            )
           # response.raise_for_status()
           
            data = response.json()
            #print(data)
            #values = []
            #i=0

            return data    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
     
    def busca_vendas_evo(self):       
        
        api_url = 'https://evo-integracao.w12app.com.br/api/v1/sales?dateSaleStart=07/12/2022'
        #api_url = 'https://evo-integracao.w12app.com.br/api/v1/sales/1137836'
        
        try:
            response = requests.get(
                api_url, 
                auth=HTTPBasicAuth('evo', '9DE44B2E-7CD5-4346-BCE7-A8A7ECE2AA1A')
            )
            sales = response.json()
            #print(data[1])

            Email = ''
            mobilePhone = ''

            for sale in sales:
                cpf = 0
                celular = 0
                email = 0 

                #if sale['idSale'] != '':

                if sale['idSale'] == 1141672:   
                    idsale = sale['idSale']
                    dados = self.busca_clientes_evo(sale['idMember'])
                    print(dados['firstName'])
                    print(sale['idSale'])  
                    if(dados['document'] != None and dados['document'] != 'Null' and dados['document'] != ''):
                            cpf = 1
                            #print('Document',dados['document'])
                            for items in dados['contacts']:                           
                                if (items['contactType'] == 'Cellphone'):      
                                    mobilePhone = items['description']
                                    celular = 1
                                if (items['contactType'] == 'E-mail'):        
                                    Email = items['description']
                                    email = 1                    
                    if (cpf == 1 and celular == 1 and email == 1):           
                        values = {
                            "name": dados['firstName']+' '+dados['lastName'],
                            "cpfCnpj": dados['document'],
                            "mobilePhone": mobilePhone,
                            "email": Email,
                        }    
                        
                        #for saleItens in sale['saleItens']:
                             
                         
                         
                        #print(values)        
                        values=json.dumps(values)
                        dados_cliente_asaas = self.cadastra_clientes_asaas(values)
                        #print(dados_cliente_asaas)
                                               
                        #####IMPLEMENTAR PARA SOMAR PLANOS
                        #print(dados_cliente_asaas['data'][0]['id'])
                        valor = sale['saleItens'][0]['saleValue']
                        quantidade = sale['receivables'][0]['ammount']                                             
                        
                        try: 
                            vencimento = sale['receivables'][0]['dueDate'].rstrip("T")                           
                            #print(vencimento)
                        except: 
                            date = datetime.date.today() + datetime.timedelta(days=5)
                            vencimento = datetime.date.strftime(date,'%Y-%m-%d')
                            #print(vencimento)
                            
                        description =  'Quantidade: '+quantidade+' '+sale['saleItens'][0]['description'],idsale
                        #description = description.replace("[]","")
                        print(description)
                            
                        #self.gera_cobranca(dados_cliente_asaas['data'][0]['id'],vencimento,valor,description,idsale)                     
                    else:
                        print('FALTA DADOS')
            return response    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
                  
    def cadastra_clientes_asaas(self, values):

        headers = {
          'Content-Type': 'application/json',
          'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAxODY2NjE6OiRhYWNoXzUxZjg3ZDQ3LTc0NGYtNGViMi1hMjFmLWE3NmU1MjY1Mzg0ZQ=='
        }
        
        api_url = "https://www.asaas.com/api/v3/customers"
               
        try:
            
            dados = json.loads(values)
        
            client_existe = self.lista_cliente_asaas(dados['cpfCnpj'])

            if client_existe == 0:
                response = requests.post(api_url,data=values, headers=headers)
                #print('NÃO EXISTE ',response.text)
                return response.json()
            else:
                #print('JA EXISTE ',values)
                return client_existe
                       
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
              
    def lista_cliente_asaas(self,cpfCnpj):
        
        headers = {
          'Content-Type': 'application/json',
          'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAxODY2NjE6OiRhYWNoXzUxZjg3ZDQ3LTc0NGYtNGViMi1hMjFmLWE3NmU1MjY1Mzg0ZQ=='
        }
               
        try:
            api_url = "https://www.asaas.com/api/v3/customers?cpfCnpj="+cpfCnpj
            response = requests.get(api_url,headers=headers)
            
            #print(response.json())
            #print(response.json()['totalCount'])
            
            if (response.json()['totalCount'] > 0):
                return response.json()
            else:
                return 0
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
     
    def lista_cobrancas_asaas(self,cliente,id):
        
        headers = {
          'Content-Type': 'application/json',
          'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAxODY2NjE6OiRhYWNoXzUxZjg3ZDQ3LTc0NGYtNGViMi1hMjFmLWE3NmU1MjY1Mzg0ZQ=='
        }
               
        try:
            api_url = "https://www.asaas.com/api/v3/payments?customer="+cliente
            response = requests.get(api_url,headers=headers)
             
             
            print(response.json())            
            if response.json()['totalCount'] == 0:
               print('Teste')
               return 0 
            else:   
                existe = 0          
                for items in response.json()['data']:   
                    print(items['description'])    
                    cod = (items['description'].split(","))
                    cod = cod[1].rstrip(']')   
                    print('ID',id)
                    print('COD',cod)   
                    if str(id) == cod:
                        print('Cobrança EXISTE')
                        existe = 1
            if existe == 1:
                return 1 
            else:           
                return 0 
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
             
    def gera_cobranca(self,cliente,vencimento,valor,description,id):
        
        values = {
        "customer": cliente,
        "billingType": "UNDEFINED",
        "dueDate": vencimento,
        "value": valor,
        "description": description,
        }  
        
        values = json.dumps(values)
        #print(values)
    
        headers = {
          'Content-Type': 'application/json',
          'access_token': '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAxODY2NjE6OiRhYWNoXzUxZjg3ZDQ3LTc0NGYtNGViMi1hMjFmLWE3NmU1MjY1Mzg0ZQ=='
        }
        
        api_url = "https://www.asaas.com/api/v3/payments"
               
        try:
                      
            cobrancas = self.lista_cobrancas_asaas(cliente,id)
            print('cobrancas EXISTE? ',cobrancas)

            if cobrancas == 0:
                response = requests.post(api_url,data=values, headers=headers)
                print('COBRANÇA CRIADA')
            #else:
                #print('cobrancas JA EXISTE')

            #return response    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
    
w12 = integracao()    
#w12.busca_clientes_evo()    



    
    
    
    
    
    
    
    
    
    
    
    
    
    