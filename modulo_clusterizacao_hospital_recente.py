
class clusterizacao:
    
    def carrega_dataset(hospital, convenio, tipo_glosa):
    
        #banco de dados
        import cx_Oracle
        import pandas as pd
             
        #conectando ao banco de dados
        uid = "****"    # usuário
        pwd = "*******"   # senha
        db = "*****"  # string de conexão do Oracle, configurado no cliente Oracle, arquivo tnsnames.ora
         
        connection = cx_Oracle.connect(uid+"/"+pwd+"@"+db) #cria a conexão
        cursor = connection.cursor() # cria um cursor

        querystring = f"""WITH BASE_TRATA_NOMES_E_VAZIOS AS(
                    SELECT TASY.TB_GLOSA_APRIORI_RECENTE.*,
                        CASE
                            WHEN VALOR_COBRADO_GERAL IS NULL THEN 0
                            ELSE VALOR_COBRADO_GERAL
                        END AS COBRADO_ATUAL,
                        CASE
                            WHEN VALOR_GLOSA IS NULL THEN 0 
                            ELSE VALOR_GLOSA 
                        END AS GLOSA_ATUAL,
                        CASE 
                            WHEN VALOR_COBRADO_RELEVANCIA IS NULL THEN 0 
                            ELSE VALOR_COBRADO_RELEVANCIA 
                        END AS COBRADO_RELEVANCIA_ATUAL,
                        CASE
                            WHEN COBRADO_ANTERIOR IS NULL THEN 0
                            ELSE COBRADO_ANTERIOR
                        END AS COBRADO_MES_ANTERIOR,
                        CASE
                            WHEN GLOSA_ANTERIOR IS NULL THEN 0
                            ELSE GLOSA_ANTERIOR
                        END AS GLOSA_MES_ANTERIOR,
                        CASE
                            WHEN QTD_LINHAS_GLOSA IS NULL THEN 0
                            ELSE QTD_LINHAS_GLOSA
                        END AS QTD_LINHAS_GLOSADAS
                    FROM TASY.TB_GLOSA_APRIORI_RECENTE
                ),
                BASE_AGRUPADA AS (
                    SELECT MES_RECEBIMENTO,
                           HOSPITAL,
                           REGIONAL,
                           I_ITEM_CATEGORIA AS TIPO_DESPESA,
                           SETOR_N1,
                           SETOR_N2,
                           REPLACE(TRIM(TIPO_GRUPO), 'Não identificado-Não identificado', 'N/A-N/A') AS TIPO_GRUPO,
                           TIPO_ATENDIMENTO,
                           CONVENIO,
                           TIPO_GLOSA,
                           SUM(COBRADO_ATUAL) AS COBRADO_ATUAL,
                           SUM(COBRADO_MES_ANTERIOR) AS COBRADO_MES_ANTERIOR,
                           SUM(GLOSA_ATUAL) AS GLOSA_ATUAL,
                           SUM(GLOSA_MES_ANTERIOR) AS GLOSA_MES_ANTERIOR,
                           SUM(QTD_LINHAS_GLOSADAS) AS QTD_LINHAS_GLOSA,
                           CASE
                                WHEN (SUM(COBRADO_ATUAL) = 0) THEN 0
                                ELSE (SUM(GLOSA_ATUAL) / SUM(COBRADO_ATUAL))
                           END AS IND_GLOSA,
                           CASE
                                WHEN (SUM(COBRADO_MES_ANTERIOR) = 0) THEN 0
                                ELSE (SUM(GLOSA_MES_ANTERIOR) / SUM(COBRADO_MES_ANTERIOR))
                           END AS IND_GLOSA_ANTERIOR
                    FROM BASE_TRATA_NOMES_E_VAZIOS
                    GROUP BY MES_RECEBIMENTO,
                             HOSPITAL,
                             REGIONAL,
                             I_ITEM_CATEGORIA,
                             SETOR_N1,
                             SETOR_N2,
                             TIPO_GRUPO,
                             TIPO_ATENDIMENTO,
                             CONVENIO,
                             TIPO_GLOSA
                )
                
                SELECT MES_RECEBIMENTO,
                       HOSPITAL,
                       REGIONAL,
                       CONVENIO,
                       TIPO_DESPESA,
                       SETOR_N1,
                       SETOR_N2,
                       TIPO_GRUPO,
                       TIPO_ATENDIMENTO,
                       TIPO_GLOSA,
                       GLOSA_ATUAL,
                       IND_GLOSA,
                      (GLOSA_ATUAL - GLOSA_MES_ANTERIOR) AS SALTO_VALOR,
                      (IND_GLOSA - IND_GLOSA_ANTERIOR) AS SALTO_INDICE,
                       QTD_LINHAS_GLOSA
                FROM BASE_AGRUPADA
                WHERE HOSPITAL = '{hospital}' AND  CONVENIO = '{convenio}'  AND TIPO_GLOSA = '{tipo_glosa}'
                AND MES_RECEBIMENTO = ADD_MONTHS (TRUNC (SYSDATE, 'MM'), -1)
                ORDER BY MES_RECEBIMENTO
                """
        # Executar a query com variáveis
        cursor.execute(querystring)
        nome_colunas = [row[0] for row in cursor.description]

        base = pd.DataFrame(cursor.execute(str(querystring)),columns=nome_colunas)# consulta sql
        
        return base
        
        
            
    def carrega_dataset_hospitais():
    
        #banco de dados
        import cx_Oracle
        import pandas as pd
             
        #conectando ao banco de dados
        uid = "****"    # usuário
        pwd = "*******"   # senha
        db = "*****"  # string de conexão do Oracle
         
        connection = cx_Oracle.connect(uid+"/"+pwd+"@"+db) #cria a conexão
        cursor = connection.cursor() # cria um cursor

        querystring_hospital = """  SELECT DISTINCT HOSPITAL
                                    FROM TASY.TB_GLOSA_APRIORI_RECENTE
                                    ORDER BY HOSPITAL """

        # Executar a query com variáveis
        cursor.execute(querystring_hospital)
        nome_colunas_hospital = [row[0] for row in cursor.description]

        hospitais = pd.DataFrame(cursor.execute(str(querystring_hospital)),columns=nome_colunas_hospital)# consulta sql

        return hospitais
        
        

    def carrega_dataset_combinacoes():
        # Banco de dados
        import cx_Oracle
        import pandas as pd
            
        # Conectando ao banco de dados
        uid = "*****"    # Usuário
        pwd = "*****"   # Senha
        db = "****"  # String de conexão do Oracle
            
        connection = cx_Oracle.connect(uid + "/" + pwd + "@" + db)  # Cria a conexão
        cursor = connection.cursor()  # Cria um cursor

        querystring_combinacoes = """SELECT /*+PARALLEL(8)*/ DISTINCT HOSPITAL, CONVENIO, TIPO_GLOSA
                                    FROM TASY.TB_GLOSA_APRIORI_RECENTE
                                    WHERE CONVENIO IN ('CONVENIO A','CONVENIO B') 
                                    AND TIPO_GLOSA IN ('TIPO_GLOSA  A','TIPO_GLOSA B')
                                    ORDER BY HOSPITAL, CONVENIO, TIPO_GLOSA"""

        # Executar a query com variáveis
        cursor.execute(querystring_combinacoes)
        nome_colunas_combinacoes = [row[0] for row in cursor.description]

        combinacoes = pd.DataFrame(
        cursor.execute(str(querystring_combinacoes)), columns=nome_colunas_combinacoes)  # Consulta SQL
            
        return combinacoes
    
       
    def cria_cluster(base):
        # Bibliotecas
        import pandas as pd
        import warnings
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score

        # Ignora avisos
        warnings.simplefilter("ignore")
        
        # Verifica se o número de amostras é suficiente para realizar a clusterização
        n_amostras = len(base)
        
        if n_amostras == 0:
            return base

        # Padronizando os dados
        escala = StandardScaler()
        df_padrao = pd.DataFrame(escala.fit_transform(base[['GLOSA_ATUAL', 'IND_GLOSA', 'SALTO_VALOR', 'SALTO_INDICE']]),
                                 columns=['GLOSA_ATUAL', 'IND_GLOSA', 'SALTO_VALOR', 'SALTO_INDICE'])

        # Inicializando as variáveis
        maior_score = 0  # Inicializando com um valor baixo
        i_otimo = 2  # Variável para armazenar o número ótimo de clusters
        limite_cluster = 15  # Limite máximo de clusters


        
        # Caso o número de amostras seja menor que 2, não podemos fazer a clusterização
        if n_amostras < 2:
            print("Não há amostras suficientes para realizar a clusterização.")
            base['CLUSTER'] = 0
            return base

        # Ajusta o limite de clusters se for maior que o número de amostras - 1
        limite_cluster = min(limite_cluster, n_amostras - 1)

        # Realiza o cálculo do número ótimo de clusters com base na pontuação de Silhouette
        for i in range(2, limite_cluster ):  # Começa de 2 clusters até o limite
            clusterer = KMeans(n_clusters=i)
            preds = clusterer.fit_predict(df_padrao)
            score = silhouette_score(df_padrao, preds)

            # Atualiza a maior pontuação e o número de clusters ótimo
            if score > maior_score:
                maior_score = score
                i_otimo = i

        # Exibe o número de clusters ótimo
        print(f'O número ótimo de clusters é: {i_otimo}')
        print(f'A maior pontuação de Silhouette é: {maior_score}')

        # Realiza a clusterização com o número ótimo de clusters
        clus = KMeans(n_clusters=i_otimo, init='k-means++', max_iter=300, random_state=3)
        clus.fit(df_padrao)

        # Ajusta a coluna 'CLUSTER' no DataFrame original
        base.loc[:, 'CLUSTER'] = clus.labels_

        return base
