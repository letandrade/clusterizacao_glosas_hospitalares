
#bibliotecas

#banco de dados
import cx_Oracle

#manipulação
import pandas as pd
import numpy as np
seed = 100

#warnings
import warnings
warnings.simplefilter("ignore")

#cluster
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

#importar modulo construido
from modulo_clusterizacao_hospital_recente import clusterizacao

# Declarando variáveis usadas para regras 
convenios = ['CONVENIO A', 'CONVENIO B']

hospitais = clusterizacao.carrega_dataset_hospitais()
hospitais = hospitais['HOSPITAL'].tolist()

tipo_glosa = ['TIPO_GLOSA  A','TIPO_GLOSA B']

# Executar a consulta para buscar as combinações válidas
combinacoes_validas = clusterizacao.carrega_dataset_combinacoes()

# Criando combinações
combinacoes_validas_set = set(zip(combinacoes_validas['HOSPITAL'], combinacoes_validas['CONVENIO'], combinacoes_validas['TIPO_GLOSA']))

# Lista para armazenar os DataFrames resultantes
base_cluster = []

# Loop para iterar sobre as combinações válidas
for hospital in hospitais:
    for convenio in convenios:
        for tipo in tipo_glosa:
            # Verifica se a combinação (hospital, convênio, tipo de glosa) é válida
            if (hospital, convenio, tipo) in combinacoes_validas_set:
                # Realiza o processo de clusterização para a combinação válida
                df_atual = clusterizacao.cria_cluster(clusterizacao.carrega_dataset(hospital, convenio, tipo))
                # Empilha o DataFrame da iteração na lista base_apriori
                base_cluster.append(df_atual)

# Agora empilha todos os DataFrames da lista base_cluster
base_cluster_df = pd.concat(base_cluster, ignore_index=True)

# Agora base_cluster_df é um único DataFrame com todos os dados empilhados
print(base_cluster_df)
print(f'Tamanho de base_cluster: {len(base_cluster_df)}')  # Exibe a quantidade de itens empilhados

# Ajustando o caminho base
caminho_base = r"\\08.Desenvolvimento\03.Dashboards\Cluster_Apriori"

# Concatenando o nome do arquivo ao caminho base
nome_do_arquivo_csv = f"{caminho_base}\\base_cluster_por_hospital.csv"

#exportar arquivo
base_cluster_df.to_csv(nome_do_arquivo_csv, index=False, encoding='utf-8')
print('Arquivo base_cluster_por_hospital.csv exportado')

#encerrar
print('Fim do script')
