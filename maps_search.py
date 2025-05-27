from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def buscar_dados_cards_maps(termo, limite=50):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.google.com/")
    time.sleep(2)

    # Aceita cookies se aparecer
    try:
        aceitar = driver.find_element(By.XPATH, "//button/div[contains(text(),'Aceitar')]")
        aceitar.click()
    except:
        pass

    # Pesquisa o termo
    barra = driver.find_element(By.NAME, "q")
    barra.send_keys(termo)
    barra.send_keys(Keys.ENTER)
    time.sleep(3)

    # Abre aba Maps
    try:
        aba_maps = driver.find_element(By.PARTIAL_LINK_TEXT, "Maps")
        aba_maps.click()
        time.sleep(5)
    except Exception as e:
        print("Erro ao clicar na aba Maps:", e)
        driver.quit()
        return []

    # Scroll para carregar mais cards
    try:
        scroll_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )
        for i in range(10):
            driver.execute_script("arguments[0].scrollTop += 1000", scroll_area)
            time.sleep(random.uniform(1.5, 2.5))
    except Exception as e:
        print("Erro ao rolar:", e)

    # Extrai os cards
    cards = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
    print(f"{len(cards)} cards encontrados")

    resultados = []
    for i, card in enumerate(cards[:limite]):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            card.click()
            time.sleep(4)

            nome = telefone = endereco = site = ""

            try:
                nome = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1').text

            except: pass

            try:
                endereco = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "address")]').text
            except: pass

            try:
                telefone = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone")]').text
            except: pass

            try:
                site = driver.find_element(By.XPATH, '//a[contains(@data-item-id, "authority")]').get_attribute('href')
            except: pass

            resultados.append({
                "nome": nome,
                "telefone": telefone,
                "endereco": endereco,
                "site": site
            })

        except Exception as e:
            print(f"Erro ao processar card {i+1}: {e}")
            continue

    driver.quit()
    return resultados
