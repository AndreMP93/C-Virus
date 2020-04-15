import requests
from datetime import datetime
import csv
import time
import os
chave = '--------------------------------'

def extrairDados(dicio):
    elementos = dicio['elements'][0]
    print(elementos['status'], end = " ")
    distancia = elementos['distance']['value']
    duração = elementos['duration_in_traffic']['value']#segundos
    return (distancia,duração)



def escreve_no_arquivo(nome_arquivo, informacao):
  with open(nome_arquivo, 'a', encoding="utf8") as arquivo_csv:
    escrever = csv.writer(arquivo_csv, delimiter=',', lineterminator="\n")
    escrever.writerow(informacao)

def main():
    arquivo = open('coordenadas.csv', encoding="utf8")
    linhas = csv.reader(arquivo)
    x = 0
    auxiliar = 0
    for linha in linhas:
      if(x%2 == 0):
        c_origem = str(linha[0])+","+str(linha[1])
        r_origem = str(linha[2])
      else:
        c_destino = str(linha[0])+","+str(linha[1])
        r_destino = str(linha[2])
        requisicao = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+c_origem+'&destinations='+ c_destino+'&mode=driving&departure_time=now&traffic_mod=&&key='+chave
        
        conexao = False
        while(conexao == False):
          try:
            dados_rota = requests.get(requisicao)
            conexao = True
          except:
            print("x", end=" ")
            time.sleep(30)
            conexao = False
        print(str(horas), end=" ")
        try:
            distancia_tempo= extrairDados(dados_rota.json()['rows'][0])
            print(".", end=" ")
            
        except:
            print("(---ERRO---)", end=" ")

        data_e_hora = datetime.now()
        auxiliar += 1
        pasta = data_e_hora.strftime('%d-%m')
        

        if not os.path.isfile(pasta+"/dados_rota"+str(auxiliar)+".csv"):
            escreve_no_arquivo(pasta+"/dados_rota"+str(auxiliar)+".csv",[r_origem,r_destino,data_e_hora.strftime('%d/%m/%Y')])
            escreve_no_arquivo(pasta+"/dados_rota"+str(auxiliar)+".csv",[str(distancia_tempo[0]), str(distancia_tempo[1]), data_e_hora.strftime('%H:%M')])
        else:
            escreve_no_arquivo(pasta+"/dados_rota"+str(auxiliar)+".csv",[str(distancia_tempo[0]), str(distancia_tempo[1]), data_e_hora.strftime('%H:%M')])
      x+=1



horas = 0
print('.', end='  ')
time.sleep(840)
print('.')
for i in range(96):
    inicio = time.time()
    data_e_hora = datetime.now()
    pasta = data_e_hora.strftime('%d-%m')
    USERS_PATH = './'+pasta+'/'
    if not os.path.exists(USERS_PATH):
        os.makedirs(USERS_PATH)
        
    
    main()
    fim = time.time()
    tempo_total = fim - inicio
    horas+=1
    if(tempo_total >1800):
        print("\n----- TEMPO > 1800 -----")
        time.sleep(1800)
    else:
        print('\n .->\n')
        time.sleep(1800 - tempo_total)

