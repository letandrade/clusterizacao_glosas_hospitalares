
<h1 align="center">Clusterização de Glosas Hospitalares <br /> </h1>

## **1.0 Visão geral**

No ramo da prestação de serviços de saúde é comum ouvir falar sobre glosa hospitalar. As glosas correspondem a valores de faturamento que não são recebidos ou são recusados pelas operadoras de saúde (convênios), geralmente devido a problemas de comunicação ou inconsistências nas informações fornecidas pelo prestador. 

Na maioria das vezes, as glosas ocorrem quando os dados enviados pelo prestador não coincidem com os registros da operadora. Por isso, evitar glosas é fundamental para manter a eficiência na gestão financeira das instituições de saúde.

Diante da relevância desse tema, propõe-se a criação de um modelo de clusterização.

Clusterização é uma técnica de aprendizado de máquina não-supervisionado que consiste em agrupar elementos com características semelhantes, sem a necessidade de rótulos pré-definidos. Essa abordagem é especialmente útil para explorar padrões e identificar grupos naturais dentro de um conjunto de dados.

Para este caso específico, o objetivo da clusterização é agrupar os casos de glosa com características semelhantes, facilitando tanto a identificação das causas quanto a priorização dos grupos com maior impacto financeiro. Dessa forma, a análise torna-se mais estratégica, permitindo ações mais direcionadas para a redução das glosas e a otimização do faturamento.

Por questões de confidencialidade e segurança da informação, o nome da rede de saúde e os valores financeiros envolvidos neste projeto foram anonimizados.

## **2.0 Objetivos técnicos**

Desenvolver modelos de clusterização segmentados por hospital, convênio e tipo de glosa, com o objetivo de identificar padrões e facilitar a análise das principais causas de glosas.

Foi implementada uma estrutura em loop, capaz de gerar automaticamente diferentes clusterizações para cada combinação de hospital, operadora e tipo de glosa.
Por exemplo:

- Para a base de dados 1, referente ao Hospital A, da Operadora B e do Tipo de Glosa C, foram identificados 3 grupos.

- Já para a base de dados 2, correspondente ao Hospital E, da Operadora F e do Tipo de Glosa G, foram identificados 5 grupos.

Essa rotina de criação dos modelos foi transformada em um processo automático, com a execução do script Python agendada por meio do Agendador de Tarefas do Windows, garantindo a atualização periódica dos dados sem necessidade de intervenção manual.

Além disso, um painel no Power BI será alimentado com os resultados dessas análises, permitindo o acompanhamento semanal da evolução das glosas, com foco na tomada de decisão mais rápida e estratégica por parte das áreas responsáveis.

## **3.0 Ferramentas utilizadas**

