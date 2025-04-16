
<h1 align="center">Clusterização de Glosas Hospitalares <br /> </h1>

1.0 Visão geral

No ramo da prestação de serviços de saúde, é comum ouvir falar sobre glosa hospitalar. As glosas correspondem a valores de faturamento que não são recebidos ou são recusados pelas operadoras de saúde — clínicas, hospitais e laboratórios — geralmente devido a problemas de comunicação ou inconsistências nas informações fornecidas.

Na maioria das vezes, as glosas ocorrem quando os dados enviados pelo prestador não coincidem com os registros da operadora. Por isso, evitar glosas é fundamental para manter a eficiência na gestão financeira das instituições de saúde.

Diante da relevância desse tema, propõe-se a criação de um modelo de clusterização.

Clusterização é uma técnica de aprendizado de máquina que consiste em agrupar elementos com características semelhantes, sem a necessidade de rótulos pré-definidos. Essa abordagem é especialmente útil para explorar padrões e identificar grupos naturais dentro de um conjunto de dados.

Para este caso específico, o objetivo da clusterização é agrupar os casos de glosa com características semelhantes, facilitando tanto a identificação das causas quanto a priorização dos grupos com maior impacto financeiro. Dessa forma, a análise torna-se mais estratégica, permitindo ações mais direcionadas para a redução das glosas e a otimização do faturamento.

2.0 Objetivos técnicos

Desenvolver modelos de clusterização segmentados por hospital, convênio e tipo de glosa, com o objetivo de identificar padrões e facilitar a análise das principais causas de glosas.

Foi implementada uma estrutura em loop, capaz de gerar automaticamente diferentes clusterizações para cada combinação de hospital, operadora e tipo de glosa.
Por exemplo:

- Para a base de dados 1, referente ao Hospital A, da Operadora B e do Tipo de Glosa C, foram identificados 3 grupos.

- Já para a base de dados 2, correspondente ao Hospital E, da Operadora F e do Tipo de Glosa G, foram identificados 5 grupos.

Essa rotina de criação dos modelos foi transformada em um processo automático, com a execução do script Python agendada por meio do Agendador de Tarefas do Windows, garantindo a atualização periódica dos dados sem necessidade de intervenção manual.

Além disso, um painel no Power BI será alimentado com os resultados dessas análises, permitindo o acompanhamento semanal da evolução das glosas, com foco na tomada de decisão mais rápida e estratégica por parte das áreas responsáveis.

3.0 Tecnologias Utilizadas

- Python: Utilizado para o processamento e modelagem dos dados, incluindo a criação dos modelos de clusterização e tratamento das bases segmentadas por hospital, operadora e tipo de glosa.

- Agendador de Tarefas do Windows: Responsável pela automação da execução do script Python, garantindo que os modelos sejam atualizados de forma periódica e sem necessidade de intervenção manual.

- Power BI: Ferramenta utilizada para a visualização e monitoramento dos resultados. Os dados processados são integrados ao painel para acompanhamento semanal das glosas, facilitando a análise e a tomada de decisões.
  
![pipeline](https://github.com/user-attachments/assets/4ff29d87-8d82-4e6a-8567-2797690b8d82)

  
4.0 Desenvolvimento 

5.0 Deploy 

6.0 Resultados
