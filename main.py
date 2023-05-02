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
from datetime import timedelta
from autevo import *
      
class integracao:
    def __init__(self):
        self.bot = None
        self.cookies = None
        #self.busca_clientes_evo()
        #self.gera_cobranca()     
        TOKEN = ""
        headers = {
          'Content-Type': 'application/json',
          'access_token': {TOKEN}
        }      
        APIKEY = ""

        self.busca_vendas_evo()
        #self.marcar_recebido_evo('')
        #self.notificacoes('cus_000035576884')
                          
    def busca_clientes_evo(self,idMember):
        
        #print(idMember)
        if (idMember != ''):
            idMember = "/"+str(idMember)  
        
        api_url ='https://evo-integracao.w12app.com.br/api/v1/members'+idMember
        
        #print(api_url)
        
        try:
            response = requests.get(
                api_url, 
                auth=HTTPBasicAuth('evo', self.APIKEY)
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
     
    def busca_info_venda(self,idsale): 
                
        try:           
            api_url = 'https://evo-integracao.w12app.com.br/api/v1/sales/'+str(idsale)
            response = requests.get(api_url,auth=HTTPBasicAuth('evo', self.APIKEY))
            return response.json()   
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)    
         
    def busca_vendas_evo(self):    
                
        try:    
            
            date = datetime.date.today()# - + timedelta(days=-3)
            #print(date)
            dateSaleStart = date - timedelta(days=+15)
            #print(dateSaleStart)
            dateSaleEnd = date - timedelta(days=-1)
            #print(dateSaleEnd)
            dateSaleStart = datetime.date.strftime(dateSaleStart,'%Y-%m-%d')  
            dateSaleEnd =  datetime.date.strftime(dateSaleEnd,'%Y-%m-%d')      
                   
            api_url = 'https://evo-integracao.w12app.com.br/api/v1/sales?dateSaleStart='+dateSaleStart+'&dateSaleEnd='+dateSaleEnd
            print(api_url)
            response = requests.get(api_url,auth=HTTPBasicAuth('evo', self.APIKEY))
            sales = response.json()

     
            for sale in sales:
                cpf = 0
                celular = 0
                email = 0 
                mobilePhone = ''
                Email = ''
                #print(sale)  
                print(sale['idSale'])  
                print(sale['idMember'])
                print('____________________')
                #if sale['idSale'] == 1539470:  
                #if sale['idMember'] == 303925:      
                if  (sale['idSale'] != '' and sale['idMember'] != None and sale['idMember'] != ''):
                    #print('SALE ', sale)                 
                    idsale = sale['idSale']
                    salesinfos = self.busca_info_venda(idsale)
                    #print('salesinfos ', salesinfos)    
                    status = salesinfos['receivables'][0]['status']['name']
                    paymentType = salesinfos['receivables'][0]['paymentType']['name']
                    #print(paymentType)
                    #print('salesinfos ', salesinfos)     
                    print('STATUS ',status)
                    if paymentType != 'Credit card':
                        if status == 'Em aberto' or status == 'Vencido' or status == 'open' or status == 'Expired':
                            #print(salesinfos) 
                            #print(sale['idMember'])
                            dados = self.busca_clientes_evo(sale['idMember'])
                            #print(dados)
                            print('NOME ', dados['firstName'],'',dados['lastName'])
                            print('DOCUMENTOS ' , dados['document'])
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
                                #print(dados_cliente_asaas)
                                valor = salesinfos['receivables'][0]['ammount']    
                            #print('VALOR ',valor)

                            ######IMPLEMENTAR CURSOR PARA saleItens quantidade

                            #quantidade = 0
                            #quantidade = salesinfos['receivables'][0]['ammount']      
                            #print('QUANTIDADE ',quantidade)                                     

                            #try: 
                                vencimento = salesinfos['receivables'][0]['dueDate'].split("T")
                                vencimento = vencimento[0]  
                                date = datetime.date.today() + datetime.timedelta(days=5)  
                                #venci = datetime.date.strftime(date,'%Y-%m-%d')  
                                #print(vencimento)                         
                                vencimento = (datetime.datetime.strptime(vencimento,'%Y-%m-%d') + datetime.timedelta(days=3)).date() #.date() 

                                #print(vencimento)
                                #print(venci + datetime.timedelta(days=5))
                                #if (vencimento) >= venci:
                                #print(vencimento)
                                #vencimento = venci
                                #print(vencimento).
                                servicesdescription = ''

                                for saleIten in sale['saleItens']:
                                    servicesdescription = servicesdescription + (saleIten['description']) +' R$ ' + str(saleIten['saleValue']) +  ' '

                                #description =  sale['saleItens'][0]['description']+' Quantidade: '+str(quantidade)+' Valor: '+str(valor),idsale
                                description =  servicesdescription+' - Valor Total: R$ '+str(valor),idsale
                                #description = description.replace("[]","")
                                #print(servicesdescription)
                                #print(description)
                                #print(dados_cliente_asaas['data'][0]['id'])
                                vencimento = datetime.date.strftime(vencimento,'%Y-%m-%d') 
                                print(vencimento)
                                #print(venci)
                                print(valor)
                                #print('____________________')
                                #
                                #print(valor)
                                #print(idsale)

                                self.gera_cobranca(dados_cliente_asaas['data'][0]['id'],vencimento,valor,description,idsale)                     
                                #else:
                                #    print('VENCIDO')
            return response    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
     
    def busca_notificacoes(self, id):
        
        api_url = 'https://www.asaas.com/api/v3/customers/'+id+'/notifications'
        
        #api_url = 'https://www.asaas.com/api/v3/notifications/'+id
        
        #print(api_url)
               
        try:
            response = requests.get(api_url, headers= self.headers
        )
            print(response.text)
            return response.json()
                       
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)    
           
    def notificacoes(self, id):

        
              
        notificacoes = self.busca_notificacoes(id)
        
        #print(notificacoes)
        
        for notifica in notificacoes['data']:
            #print(notifica['id'])
            #print(notifica['event'])
            if notifica['event'] == 'PAYMENT_CREATED':
                id_notificacao = notifica['id']
                   
        values = """
              {
                "object":"notification",  
                "id": """+str(id_notificacao)+""",
                "enabled": true,
                "emailEnabledForProvider": true,
                "smsEnabledForProvider": true,
                "emailEnabledForCustomer": true,
                "smsEnabledForCustomer": true,
                "whatsappEnabledForCustomer": true,
                "phoneCallEnabledForCustomer": false,
                "event": "PAYMENT_CREATED",
              }
            """
            
        #print(values)    
        
        api_url = 'https://www.asaas.com/api/v3/notifications/'+id
        
        #print(api_url)
               
        try:
            response = requests.post(api_url,data=values, headers= self.headers
        )
            print(response.text)
            return response.json()
                       
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)    
                              
    def cadastra_clientes_asaas(self, values):

        api_url = "https://www.asaas.com/api/v3/customers"
               
        try:
            
            dados = json.loads(values)
        
            client_existe = self.lista_cliente_asaas(dados['cpfCnpj'])

            if client_existe == 0:
                response = requests.post(api_url,data=values, headers= self.headers
        )
                #print('NÃO EXISTE ',response.text)
                self.notificacoes(response.json()['id'])
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
                    
        try:
            api_url = "https://www.asaas.com/api/v3/customers?cpfCnpj="+cpfCnpj
            response = requests.get(api_url,headers= self.headers
        )
            
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
                    
        try:
            api_url = "https://www.asaas.com/api/v3/payments?customer="+cliente
            response = requests.get(api_url,headers= self.headers
        )
                          
            #print(response.json())            
            if response.json()['totalCount'] == 0:
               #print('Teste')
               return 0 
            else:   
                existe = 0          
                for items in response.json()['data']:
                    try:   
                        #print(items['description'])   
                        cod = (items['description'].split(","))
                        cod = cod[1] 
                        #print('COD ',cod)   
                        if int(id) == int(cod):
                            #print('SALES ID ',id)
                            #print('Cobrança EXISTE')
                            return items
                    except Exception as e:
                        print(e)
                        pass    
            #if existe == 1:
                
            #else:           
                return 0 
            
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
             
    def gera_cobranca(self,cliente,vencimento,valor,description,idsale):
        
        description = str(description).replace("'","").replace(")","").replace("(","")
        #print(description)
        
        values = {
        "customer": cliente,
        "billingType": "UNDEFINED",
        "dueDate": vencimento,
        "value": valor,
        "description":description,
        }  
        
        print(values)
        
        values = json.dumps(values)
        
        api_url = "https://www.asaas.com/api/v3/payments"
               
        try:
                      
            cobrancas = self.lista_cobrancas_asaas(cliente,idsale)
            print('cobrancas EXISTE? ',cobrancas)
            
            if cobrancas == 0:
                response = requests.post(api_url,data=values, headers= self.headers
        )
                #print(response.text)
                print('COBRANÇA CRIADA!!!!!!!!')
            else:
                print('COBRANÇA JA EXISTE')
                print(cobrancas)
                print(cobrancas['status'])
                if(cobrancas['status'] == 'RECEIVED' or cobrancas['status'] == 'RECEIVED_IN_CASH' or cobrancas['status'] == 'CONFIRMED'):
                    #print(cobrancas['status'])
                    print(cobrancas)
                    idsalesasaas = str(cobrancas['id'])
                    comprovante = str(cobrancas['transactionReceiptUrl'])
                    salesinfo = self.busca_info_venda(idsale)
                    #print(salesinfo)
                    idMember = str(salesinfo['idMember'])
                    #print(idMember)
                    estado = salesinfo['receivables'][0]['status']['name']           
                    print('ESTADO ', estado)        
                    if estado == 'Vencido' or estado == 'Em aberto' or estado == 'open' or estado == 'Expired':
                        print('NECESSARIO DAR BAIXA NO EVO ', salesinfo['receivables'][0]['status']['name'])                          
                        autevo.baixa_venda(idMember,str(idsale),idsalesasaas+','+comprovante)

            #return response    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
    
    def marcar_recebido_evo(self,idsReceivables):
        
        api_url = 'https://evo-integracao.w12app.com.br/api/v1/receivables/mark-received'
        
        dados = {"idsReceivables": [1704617],
                  "idBankAccount": 0,
                }
        
        try:
            response = requests.put(
                api_url, 
                auth=HTTPBasicAuth('evo', self.APIKEY), 
                data =dados
            )
            #print(response.text)
            #print(response)
            print(response.content)
            #return data    
        #except Exception:
        #    raise Exception    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
            
    def marcar_recebido_evo_selenium(self,idsReceivables):
        
        api_url = 'https://evo-integracao.w12app.com.br/api/v1/receivables/mark-received'
        
        dados = {"idsReceivables": [1704617],
                  "idBankAccount": 0,
                }
        
        try:
            response = requests.put(
                api_url, 
                auth=HTTPBasicAuth('evo', self.APIKEY), 
                data =dados
            )
            #print(response.text)
            #print(response)
            print(response.content)
            #return data    
        #except Exception:
        #    raise Exception    
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)        
  
            
#autevo = automacao_evo() 
            
w12 = integracao()    
#w12.busca_clientes_evo()    



    
    
    
    
    
    
    
    
    
    
    
    
    
    