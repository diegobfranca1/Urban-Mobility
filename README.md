# Urban Mobility — MVP de matrizes OD sintéticas

Protótipo para explorar padrões agregados de deslocamento entre zonas urbanas e testar uma metodologia de inteligência territorial. O projeto começa com uma matriz **modelada/sintética**, não com viagens observadas de usuários.

> **Importante:** Google Maps, Waze, AWS e APIs de roteamento não devem ser tratados como fontes de contagens reais de viagens entre bairros. O MVP usa distância entre zonas e atratividade socioespacial como parâmetros de um modelo gravitacional simples. Os resultados são hipóteses para exploração, não evidência de mobilidade real nem recomendação de política pública.

## O que já está no repositório

- Aplicativo Streamlit para gerar e visualizar matrizes OD por cenário (trabalho, serviços, lazer).
- Dados de demonstração sintéticos, com zonas de São Paulo apenas como exemplos ilustrativos.
- Upload de CSV de zonas, configuração de parâmetros e exportação dos resultados.
- Validações de dados e testes unitários do modelo.
- Documentação de visão, metodologia, fontes de dados, riscos, plano de validação e roteiro de obtenção de dados observados.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

O app carrega `data/demo_zones.csv` por padrão. O usuário pode carregar seu próprio arquivo CSV seguindo o esquema em [`docs/data-and-method.md`](docs/data-and-method.md).

## Rodar testes

```bash
pytest
```

## Metodologia do protótipo

Para cada origem, o modelo estima uma produção proporcional à população e distribui essa produção entre destinos segundo a atratividade do destino e uma função de decaimento com a distância. A forma geral é:

`T_ij = P_i × (A_j^α × exp(-β × d_ij)) / Σ_j(A_j^α × exp(-β × d_ij))`

O usuário pode escolher a camada de atratividade (empregos, serviços ou lazer), o expoente `α`, a sensibilidade à distância `β` e uma taxa hipotética de viagens por residente. Isso produz uma matriz sintética reproduzível. Não estima o número real de viagens sem calibração e dados observados.

## Próximos passos

1. Confirmar a disponibilidade, formato, licença e granularidade dos dados oficiais OD de São Paulo.
2. Usar uma pesquisa OD pública como referência de calibração/validação, sem confundir sua data de coleta com mobilidade atual.
3. Comparar a matriz sintética com uma matriz observada compatível em zonas e período; registrar erro e limitações.
4. Solicitar a fornecedores uma amostra agregada e um piloto limitado, comparando custo, cobertura, temporalidade, método e direitos de uso.
5. Só então decidir se o produto deve consumir dados licenciados, pesquisa amostral própria, registros administrativos ou combinar fontes.

Veja o plano completo em [`docs/mvp-plan.md`](docs/mvp-plan.md) e a análise preliminar de fontes em [`docs/data-sources-and-benchmark.md`](docs/data-sources-and-benchmark.md).

## Privacidade e uso responsável

O app não coleta localização individual nem dados pessoais. Não carregue dados identificáveis. Uma futura integração com dados agregados ainda exige avaliação da origem, base legal, contrato/licença, risco de reidentificação e limiares mínimos de publicação. Consulte assessoria jurídica e de privacidade antes de qualquer piloto com dados de terceiros.

## Licença

O código deste protótipo é disponibilizado sob MIT; consulte [`LICENSE`](LICENSE). Isso não concede direitos sobre dados externos. Cada dataset mantém sua própria licença e termos.
