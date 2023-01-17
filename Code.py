
import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.default_directory" : r"C:\Users\CESAR\Desktop\GitHub",
        "savefile.default_directory": r"C:\Users\CESAR\Desktop\GitHub"})
chromedriver =  r'C:\Program Files\ChromeDriver\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver, chrome_options=options)
driver.get('https://apps5.mineco.gob.pe/transferencias/gl/default.aspx')

for year in range(2005,2021):
	#La pagina web esta dividida en dos frames: (i) frame(0) es la parte superior, y (ii) frame(1) es la parte inferior.
	#Constantemente se tiene que realizar este cambio para poder seleccionar los distintos botones.
	#Año
	driver.switch_to.frame(0)
	seleccionar = Select(driver.find_element('id','drpAno'))
	seleccionar.select_by_value(str(year))

	#Recurso
	driver.switch_to.parent_frame()
	driver.switch_to.frame(1)
	driver.find_element('id','BTRecurso').click()

	#Canon minero
	driver.switch_to.parent_frame()
	driver.switch_to.frame(0)
	driver.find_element('xpath',"//*[contains(text(), 'CANON MINERO')]").click()
	
	#Departamentos
	driver.switch_to.parent_frame()
	driver.switch_to.frame(1)
	driver.find_element('name','BTDepartamento').click()

	driver.switch_to.parent_frame()
	driver.switch_to.frame(0)
	tabla_dpto = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]')
	departamentos = tabla_dpto.find_elements(By.TAG_NAME,'tr')
	for dpto in range(len(departamentos)-2):
		print("Departamento ",dpto)
		base_dato = []
		driver.find_element('id','tr' + str(dpto)).click()

		#Provincias
		driver.switch_to.parent_frame()
		driver.switch_to.frame(1)
		driver.find_element('name','BTProvincia').click()

		driver.switch_to.parent_frame()
		driver.switch_to.frame(0)
		tabla_prov = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]')
		provincias = tabla_prov.find_elements(By.TAG_NAME,'tr')
		for prov in range(len(provincias)-2):
			print("Provincia ",prov)
			driver.find_element('id','tr' + str(prov)).click()
			
			#Distritos
			driver.switch_to.parent_frame()
			driver.switch_to.frame(1)
			driver.find_element('name','BTMunicipalidad').click()

			#Descargar
			driver.switch_to.parent_frame()
			driver.switch_to.frame(0)
			dpto_valor = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[2]/tbody/tr[3]/td[2]').text
			prov_valor = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[2]/tbody/tr[4]/td[2]').text

			tabla_dist = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]')
			distritos = tabla_dist.find_elements(By.TAG_NAME,'tr')
			for dist in range(2,len(distritos)):
				print("Distrito",dist)
				dist_valor = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]/tbody/tr[' + str(dist) + ']/td[2]').text
				dist_m1 = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]/tbody/tr[' + str(dist) + ']/td[3]').text
				dist_m2 = driver.find_element('xpath','/html/body/form/div/table/tbody/tr/td[2]/table[3]/tbody/tr[' + str(dist) + ']/td[4]').text

				base_dato.append([year,dpto_valor,prov_valor,dist_valor,dist_m1,dist_m2])
				df = pd.DataFrame(base_dato,columns=['year','dpto_valor','prov_valor','dist_valor','dist_m1','dist_m2'])
				df.to_csv('A_' + str(year) + '_' + str(dpto) + '.csv',encoding='utf-8-sig',index=False)
				time.sleep(1)

			driver.find_element('id','ImgBack').click()
		
		time.sleep(2)
		driver.find_element('id','ImgBack').click()

	print("Terminó el año ",year)
	driver.find_element('id','ImgInicio').click()
	driver.switch_to.parent_frame()

driver.close()
