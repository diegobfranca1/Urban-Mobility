# Esquema de dados e metodologia

## Arquivo de entrada

O MVP aceita CSV UTF-8 com uma linha por zona e as seguintes colunas obrigatórias:

| Coluna | Tipo | Significado |
|---|---|---|
| `zone` | texto único | Identificador/nome da zona OD |
| `population` | número ≥ 0 | População residente usada como proxy de produção de viagens |
| `jobs` | número ≥ 0 | Proxy de atratividade de destinos de trabalho |
| `services` | número ≥ 0 | Proxy de atratividade de serviços |
| `leisure` | número ≥ 0 | Proxy de atratividade de lazer |
| `latitude`, `longitude` | decimal | Coordenada representativa da zona; a distância calculada é em linha reta |

A coordenada representativa deve ser documentada (por exemplo, centroide oficial da zona). O demo não é dado oficial. Coordenadas servem apenas para distância geodésica aproximada, não para distância pela rede viária nem para identificar trajetos.

## Modelo atual

Para origem `i` e destino `j`, o modelo usa uma função gravitacional simples:

`w_ij = A_j^α × exp(-β × d_ij)`

`T_ij = (population_i × trip_rate) × w_ij / Σ_j(w_ij)`

- `A_j`: empregos, serviços ou lazer, escolhidos como cenário;
- `d_ij`: distância em linha reta, km;
- `α`: sensibilidade à atratividade;
- `β`: decaimento espacial por km;
- `trip_rate`: taxa hipotética para produzir uma escala de fluxos.

A distribuição é normalizada por origem. O parâmetro `trip_rate` controla a escala, mas não é calibrado. Os percentuais por origem são mais interpretáveis do que os volumes absolutos, porém também dependem dos proxies e parâmetros. No MVP não há perfil por hora/dia, sazonalidade, escolha modal, impedância por tempo de viagem, restrições de capacidade ou calibração empírica.

## Interpretação e validação

- `estimated_trips` é resultado do modelo, **não contagem de pessoas/viagens observadas**.
- `share_of_origin_pct` mostra a distribuição modelada dos destinos para uma origem.
- `share_total_pct` mostra a participação do par no total da matriz modelada.
- A distância é linha reta entre coordenadas, não rota percorrida.
- O demo usa nomes reais de algumas zonas de São Paulo, mas atributos fictícios; não use seus resultados para decisões de saúde, educação, segurança ou investimento.
- Uma futura calibração requer dados OD observados compatíveis em geografia e período. Deve haver separação entre período de calibração e validação quando possível, além de métricas e análise de sensibilidade.

## Futuras fontes observadas

A plataforma deve tratar fontes e modelos como componentes separados: (1) dados OD observados/agregados licenciados ou públicos; (2) variáveis socioespaciais públicas; (3) dados de rede/roteamento; (4) saídas de modelos sintéticos. Uma API de rotas pode fornecer distância/tempo de rota, mas não a quantidade de viagens efetivamente realizadas.

Antes de adicionar fonte externa, registrar fornecedor, cobertura, período, unidade espacial, método de geração, viés amostral, supressão de pequenos grupos, licença, retenção, custo e autorização para derivados/comercialização.
