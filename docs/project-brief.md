# Urban Mobility — informações do projeto

## Problema

Organizações podem se beneficiar de uma leitura agregada de movimentos entre zonas para contextualizar onde instalar serviços, planejar campanhas ou compreender acessibilidade e conexões territoriais. Dados comerciais de mobilidade podem ser caros e têm limites de cobertura, licenciamento e privacidade.

## Proposta

Uma camada de análise que combina fluxos OD autorizados (quando disponíveis) com dados socioespaciais públicos e ferramentas de exploração orientadas a decisões. O produto deve ser transparente sobre fonte, representatividade, método e incerteza.

## Casos de uso a investigar

- Saúde: padrões agregados de acesso a unidades de atendimento; não usar fluxos isolados para decisão clínica.
- Educação: áreas de origem de demanda potencial e acessibilidade a escolas.
- Varejo/imobiliário: conexões entre residência, emprego e serviços.
- Lazer/eventos: áreas de captação e comparação temporal agregada.
- Planejamento público: apoio a hipóteses de localização e acessibilidade, sempre com validação local.

## Princípios

1. Não coletar nem exibir trajetórias individuais.
2. Separar dado observado, dado modelado e dado calculado por rota.
3. Não alegar que resultados sintéticos são comportamento real.
4. Respeitar licença, LGPD, limiares de agregação e risco de inferência.
5. Comunicar limitações e não automatizar decisões sensíveis sem validação e supervisão.

## Estado atual

Protótipo de demonstração em Streamlit com matriz gravitacional sintética. Próxima etapa: confirmar e importar dados OD observados autorizados para uma região piloto, depois avaliar uma amostra comercial/institucional caso seja necessária atualização histórica contínua.
