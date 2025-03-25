import tkinter as tk
from optparse import Values
from pydoc import locate
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import pandas as pd
import requests
from datetime import datetime
import numpy as np



requisisao = requests.get('https://economia.awesomeapi.com.br/json/all')
dicionario_moedas = requisisao.json()



lista_moedas = list(dicionario_moedas.keys())

def pegar_cotacao():
    moeda = combobox_selecionarmoeda.get()
    data_cotacao = calendario_moeda.get()
    ano = data_cotacao[-4:]
    mes = data_cotacao[3:5]
    dia = data_cotacao[:2]
    link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}"
    requisisao_moeda = requests.get(link)
    cotacao = requisisao_moeda.json()
    valor_moeda = cotacao[0]['bid']
    label_textocotacao['text'] = f"A Cotação da Moeda {moeda} no dia {data_cotacao} foi de: R${valor_moeda}"





def selecionar_arquivo():
    caminho_arquivo = askopenfilename(title="Selecione o Arquivo de Moeda")
    var_caminhoarquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_arquivoselecionado['text'] = f"Arquivo Selecionado: {caminho_arquivo}"






def atualizar_cotacoes():
    try:
        # ler o dataframe de moedas (tabela excel) (PARA ISSO PRECISA IMPORTAR "PANDAS")
        # Atenção a variável "df" significa dataframe
        df = pd.read_excel(var_caminhoarquivo.get())
        # pegar a data de início e a data do fim das cotações
        # moedas = df.iloc[linha, coluna]   assim não vai pegar o arquivo inteiro,
        # aqui é selecionada a LINHA e a COLUNA sendo " : " (Todas as Linhas)  e  " 0 " (Primeira coluna)
        moedas = df.iloc[:, 0]
        data_inicial = calendario_datainicial.get()
        data_final = calendario_datafinal.get()
        ano_inicial = data_inicial[-4:] # [-4:] = EDIÇÃO DE "STRING"
        mes_inicial = data_inicial[3:5] # [3:5] = EDIÇÃO DE "STRING"
        dia_inicial = data_inicial[:2]  # [:2] = EDIÇÃO DE "STRING"

        ano_final = data_final[-4:]   # [-4:] = EDIÇÃO DE STRING
        mes_final = data_final[3:5]  # [3:5] = EDIÇÃO DE "STRING"
        dia_final = data_final[:2]  # [:2] = EDIÇÃO DE "STRING"
        # função "for"
        # para cada moeda ( aqui começa a função "for"
        for moeda in moedas:
            link = (f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?" 
                    f"start_date={ano_inicial}{mes_inicial}{dia_inicial}" 
                    f"&end_date={ano_final}{mes_final}{dia_final}")
            requisisao_moeda = requests.get(link)
            cotacoes = requisisao_moeda.json()
            for cotacao in cotacoes:
                timestamp = int(cotacao['timestamp'])
                bid = float(cotacao['bid'])
                data_obj = datetime.fromtimestamp(timestamp)
                data = data_obj.strftime('%d/%m/%Y')  # para tratar a data no Formato Brasileiro dia/mês/ano.
                if data not in df:
                    df[data] = np.nan
                    # df.loc[linha,coluna]   para localizar (loc) uma Linha e uma Coluna
                df.loc[df.iloc[:, 0] == moeda, data] = bid      #  [df.iloc[:, 0]  SIGNIFICA ( " : "    Todas as linhas)
                                   # na [df.iloc[:, 0]    ( " 0 "  Primeira Coluna )
        df.to_excel("Teste.xlsx")
        label_atualizarcotacoes['text'] = "Arquivo Atualizado com Sucesso"

    except:
        label_atualizarcotacoes['text'] = "Selecione um arquivo Excel no Formato Correto"




        # No link do AwesomeAPI, vamos buscar a data da cotação ( 'timestamp' )
        # e para tratar a DATA, é necessário importar a Biblioteca 'datetime'.
        # e o VALOR da cotação ( 'bid' )
        # a data vem no formato de um número ex: ( 150813654000 ) precisa
        # ser "tratada" ( transformada em um valor "int" (valor inteiro)
        # e o VALOR  "tratado em forma de 'float' . "




        # pegar todas s cotações daquela moeda (selecionada)
        # criar uma coluna em um novo datafreme com todas as cotações daquela moeda
    # fora da função "for"
    # criar um arquivo com todas as cotações





janela = tk.Tk()

janela.title('Ferramenta de Cotação de Moedas')

label_cotacaomoeda = tk.Label(text="Cotação de 1 Moeda Específica", borderwidth=2, relief='solid')
label_cotacaomoeda.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', columnspan=3)

label_selecionarmoeda = tk.Label(text="Selecionar Moeda", anchor='e')
label_selecionarmoeda.grid(row=1, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)

combobox_selecionarmoeda = ttk.Combobox(values=lista_moedas)
combobox_selecionarmoeda.grid(row=1, column=2, padx=10, pady=10, sticky='nswe')

label_selecionardia = tk.Label(text="Selecione o dia que deseja pegar a cotação",anchor='e')
label_selecionardia.grid(row=2, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)

calendario_moeda = DateEntry(year=2025, locale='pt_br')
calendario_moeda.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

label_textocotacao = tk.Label(text="")
label_textocotacao.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

botao_pegarcotacao = tk.Button(text="Pegar Cotação", command=pegar_cotacao)
botao_pegarcotacao.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')


#cotação de várias moedas


label_cotacaovariasmoedas = tk.Label(text="Cotação de Múltiplas Moedas", borderwidth=2, relief='solid')
label_cotacaovariasmoedas.grid(row=4, column=0, padx=10, pady=10, sticky='nswe', columnspan=3)

label_selecionararquivo = tk.Label(text='Selecione um Arquivo em Excel com as Moedas na Coluna A')
label_selecionararquivo.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

var_caminhoarquivo = tk.StringVar()

botao_selecionararquivo = tk.Button(text="Clique para Selecionar", command=selecionar_arquivo)
botao_selecionararquivo.grid(row=5, column=2, padx=10, pady=10, sticky='nsew')

label_arquivoselecionado = tk.Label(text='Nenhum Arquivo Selecionado', anchor='e')
label_arquivoselecionado.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

label_datainicial = tk.Label(text="Data Inicial", anchor='e')
label_datafinal = tk.Label(text="Data Final", anchor='e')
label_datainicial.grid(row=7, column=0, padx=10, pady=10, sticky='nsew')
label_datafinal.grid(row=8, column=0, padx=10, pady=10, sticky='nsew')

calendario_datainicial = DateEntry(year=2025, locale='pt_br')
calendario_datafinal = DateEntry(year=2025, locale='pt_br')
calendario_datainicial.grid(row=7, column=1, padx=10, pady=10, sticky='nsew')
calendario_datafinal.grid(row=8, column=1, padx=10, pady=10, sticky='nsew')

botao_atualizarcotacoes = tk.Button(text='Atualizar Cotações', command=atualizar_cotacoes)
botao_atualizarcotacoes.grid(row=9, column=0, padx=10, pady=10, sticky='nsew')

label_atualizarcotacoes = tk.Label(text="")
label_atualizarcotacoes.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')

botao_fechar = tk.Button(text='Fechar', command=janela.quit)
botao_fechar.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')



janela.mainloop()
