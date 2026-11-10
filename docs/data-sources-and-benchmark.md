# Fontes e benchmark preliminar

Este é um mapa inicial para orientar diligência, não uma verificação contratual nem confirmação de disponibilidade/preço em uma cidade. Produtos e condições mudam; validar diretamente com os fornecedores e ler termos vigentes antes de construir dependências.

## Distinção essencial

- **OD observado/agregado:** estima viagens que ocorreram, normalmente via survey, registros de mobilidade ou dados agregados de celulares/apps.
- **Roteamento:** calcula caminhos/tempos para pares consultados. Não informa o volume de pessoas que realmente percorreu o par.
- **Tráfego:** velocidade, incidentes ou condições em vias. Não equivale automaticamente a viagens pessoa-a-pessoa entre bairros.
- **Modelagem:** aproxima fluxos a partir de população, empregos, serviços, distância/tempo e hipóteses. Deve ser rotulada como estimativa.

## Candidatos e o que investigar

| Fonte / categoria | Potencial para este caso | Limite a considerar | Próxima ação |
|---|---|---|---|
| Pesquisa OD Metrô-SP | Dados observados amostrais e referência metodológica; potencial para validar o MVP na RMSP | Edições pontuais, geografia própria, disponibilidade/licença variam por recurso | Inspecionar página, arquivos, dicionário e licença: [Metrô-SP Pesquisa OD](https://www.metro.sp.gov.br/pesquisa-od/) e [apresentação OD 2023](https://www.metro.sp.gov.br/2024/03/26/conheca-a-pesquisa-od/) |
| Pesquisas OD de outras regiões | Referência observada por zonas e motivos/modos, conforme edição | Cobertura e recência variam muito; não são séries contínuas | Procurar órgão metropolitano/municipal e portal de dados da cidade escolhida |
| Google Maps Platform | Rotas, distâncias/tempos e lugares podem enriquecer um modelo | Não assumir que fornece matriz de fluxos reais nem que respostas podem ser armazenadas indefinidamente; verificar termos e preços | Usar apenas para a função documentada e consultar documentação/termos oficiais: [APIs Google Maps](https://developers.google.com/maps/apis-by-platform?hl=pt-br) |
| Waze for Cities | Possível parceria para dados de trânsito/incidentes com entidades elegíveis | Não confundir alertas/condições de vias com OD de pessoas; elegibilidade e acesso dependem do programa | Consultar [Waze for Cities](https://www.waze.com/ccp) e perguntar explicitamente sobre histórico, cobertura e campos disponíveis |
| AWS | Armazenamento, processamento, catálogo/marketplace de dados de terceiros | AWS é infraestrutura/mercado, não fonte primária automática de mobilidade urbana | Verificar [AWS Data Exchange](https://aws.amazon.com/data-exchange/) por cobertura Brasil, licença, atualização e histórico antes de comprar |
| Uber Movement | Historicamente ofereceu dados agregados de mobilidade/tempos em algumas cidades | Disponibilidade atual, cidades, granularidade e possibilidade de matriz de volumes OD precisam ser conferidas; tempo de viagem não é volume | Consultar diretamente [Uber Movement](https://movement.uber.com/) e verificar quais produtos/datasets estão acessíveis agora |
| Meta Data for Good / Apple | Iniciativas e produtos de dados agregados podem atender a pesquisa ou emergências em escopos específicos | Não presumir API comercial, cobertura contínua, OD por bairro ou acesso aberto no Brasil | Verificar programas vigentes, critérios de elegibilidade, licença e formato; não criar dependência sem confirmação |
| Operadoras e agregadores de localização | Maior potencial de cobertura ampla e histórico contínuo por zonas | Negociação B2B, custo, viés de cobertura, metodologia, LGPD e licença; “anonimizado” não basta sem análise | Solicitar piloto agregado e documentação técnica/jurídica a Claro, Vivo, TIM e fornecedores relevantes |
| Bilhetagem/transporte público | Fluxos efetivos dos usuários daquele sistema e horários | Cobertura modal/populacional parcial; dados podem ser restritos; transferência/integração pode não revelar origem residencial | Buscar parceria com operador/órgão e pedir tabelas agregadas e termos de uso |
| App/painel voluntário próprio | Pode fornecer série contínua sobre participantes | Viés de seleção e custo de aquisição; não representa a cidade sem desenho amostral/ponderação | Usar apenas como complemento ou estudo piloto metodológico com consentimento e avaliação ética |
| IBGE, GeoSampa e portais públicos | População, limites e variáveis socioespaciais para contextualizar/calibrar | Não são, por si sós, observações contínuas de viagens urbanas entre bairros | [API de dados IBGE](https://servicodados.ibge.gov.br/api/docs/), [GeoSampa](https://geosampa.prefeitura.sp.gov.br/) |

## Perguntas obrigatórias para fornecedores

1. Quais cidades, zonas, períodos históricos e faixas temporais estão realmente cobertos?
2. O produto entrega fluxos/participações OD ou apenas presença, velocidade, alertas, rotas ou tempos?
3. Qual é a fonte de sinal, população amostral, cobertura de dispositivos, ponderação e limiar de publicação?
4. Os dados distinguem residentes, visitantes e trabalhadores? Como definem uma visita/viagem e o domicílio?
5. Qual é a granularidade mínima e como mudaram os polígonos ao longo do histórico?
6. Qual é o custo de amostra/piloto, licença anual e expansão? Existe taxa de setup?
7. É permitido armazenar, comparar séries, criar derivados, exibir a clientes e exportar resultados?
8. Quais são as salvaguardas contra reidentificação, política de retenção e responsabilidades LGPD?
9. Há documentação e amostra de dados para avaliar antes de contratar?
10. A empresa permite validar contra uma pesquisa OD ou outra referência independente?

## Conclusão de diligência

O produto do MVP pode ser desenvolvido sem um fornecedor de big data: o protótipo atual testa uma metodologia gravitacional sintética e uma experiência de análise. Para afirmar padrões reais e atuais, será necessário obter uma fonte observada — uma pesquisa OD pública para validação inicial, uma parceria com operador de transporte, ou uma amostra licenciada de telecom/fornecedor de localização. APIs de mapa, Waze e AWS não devem ser apresentadas como substitutos automáticos dessa fonte.

A hipótese de um produto multissetorial continua sendo uma hipótese de mercado. O diferencial potencial pode estar em combinar uma fonte autorizada de fluxo agregado com camadas socioespaciais e fluxos de trabalho por setor, mas custo, cobertura e demanda precisam ser comprovados num piloto.
