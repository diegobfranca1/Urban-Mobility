# Plano do MVP

## Visão

Criar uma ferramenta de inteligência territorial que ajude organizações públicas e privadas a explorar como os fluxos agregados entre zonas se relacionam com a localização de serviços, oportunidades e equipamentos. Casos potenciais incluem saúde preventiva, planejamento de escolas, varejo, lazer, eventos, imobiliário e planejamento urbano. O produto deve apresentar evidência e incerteza; não inferir a identidade ou o comportamento de indivíduos.

## Problema e hipótese

Dados de mobilidade de alta cobertura podem ser caros ou restritos. A hipótese de produto é que análises agregadas e contextualizadas por setor possam gerar valor com dados observados licenciados, pesquisas OD e/ou modelos transparentes, começando por um caso de uso estreito.

A hipótese ainda precisa ser validada com usuários e fornecedores. Não afirmar que uma solução multissetorial equivalente não existe sem pesquisa competitiva adicional.

## MVP técnico atual

- Aplicação web local Streamlit.
- Upload de CSV de atributos por zona.
- Modelo gravitacional sintético com três cenários de atratividade.
- Seleção de par OD, gráficos e exportação CSV.
- Dados de demonstração fictícios e avisos de limitações.

## Escopo deliberadamente excluído

- Rastreamento individual, localização em tempo real e identificação de trajetórias.
- Alegação de que as APIs do Google, Waze ou AWS entregam fluxos reais de pessoas.
- Previsões ou recomendações automatizadas para decisões sensíveis.
- Apresentação dos valores sintéticos como contagens observadas.
- Divisão modal detalhada e cálculo de rotas reais.

## Plano de validação por etapas

### Etapa 1 — validar o produto analítico

1. Confirmar unidade geográfica e escolher duas zonas/bairros que existam na base disponível.
2. Testar interface e cálculos com a fixture sintética.
3. Conversar com potenciais usuários de um único setor (por exemplo, planejamento de rede de saúde ou educação) para definir a decisão que o produto deve apoiar.

### Etapa 2 — validar com dados observados públicos

1. Baixar e inspecionar os recursos oficiais da Pesquisa OD Metrô-SP e respectivos metadados; não presumir que todos os microdados estejam disponíveis ou que “zona OD” seja sinônimo de bairro.
2. Registrar ano, amostra, ponderação, período, modos, motivos, geografia, licença e limitações.
3. Adaptar um importador para o esquema real, criar uma visualização separada de resultados observados e comparar com o modelo sintético em unidades compatíveis.
4. Relatar erros, cobertura e intervalos/incertezas disponíveis; não misturar observado e modelado numa única série sem rótulo.

### Etapa 3 — amostra comercial/institucional

Solicitar a pelo menos dois fornecedores uma prova de conceito limitada: uma cidade/região, poucas zonas, período histórico suficiente para sazonalidade, agregados por faixa horária/dia e documentação do método. Pedir preço do piloto e custo de expansão separadamente. Comparar cobertura e vieses, frequência, estabilidade de zona, retenção, licença para uso comercial, direito de armazenar e redistribuir derivados, limites de células pequenas e possibilidade de validação.

### Etapa 4 — produto

Só após demonstrar utilidade e viabilidade de dados: automatizar ingestão, versionamento, monitoramento de qualidade, API, autenticação e dashboards por setor. Avaliar contratação/armazenamento cloud conforme volume, segurança e contrato. AWS pode ser infraestrutura, não substituto da fonte de dados.

## Critérios de sucesso iniciais

- Usuários conseguem responder a uma pergunta decisória definida sem apoio de analista em todas as etapas.
- Fonte e tipo de dado (observado/modelado) ficam inequívocos em toda visualização/exportação.
- Resultados são reproduzíveis a partir de parâmetros e versão de dados.
- A validação mede diferença entre modelo e referência observada, não apenas qualidade visual.
- Privacidade, licença e custo são aceitos antes de escalar.

## Riscos principais

- **Representatividade:** uma amostra de app, operadora ou survey não necessariamente representa toda a população.
- **Inferência ecológica:** fluxos por zona não explicam comportamento individual.
- **Variação temporal:** uma pesquisa pontual não oferece série diária ou sazonal de 1–2 anos.
- **Geografia:** bairros oficiais, zonas OD e áreas comerciais podem não coincidir.
- **Privacidade:** fluxos para locais sensíveis podem expor grupos pequenos; suprimir células e avaliar risco de reidentificação.
- **Licenciamento:** acesso a API não implica direito de armazenar, derivar ou comercializar dados.
- **Viés decisório:** resultados não devem ser usados isoladamente para alocar recursos de saúde, segurança, educação ou crédito.