![{1743A47F-6D12-4614-BA3F-4EF85A242CC9}](https://github.com/user-attachments/assets/90972919-4370-48c1-8b54-51c923b1976a)

- SQL: Utilizado para construção da bases de dados.

- Python: Utilizado para o processamento e modelagem dos dados, incluindo a criação dos modelos de clusterização e tratamento das bases segmentadas por hospital, operadora e tipo de glosa. É importante dizer que foi utilizado o ambiente Anaconda. 

- Agendador de Tarefas do Windows: Responsável pela automação da execução do script Python, garantindo que os modelos sejam atualizados de forma periódica e sem necessidade de intervenção manual.

- Power BI: Ferramenta utilizada para a visualização e monitoramento dos resultados. Os dados processados são integrados ao painel para acompanhamento semanal das glosas, facilitando a análise e as correções de glosa.
  
## **4.0 Desenvolvimento**

Todos os passos a seguir estão detalhados nos módulos e arquivos de texto em anexo. 

### **4.1 Construção da base de dados em SQL**

A base de dados foi extraída de um banco de dados, esse script faz toda a seleção de variáveis e tratamento. E entrega a base no formato de entrada do algoritmo. 

A query construída foi chamada através da conexão com o banco de dados Oracle executada através da biblioteca cx_oracle.

### **4.2 Módulo de Clusterização para Análise de Glosas Hospitalares**

Este módulo python (modulo_clusterizacao_hospital_recente.py) tem como objetivo realizar análises de clusterização em dados de glosas hospitalares, extraídos diretamente de um banco de dados Oracle. Ele utiliza uma consulta SQL para coletar e tratar os dados relevantes e aplica o algoritmo de Machine Learning K-Means para agrupar padrões semelhantes de glosa.

Funcionalidades principais:

- Conexão Oracle: Acesso direto ao banco de dados Oracle para execução da query.
  
- Consulta customizada: Extração de dados por hospital, convênio e tipo de glosa, com tratamento de nulos e cálculos de indicadores como salto de valor e índice de glosa.
  
- Clusterização inteligente: Aplicação do algoritmo K-Means com escolha automática do número ótimo de clusters baseado no índice de Silhouette.
  
- Escalabilidade: Limitação dinâmica do número de clusters com base na quantidade de amostras disponíveis.
  
- Exploração de variáveis relevantes: Agrupamento baseado em GLOSA_ATUAL, IND_GLOSA, SALTO_VALOR, e SALTO_INDICE.

Essa solução permite identificar padrões e anomalias no comportamento das glosas, sendo útil para auditoria médica, análises operacionais e estratégias de redução de perdas.

### **4.3 Módulo de execução de funções**

Este módulo python (modulo_clusterizacao_hospital_recente_loop.py) executa de forma automatizada as funções do módulo anterior (modulo_clusterizacao_hospital_recente.py) para cada combinação válida de hospital, convênio e tipo de glosa, a fim de gerar uma base consolidada de clusters.

Funcionalidades principais:

- Leitura de dados específicos por hospital, convênio e tipo de glosa.
  
- Verificação das combinações válidas com base nos hospitais, convênios e tipo de glosa presentes na base de dados. 
  
- Execução de clusterização com K-Means, utilizando padronização e métricas como silhouette score para qualidade dos clusters.
  
- Empilhamento dos resultados em um único DataFrame (base_cluster_df) para análise consolidada.
  
- Exportação automatizada da base final para um arquivo .csv centralizado em um diretório compartilhado.

### **4.4 Agendamento do script de loop no Windows**

Funcionalidades principais:

- Criação um arquivo .bat (executar_cluster_apriori_recente.bat) responsável por executar o script Python de clusterização.

- Organização dos arquivos necessários (modulo_clusterizacao_hospital_recente.py, modulo_clusterizacao_hospital_recente_loop.py, executar_cluster_apriori_recente.bat) em uma pasta dedicada dentro de um diretório de trabalho.

- Configurar uma nova tarefa no Agendador de Tarefas do Windows, definindo a execução automática com frequência semanal e fazer o apontamento para o arquivo .bat presente na pasta anterior. Caminho: Agendador de Tarefas > Criar tarefa < Ações < Novo. Preencha o campo Programa/Script com o caminho do arquivo .bat e o campo Iniciar em com o caminho da pasta com os arquivos. 

<img width="468" alt="1" src="https://github.com/user-attachments/assets/4a555246-3694-43bd-85cb-2efd438a75d0" />

<img width="497" alt="2" src="https://github.com/user-attachments/assets/cb72291a-3acd-4e0e-b3b2-6c6cdc886ed5" />

- Ao final de cada execução, o script exporta um arquivo.csv (base_cluster_por_hospital.csv) contendo o empilhamento dos clusters gerados, armazenando-o no diretório especificado no código.

- O tutorial a seguir esclarece de forma detalhada a implementação. https://medium.com/sucessoemvendasacademy/como-executar-scripts-de-python-de-forma-autom%C3%A1tica-e-recorrente-windows-867db62523bf

### **4.5 Dashboard de Clusterização**

Funcionalidades principais:

- Importação do arquivo base_cluster_por_hospital.csv no Power BI desktop.
- Construção dos visuais.
- Criação dos slicers por hospital, convênio e tipo de glosa. Para cada chave são apresentados os agrupamentos criados.

<img width="578" alt="{2EBF3867-D52B-4331-B744-EFB1714929A6}" src="https://github.com/user-attachments/assets/dd001b7c-e420-44a4-a9a2-9bbc3aef63c2" />

<img width="581" alt="{F48372F0-D613-40CD-A70F-0104656E920F}" src="https://github.com/user-attachments/assets/963b019b-fe6c-47a2-bb56-557d6afb8fee" />


## **5.0 Resultados**

Entre janeiro e abril de 2025, a ferramenta clusterização em conjunto com a ferramenta de [regras de associação](https://github.com/letandrade/regras_de_associacao_glosas_hospitalares) identificaram 37 casos relevantes de glosas somando aproximadamente R$5 milhões, cuja tratativa resultou em uma glosa evitada anualizada de aproximadamente R$60 milhões.

Vale destacar que a ferramenta fornece os valores mensais de glosa por caso. Após a correção da causa da glosa, a perda financeira deixa de ocorrer. Por isso, o principal indicador de desempenho é a glosa evitada, ou seja, o valor anual que seria perdido caso os problemas não fossem identificados e corrigidos.

Além disso, a ferramenta foi incorporada como um processo autônomo, com atualizações semanais, garantindo agilidade e escalabilidade na detecção e prevenção de glosas ao longo do tempo.


