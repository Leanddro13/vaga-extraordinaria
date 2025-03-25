from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apscheduler.schedulers.blocking import BlockingScheduler

from plyer import notification

from datetime import datetime

import time
import subprocess


# Lista de matérias a serem monitoradas
materias = [
    # Exemplo
    {
        "prof": "MARCOS FAGUNDES CAETANO (60h)",
        "horario": "35M12",
        "ensino": "GRADUAÇÃO",
        "departamento": "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA"
    },
    {
        "prof": "RICARDO PEZZUOL JACOBI (60h)",
        "horario": "24T23",
        "ensino": "GRADUAÇÃO",
        "departamento": "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA"
    }
    # },
    # {
    #     "prof": "",
    #     "horario": "",
    #     "ensino": "",
    #     "departamento": ""
    # },

    # Adicione mais matérias aqui seguindo o mesmo padrão
]

def pegaHoras():
    return datetime.now().strftime("[%H:%M]")

# Sistema de notificação

def notificarVaga(prof):
    notification.notify(
        title="TEM VAGA!!!",
        message=f"Tem vaga na disciplina com o {prof}!!!",
        app_name="Notificação do Sistema",
        timeout=10
    )
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

# Função para verificar a existência de vaga

def verificarVaga(): 
    service = Service()
    options = webdriver.ChromeOptions()
    
    # Para executar sem abrir a janela do navegador, descomente a linha abaixo:
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)

    url = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
    driver.get(url)

    # Fecha o aviso de cookies, se houver
    try:
        botao_cookie = driver.find_element(By.ID, "sigaa-cookie-consent")
        aceitar_btn = botao_cookie.find_element(By.TAG_NAME, "button")
        aceitar_btn.click()
        time.sleep(1)
    except:
        pass

    # Itera por cada matéria da lista
    for info_materia in materias:
        # Informações para busca
        prof = info_materia["prof"]
        horario = info_materia["horario"]
        ensino = info_materia["ensino"]
        departamento = info_materia["departamento"]
        pesquisa = f"{prof} {horario}"

        # Preenche os dropdowns com as informações de ensino e departamento
        dropdownbox = driver.find_elements(by=By.TAG_NAME, value="Option")

        for item in dropdownbox:
            if item.text == ensino or item.text == departamento:
                item.click()

        # Espera até que o botão de buscar esteja clickável
        try:
            botao_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="formTurma"]/table/tfoot/tr/td/input[1]'))
            )
            botao_buscar.click()
        except:
            hora_atual = pegaHoras()
            print(f"{hora_atual} Não foi possível clicar no botão Buscar para {horario} com {prof}.")
            driver.get(url)
            continue

        # Espera os resultados aparecerem
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="listagem"]'))
            )
        except:
            hora_atual = pegaHoras()
            print(f"{hora_atual} Tabela de resultados não carregou para {horario} com {prof}.")
            driver.get(url)
            continue

        elementos = driver.find_elements(By.TAG_NAME, 'tr')
        lista_materias = [value.text.replace('\n', ' ') for value in elementos]

        resultado_pesquisa = [item for item in lista_materias if pesquisa in item]
        resultado_pesquisa = ' '.join(resultado_pesquisa)

        # Se não encontrar uma matéria, parte para a próxima
        if not resultado_pesquisa.strip():
            hora_atual = pegaHoras()
            print(f"{hora_atual} A matéria de {horario} com {prof} não foi encontrada.")
            driver.get(url)
            continue

        partes = resultado_pesquisa.split()

        try:
            total_vaga = int(partes[-5]) # Pega o total de vagas
            vaga = int(partes[-4]) # Pega a quantidade de matriculados
        except (IndexError, ValueError):
            hora_atual = pegaHoras()
            print(f"{hora_atual} Erro ao analisar os dados de vagas da matéria de {horario} com {prof}.")
            driver.get(url)
            continue

        if(vaga < total_vaga):
            hora_atual = pegaHoras()
            print(f"{hora_atual} Tem vaga {horario} com {prof}")
            notificarVaga(prof)
        else:
            hora_atual = pegaHoras()
            print(f"{hora_atual} Não tem vaga {horario} com {prof}")
        
        # Recarrega a página para a próxima iteração
        driver.get(url)

    driver.quit()

# Configura o scheduler para verificar a cada 30 segundos
scheduler = BlockingScheduler()
scheduler.add_job(verificarVaga, 'interval', seconds=30)

try:
    hora_atual = pegaHoras()
    print(f"{hora_atual} Monitoramento iniciado...\nPressione Ctrl+C para encerrar.")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    hora_atual = pegaHoras()
    print(f"\n{hora_atual} Monitoramento encerrado pelo usuário.")
