'''
Esta aplicação calcula o beta de uma ação em relação ao Ibovespa, dada uma data de início da análise.

Desenvolvido por Victor Caldeira
Github: https://github.com/victor-caldeira

'''

import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def calcularBeta():
    start_date = input('Data de início da análise (Formato YYYY-MM-DD): ')
    print()

    # Importar dados
    ibov    = web.DataReader('^BVSP', data_source='yahoo', start=start_date)['Adj Close']

    while True:
        try:
            # Ativo de interesse:
            ativo = input('Digite o nome do ativo a ter o beta calculado: ')
            cotacao = web.DataReader(ativo, data_source='yahoo', start=start_date)['Adj Close']
            break
        except RemoteDataError: # ValueError:
            print("O ativo solicitado não foi encontrado na base de dados. Verifique o ticker e tente novamente (Formato B3: ABCDn.SA).")
            print()

    #cotacao = web.DataReader(ativo, data_source='yahoo', start=start_date)['Adj Close']

    print('...')

    # Retorno diário ativos
    ret_ibov  = ibov.pct_change()[1:]
    ret_ativo = cotacao.pct_change()[1:]

    # Calculo beta
    var_ibov = stats.tvar(ret_ibov)
    cov_ativo_ibov = np.cov(pd.concat([ret_ativo, ret_ibov], axis=1, join='inner'), rowvar=False)
    beta_ativo_ibov = cov_ativo_ibov[0,1] / var_ibov

    print('Data de início da análise:')
    print(ret_ativo.first_valid_index())
    print('Beta do ativo relativo ao Ibovespa: ')
    print(beta_ativo_ibov)
    print()

#Header
print('------------------------------------')
print('Esta aplicação calcula o beta de uma ação em relação ao Ibovespa, dada uma data de início da análise.')
print()
print('Desenvolvido por Victor Caldeira')
print('Github: https://github.com/victor-caldeira')
print()
print('------------------------------------')
print()

# Executa o código para calcular o Beta
calcularBeta()

ans = input('Deseja calcular o Beta de outro ativo? [Y/N] ')

while True:
    if ans == 'N' or  ans == 'n':
        input('Pressione Enter para encerrar.') # Mantém a cmd aberta até apertar enter
        break

    elif ans == 'Y' or  ans == 'y':
        calcularBeta()
        ans = input('Deseja calcular o Beta de outro ativo [Y/N]? ')
        print()

    else: 
        print()
        ans = input('Entrada não reconhecida. Digite Y se deseja calcular o beta de outro ativo ou N para encerrar: ') 
        print()
