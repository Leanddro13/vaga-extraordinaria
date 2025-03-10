from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
from plyer import notification
import time
import subprocess

# Informações para busca
prof = "MARCOS FAGUNDES CAETANO (60h)"
horario = "35M34"
ensino = "GRADUAÇÃO"
departamento = "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA"

# Não alterar esse ultimo
pesquisa = prof + " " + horario


# Sistema de notificação

def notificarVaga():
    notification.notify(
        title="TEM VAGA!!!",
        message=f"tem vaga na disciplina com o {prof}!!!",
        app_name="Notificação do Sistema",
        timeout=10
    )
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

# Função para verificar a existência de vaga

def verificarVaga(): 
    service = Service()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
    driver.get(url)

    dropdownbox = driver.find_elements(by=By.TAG_NAME, value="Option")
    i = 0

    while i < len(dropdownbox):
        if(dropdownbox[i].text == ensino or dropdownbox[i].text == departamento):
            dropdownbox[i].click()
        i = i + 1
    driver.find_element(By.XPATH, '//*[@id="formTurma"]/table/tfoot/tr/td/input[1]').click()


    element = driver.find_elements(By.TAG_NAME, 'tr')
    materia = [value.text.replace('\n', ' ') for value in element]
    driver.quit()

    resultado_pesquisa = [item for item in materia if pesquisa in item]
    resultado_pesquisa = ' '.join(resultado_pesquisa)

    
    partes = resultado_pesquisa.split()

    total_vaga = int(partes[-5])
    vaga = int(partes[-4])

    if(vaga < total_vaga):
        print("Tem vaga")
        notificarVaga()
    else:
        print("Não tem vaga")

scheduler = BlockingScheduler()
scheduler.add_job(verificarVaga, 'interval', seconds=30)
print("Monitoramento iniciado....")
scheduler.start()