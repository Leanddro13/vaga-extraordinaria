from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apscheduler.schedulers.blocking import BlockingScheduler

from plyer import notification

from datetime import datetime

from dotenv import load_dotenv

import os
import time
import subprocess

# Carrega variáveis do arquivo .env
load_dotenv()

login = os.getenv("LOGIN")
senha = os.getenv("SENHA")
data_nascimento = os.getenv("DATA_NASCIMENTO")

# Lista de matérias a serem monitoradas
materias = [
    # Exemplo
    {
        "prof": "MARCOS FAGUNDES CAETANO (60h)",
        "codigo": "CIC0124",
        "horario": "35M12",
        "ensino": "GRADUAÇÃO",
        "departamento": "DEPTO CIÊNCIAS DA COMPUTAÇÃO - BRASÍLIA"
    },
    {
        "prof": "RICARDO PEZZUOL JACOBI (60h)",
        "codigo": "CIC0130",
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

# Sistema de matrícula

# TODO: Fazer Chrome entrar no portal do aluno e matricular
# TODO: Fazer Sistema parar de tentar matricular na matéria já matriculada 

# def realizarMatricula(codigo_componente, horario, nome_prof):
#     try:
#         matricula_driver = webdriver.Chrome()
#         link = 'https://sigaa.unb.br/sigaa/portais/discente/discente.jsf'
#         matricula_driver.get(link)

#         # Login
#         matricula_driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(login)
#         matricula_driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha)
#         matricula_driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()

#         # Acessar aba de matrícula extraordinária
#         time.sleep(2)
#         matricula_driver.find_element(By.XPATH, '//*[@id="menu_form_menu_discente_j_id_jsp_340461267_98_menu"]/table/tbody/tr/td[1]/span[2]').click()
#         matricula_driver.find_element(By.XPATH, '//*[@id="cmSubMenuID1"]/table/tbody/tr[13]/td[2]').click()
#         matricula_driver.find_element(By.XPATH, '//*[@id="cmSubMenuID3"]/table/tbody/tr[3]/td[2]').click()

#         # Buscar disciplina
#         matricula_driver.find_element(By.XPATH, '//*[@id="form:txtCodigo"]').send_keys(codigo_componente)
#         matricula_driver.find_element(By.XPATH, '//*[@id="form:txtHorario"]').send_keys(horario)
#         matricula_driver.find_element(By.XPATH, '//*[@id="form:txtNomeDocente"]').send_keys(nome_prof)
#         matricula_driver.find_element(By.NAME, 'form:buscar').send_keys("\n")

#         # Selecionar turma e confirmar matrícula
#         time.sleep(2)
#         matricula_driver.find_element(By.XPATH, '//*[@id="form:selecionarTurma"]/img').click()
#         matricula_driver.find_element(By.XPATH, '//*[@id="j_id_jsp_334536566_1:Data"]').send_keys(data_nascimento)
#         matricula_driver.find_element(By.XPATH, '//*[@id="j_id_jsp_334536566_1:senha"]').send_keys(senha)
#         matricula_driver.find_element(By.XPATH, '//*[@id="j_id_jsp_334536566_1:btnConfirmar"]').click()

#         # Aceita alerta
#         WebDriverWait(matricula_driver, 5).until(EC.alert_is_present())
#         matricula_driver.switch_to.alert.accept()

#         print(f"{pegaHoras()} Matrícula realizada com sucesso para {codigo_componente} - {nome_prof} - {horario}")
#         matricula_driver.quit()

#     except Exception as e:
#         print(f"{pegaHoras()} Erro ao tentar se matricular: {e}")


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
    # options.add_argument("--headless")

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
            print(f"{pegaHoras()} Não foi possível clicar no botão Buscar para {horario} com {prof}.")
            driver.get(url)
            continue

        # Espera os resultados aparecerem
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//table[@class="listagem"]'))
            )
        except:
            print(f"{pegaHoras()} Tabela de resultados não carregou para {horario} com {prof}.")
            driver.get(url)
            continue

        elementos = driver.find_elements(By.TAG_NAME, 'tr')
        lista_materias = [value.text.replace('\n', ' ') for value in elementos]

        resultado_pesquisa = [item for item in lista_materias if pesquisa in item]
        resultado_pesquisa = ' '.join(resultado_pesquisa)

        # Se não encontrar uma matéria, parte para a próxima
        if not resultado_pesquisa.strip():
            print(f"{pegaHoras()} A matéria de {horario} com {prof} não foi encontrada.")
            driver.get(url)
            continue

        partes = resultado_pesquisa.split()

        try:
            total_vaga = int(partes[-5]) # Pega o total de vagas
            vaga = int(partes[-4]) # Pega a quantidade de matriculados
        except (IndexError, ValueError):
            print(f"{pegaHoras()} Erro ao analisar os dados de vagas da matéria de {horario} com {prof}.")
            driver.get(url)
            continue

        if(vaga < total_vaga):
            print(f"{pegaHoras()} Tem vaga {horario} com {prof}")
            notificarVaga(prof)
            # realizarMatricula(info_materia["codigo"], horario, prof)
        else:
            print(f"{pegaHoras()} Não tem vaga {horario} com {prof}")
        
        # Recarrega a página para a próxima iteração
        driver.get(url)

    driver.quit()

# Configura o scheduler para verificar a cada 30 segundos
scheduler = BlockingScheduler()
scheduler.add_job(verificarVaga, 'interval', seconds=30)

try:
    print(f"{pegaHoras()} Monitoramento iniciado...\nPressione Ctrl+C para encerrar.")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print(f"\n{pegaHoras()} Monitoramento encerrado pelo usuário.")
