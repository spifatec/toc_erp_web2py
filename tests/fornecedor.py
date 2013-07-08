import sys
import os
from os import path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

sys.path.append('../../../') # we need this to use web2py's modules

from gluon.sql import DAL, Field
from gluon.validators import *

compras_url_base = 'http://127.0.0.1:8000/toc_erp_web2py/compras'
driver = webdriver.Firefox()
action = '/inserir_fornecedor'
url_inserir_fornecedor = compras_url_base + action
submit_button = "//input[@value='Submit']"
flash_none = "//div[@class='flash' @style='display: none']"
flash_block = "//div[@class='flash']"

db_username_postgres = 'postgres'
db_password_postgres = '1234'
db_postgres_url = 'postgres://' + db_username_postgres + ':' + db_password_postgres + '@localhost/dev'

path_to_database = path.join(path.curdir, "../databases")
db_test = DAL(db_postgres_url, folder=path_to_database)
db_test.import_table_definitions(path_to_database)

def test_campos_obrigatorios_vazios():
	
	driver.get(url_inserir_fornecedor)

	nome_error = driver.find_elements_by_id("nome__error")
	cpf_cnpj_error = driver.find_elements_by_id("cpf_cnpj__error")
	rua_error = driver.find_elements_by_id("rua__error")
	bairro_error = driver.find_elements_by_id("bairro__error")
	cidade_error = driver.find_elements_by_id("cidade__error")
	estado_error = driver.find_elements_by_id("estado__error")

	mensagem_erro_padrao = 'enter a value'

	driver.find_element_by_xpath(submit_button).click()

	WebDriverWait(driver, 10)

	for element in nome_error:
		assert element.text == mensagem_erro_padrao

	for element in cpf_cnpj_error:
		assert element.text == mensagem_erro_padrao

	for element in rua_error:
		assert element.text == mensagem_erro_padrao	

	for element in bairro_error:
		assert element.text == mensagem_erro_padrao

	for element in cidade_error:
		assert element.text == mensagem_erro_padrao

	for element in estado_error:
		assert element.text == mensagem_erro_padrao

	#driver.quit()
	

def test_campos_obrigatorios_preenchidos():

	#driver.get(url_inserir_fornecedor)

	nome = driver.find_element_by_id("no_table_nome")
	cpf_cnpj = driver.find_element_by_id("no_table_cpf_cnpj")
	rua = driver.find_element_by_id("no_table_rua")
	bairro = driver.find_element_by_id("no_table_bairro")
	cidade = driver.find_element_by_id("no_table_cidade")
	estado = driver.find_element_by_id("no_table_estado")

	mensagem_sucesso = 'FOI'


	nome.send_keys("fornecedor qualquer")

	cpf_cnpj_num = "02441251524"

	cpf_cnpj.send_keys(cpf_cnpj_num)
	rua.send_keys("E")
	bairro.send_keys("MDA")
	cidade.send_keys("FSA")
	estado.send_keys("Bahia")

	driver.find_element_by_xpath(submit_button).click()

	assert (db_test(db_test.fornecedor.cpf_cnpj == cpf_cnpj_num).select() > 0) == True

	driver.quit()

"""def test_insercao_fornecedor_unico():
	pass

def test_exclusao_fornecedor_com_movimentacoes():
	pass

def test_exclusao_fornecedor_sem_movimentacoes():
	pass			"""
