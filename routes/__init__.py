from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from flask import jsonify, request
from app_core import app
import os

@app.route("/")
def root():
    return jsonify({'mensage':'inicio API'}) 

@app.route("/scraping", methods=['POST'])
def scraping( ):
    req = request.get_json(silent=True)
    if not req:
        return jsonify({
            'mensage':'error'
        })

    try:    
        print(os.getcwd() + "/driver")      
        # ubicacion = "C:\\INSERTE_RUTA\\chromedriver.exe"
        
        ubicacion = os.getcwd() + "/driver/" + "chromedriver.exe"
        driver = webdriver.Chrome(executable_path=ubicacion)    
        _nro =  request.json['nro']
        _id =  request.json['id']
        _correo =  request.json['email']

        driver.get("https://www.pagostore.com/app")
        time.sleep(6)
        # driver.maximize_window()

        driver.find_element_by_class_name("_3TqH_GzIKGvl5zE4o8qVY_").click() 
        time.sleep(2)

        divFrame = driver.find_element_by_class_name("_398I0fs2EPlZotPmbmuUDk")
        divOpciones = divFrame.find_elements_by_class_name("CoL3r47acbYtO6eGLcT6G")
        i = 0
        for divOpcione in divOpciones:
            i = i + 1
            if i == 2:
                divOpcione.click()

        imputID = driver.find_element_by_class_name("oxVbmPqVSkCVx79GnnLc7")
        imputID.send_keys(_id)
        time.sleep(60)

        # presiono boton captcha
        driver.find_element_by_class_name("_3duKww4d68rWsj1YAVEbYt").click()
        time.sleep(4)

        # busco el diamante requerido
        divDiamante = driver.find_element_by_class_name("_3itcD-Pl_RmzhuigTd5VQN")
        aDiamantes = divDiamante.find_elements_by_class_name("qeVolXTT3AXVHe1jJL3lt")
        i = 0
        for aDiamante in aDiamantes:
            i = i + 1
            divDato = aDiamante.find_element_by_class_name("_3V9DM0qZ5XUDQCKZboGom")
            divDatoDiamante = divDato.find_element_by_class_name("_1v4QMCKGPgfdVXYRO07us")
            # print(divDatoDiamante.text)
            if i == int(_nro):
                aDiamante.click()

        #ingreso el correo
        time.sleep(2)
        imputCorreo = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[5]/div[2]/div[3]/div/div[2]/div[5]/div/div[2]/input")
        imputCorreo.send_keys(_correo)

        # preciono boton proceder pago
        driver.find_element_by_class_name("_3duKww4d68rWsj1YAVEbYt").click()
        time.sleep(6)

        # escojo el pago  
        apphome = driver.find_element_by_tag_name("app-home")

        divResultado = apphome.find_element_by_class_name("boxTransaction")
        pResultados = divResultado.find_elements_by_tag_name("p")
        selecc = 0
        for pResultado in pResultados:
            selecc = selecc + 1
            if selecc == 1:
                regresa = pResultado.text

            # print(pResultado.text)
        # print(regresa)
        
        driver.close()
        driver.quit()
        regresa = regresa.split(":")
        return jsonify({'respuesta':regresa[1].strip()})
    
    except Exception:
        driver.close()
        driver.quit()
        return jsonify({'respuesta':'error'})
    
