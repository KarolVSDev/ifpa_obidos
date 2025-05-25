# Import for the Web Bot
from botcity.web import WebBot, Browser
from botcity.maestro import BotMaestroSDK
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import openpyxl

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def download_dados_covid():
    # URL do arquivo CSV
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    # Baixando os dados
    response = requests.get(url)
    with open("owid-covid-data.csv", "wb") as file:
        file.write(response.content)

    print("Dados COVID-19 baixados com sucesso!")

def processar_visualizar_dados():
    # Ler os dados
    data = pd.read_csv("owid-covid-data.csv")

    # Filtrar dados para o Brasil
    country_data = data[data['location'] == 'Brazil']

    # Converter a coluna de data para o tipo datetime
    country_data.loc[:, 'date'] = pd.to_datetime(country_data['date'])

    # Criar gráfico da evolução diária de novos casos
    plt.figure(figsize=(10, 5))
    plt.plot(country_data['date'], country_data['new_cases'], label='Novos Casos', color='blue')
    plt.title('Evolução Diária de Novos Casos de COVID-19 no Brasil')
    plt.xlabel('Data')
    plt.ylabel('Novos Casos')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig('covid_brazil_cases.png')
    plt.show()

    # Criar gráfico da evolução diária de novas mortes
    plt.figure(figsize=(10, 5))
    plt.plot(country_data['date'], country_data['new_deaths'], label='Novas Mortes', color='red')
    plt.title('Evolução Diária de Novas Mortes de COVID-19 no Brasil')
    plt.xlabel('Data')
    plt.ylabel('Novas Mortes')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig('covid_brazil_deaths.png')
    plt.show()

    # Criar um relatório em Excel
    report_data = country_data[['date', 'new_cases', 'new_deaths']]
    report_data.to_excel('covid_report_brazil.xlsx', index=False)

    print("Relatório gerado com sucesso!")

def main():
    # Initialize BotMaestro SDK
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.driver_path = r"C:\Users\blackoperation\Downloads\chromedriver-win64\chromedriver.exe"  # Ensure this path is correct
    bot.headless = False  # Set to True if you want to run headless

    # Download dos dados COVID-19
    download_dados_covid()

    # Processamento e visualização dos dados
    processar_visualizar_dados()

    # Esperar antes de fechar
    bot.wait(3000)

    # Limpar o navegador
    bot.stop_browser()

    # Descomente para finalizar a tarefa no BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
