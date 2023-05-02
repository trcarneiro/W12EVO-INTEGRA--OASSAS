#from Bot import Bot
#import utils
#from #Browser import Browser
#from Cookies import Cookies
#from IO import IO
#from Video import Video
#from selenium.common.exceptions import StaleElementReferenceException
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#import selenium.common
#import undetected_chromedriver.v2 as uc
#from fake_useragent import UserAgent, FakeUserAgentError


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
              
       url = f"https://evo.w12app.com.br/" 
       
       self.bot.get(url)
       
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
             
    def integra(self):              
    
        #self.bot = Browser().getBot()

        #self.bot.get(self.url)
        #self.bot.refresh()
        # Cookies loaded here.
        #time.sleep(5)
        #self.cookies = Cookies(self.bot)
        #self.loginevo('trcampos@gmail.com','C3po007*a')      
        #self.cobrançasemabertoevo()       
        #self.enviarcobrancaasa()   
        #self.bot.refresh()      
        #time.sleep(20)
        #self.busca_clientes_evo()
        self.cadastra_clientes_asaas()
        
    def enviarcobrancaasa(self):
        
        url = f"https://www.asaas.com/login/auth" 
       
        self.bot.get(url)
        
        #self.loginasa('kravmagabh@gmail.com','C3po007*a1')
        
    
        # Cookies loaded here.
        self.cookies = Cookies(self.bot)
        self.bot.refresh()
        
        time.sleep(20)
            
         