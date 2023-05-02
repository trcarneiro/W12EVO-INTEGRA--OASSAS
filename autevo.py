from weakref import ref
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from cookie import Browser



class automacao_evo():    
    def __init__(self):
        print('COBRANÇA')
        #self.bot = Browser().getBot()
        #self.loginevo('trcampos@gmail.com','C3po007*a')  
        #self.baixa_venda('303925','1142732','TST')  
        
    def wait_for_elem_by_xpath(self, xp, timer=100, clickable=False):
        # clickable flag adjusts if should the element be clickable
        # labels and such elements won't be clickable hence the default False
        if clickable:
            # wait for element to be clickable
            method = EC.element_to_be_clickable
        else:
            # wait for element presence
            method = EC.presence_of_element_located

        try:
            # wait until the element is found

            element = WebDriverWait(self.bot, timer).until(method((By.XPATH, xp)))

            return element
        except TimeoutException as ex:
            #print(xp)
            #print(method)
            #print("Não Encontrado")
            return 'false'
            # if element is not found  in time, you can retry or return False 
            # or you can set a "negative" flag if you expect an element not to be found
            # or just...
            raise ex    

    def baixa_venda(self,idmember,idsale,idsaleasaas):
        
        self.bot = Browser().getBot()
        
        user = ""
        password = ""
              
        self.loginevo(user,password)  
        
        url = f"https://evo.w12app.com.br/#/app/evo/795/clientes/"+idmember+"//financeiro/saldodevedor" 
        print(url)
       
        self.bot.get(url)
        self.bot.refresh()
        
        time.sleep(5)    
        
        xpath = "//td[normalize-space()='"+idsale+"']/..//md-icon[@aria-label='Receber'][normalize-space()='attach_money']"
        print(xpath)
        input_field = self.wait_for_elem_by_xpath(xpath, True)
        if (input_field != 'false'):
            input_field.click() 
            
            
        time.sleep(5)   
        xpath = "//button[normalize-space()='Abrir']"       
        input_field = self.wait_for_elem_by_xpath(xpath, True)
        if (input_field != 'false'):
            print(xpath)
            input_field.click() 
            
        time.sleep(5)    
        
        xpath = "//md-tab-item[normalize-space()='Transferência']"
        print(xpath)
        WebDriverWait(self.bot, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        time.sleep(3)  
        
        xpath = "//input[@id='observacao']"
        print(xpath)
        WebDriverWait(self.bot, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(idsaleasaas)
        
        xpath = "//div[@class='container-acao-tab-venda no-padding-right layout-align-start-center layout-row']//div//button[@id='adicionar']"
        print(xpath)
        WebDriverWait(self.bot, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        xpath = "//button[@id='finalizar']"
        print(xpath)
        WebDriverWait(self.bot, 100).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
               
        time.sleep(10)

    def cobrançasemabertoevo(self):
    
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[id='1'] span[class='nav-text ng-binding']"))).click() 
        #WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(21) > div:nth-child(2) > div:nth-child(1) > mat-dialog-container:nth-child(2) > modal-clientes-inadimplentes:nth-child(1) > div:nth-child(2) > evo-grid:nth-child(1) > div:nth-child(2) > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > p:nth-child(1) > span:nth-child(2)'))).click()
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#detalhesModalClientesInadimplentes"))).click()
        
        xpath = "//span[normalize-space()='Vinícius Almeida Habib']"
        #selector = "body > div:nth-child(21) > div:nth-child(2) > div:nth-child(1) > mat-dialog-container:nth-child(2) > modal-clientes-inadimplentes:nth-child(1) > div:nth-child(2) > evo-grid:nth-child(1) > div:nth-child(2) > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > p:nth-child(1) > span:nth-child(2)"
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        xpath = "//span[normalize-space()='Cadastro']"
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        time.sleep(5)
        
        xpath = "//h3[@class='text-white no-margin truncate ng-binding']"
        nome = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        
        #xpath = "//input[@id='input_2933']"
        #cpf = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        
        xpath = "//span[@class='_md-nav-button-text ng-scope'][normalize-space()='Financeiro']"
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        xpath = "//md-tab-item[normalize-space()='Saldo devedor']"
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        xpath = "//*[@id='tableSaldoDevedor']/table/tbody/tr/td[4]/p"
        valor = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        
        xpath = "//*[@id='tableSaldoDevedor']/table/tbody/tr/td[5]"
        vencimento = WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).text     
        
        print("nome", nome)
        
        #print("cpf", cpf)  
        
        print("vencimento", vencimento)
        
        print("valor", valor)
        
        time.sleep(10)
         
    def loginevo(self,user,password):
              
       url = f"https://evo.w12app.com.br/#/acesso/evo/autenticacao" 
       

       self.bot.get(url)
       self.bot.refresh()
       
       time.sleep(5)
        
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#usuario'))).send_keys(user)  
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#senha'))).send_keys(password)   
       time.sleep(5) 
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#entrar'))).click() 
    
       time.sleep(10)
              
    def loginasa(self,user,password):
        
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Informe seu e-mail']"))).send_keys(user)  
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Informe sua senha']"))).send_keys(password)   
       time.sleep(5) 
       WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='button']"))).click() 
    
       selection = input("Codigo SMS enviado, digite")
       #selected = int(selection)
    
       time.sleep(10)       
               
    def enviarcobrancaasa(self):
        
        url = f"https://www.asaas.com/login/auth" 
    
        self.bot.get(url)
        
        #self.loginasa('kravmagabh@gmail.com','C3po007*a1')
        
    
        # Cookies loaded here.
        #self.cookies = Cookies(self.bot)
        self.bot.refresh()
        
        time.sleep(20)
            
autevo = automacao_evo()
