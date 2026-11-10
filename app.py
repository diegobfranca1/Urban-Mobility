from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.urban_mobility.model import REQUIRED_COLUMNS, build_od_matrix

ROOT = Path(__file__).parent
DEMO_FILE = ROOT / "data" / "demo_zones.csv"
SCENARIOS = {
    "Trabalho": "jobs",
    "Serviços": "services",
    "Lazer": "leisure",
}

st.set_page_config(page_title="Urban Mobility | OD sintética", page_icon="🗺️", layout="wide")
st.title("Urban Mobility — laboratório de matrizes OD")
st.caption("Protótipo de fluxos **modelados**, não observações reais de viagens. Consulte metodologia e limitações antes de interpretar os resultados.")

with st.sidebar:
    st.header("Dados e parâmetros")
    uploaded = st.file_uploader("Carregue um CSV de zonas", type=["csv"], help="Esquema esperado: zone,population,jobs,services,leisure,latitude,longitude")
    st.markdown("[Ver esquema e metodologia](docs/data-and-method.md)")
    scenario_label = st.selectbox("Cenário de atratividade", list(SCENARIOS))
    alpha = st.slider("Expoente de atratividade (α)", 0.1, 2.0, 1.0, 0.1)
    beta = st.slider("Decaimento por distância (β, km⁻¹)", 0.0, 1.0, 0.15, 0.01)
    trip_rate = st.number_input("Taxa hipotética de viagens por residente", min_value=0.01, max_value=5.0, value=0.6, step=0.05, help="Parâmetro ilustrativo. Não é uma taxa observada nem calibrada.")
    include_intra = st.checkbox("Incluir viagens intrazonais", value=False)

try:
    if uploaded:
        zones = pd.read_csv(uploaded)
        data_label = f"Arquivo carregado: {uploaded.name}"
    else:
        zones = pd.read_csv(DEMO_FILE)
        data_label = "Demonstração sintética — não são dados observados"

    missing = sorted(set(REQUIRED_COLUMNS) - set(zones.columns))
    if missing:
        st.error("Colunas obrigatórias ausentes: " + ", ".join(missing))
        st.stop()

    scenario = SCENARIOS[scenario_label]
    result = build_od_matrix(
        zones=zones,
        attraction_column=scenario,
        alpha=alpha,
        beta=beta,
        trip_rate=trip_rate,
        include_intrazonal=include_intra,
    )
except (ValueError, KeyError) as exc:
    st.error(f"Não foi possível gerar a matriz: {exc}")
    st.stop()

st.info(f"**Fonte:** {data_label}. Valores e resultados dependem dos parâmetros escolhidos; use apenas para testar o fluxo analítico.")

left, right = st.columns(2)
with left:
    origin = st.selectbox("Origem", sorted(zones["zone"].astype(str).unique()), index=0)
with right:
    destination_options = sorted(z for z in zones["zone"].astype(str).unique() if include_intra or z != origin)
    destination = st.selectbox("Destino", destination_options, index=0)

pair = result[(result.origin == origin) & (result.destination == destination)]
if pair.empty:
    st.warning("Não há fluxo calculado para este par com os parâmetros selecionados.")
else:
    row = pair.iloc[0]
    m1, m2, m3 = st.columns(3)
    m1.metric("Fluxo modelado", f"{row.estimated_trips:,.0f}", help="Unidades hipotéticas geradas pelo modelo; não são contagens reais.")
    m2.metric("Participação na origem", f"{row.share_of_origin_pct:.1f}%")
    m3.metric("Distância aproximada", f"{row.distance_km:.1f} km", help="Distância em linha reta entre coordenadas fornecidas, não distância de rota.")

st.subheader("Destinos a partir da origem selecionada")
origin_flows = result[result.origin == origin].sort_values("estimated_trips", ascending=False)
bar = px.bar(origin_flows, x="destination", y="share_of_origin_pct", labels={"destination": "Destino", "share_of_origin_pct": "Participação na origem (%)"}, title=f"Distribuição modelada de destinos — {origin}")
st.plotly_chart(bar, use_container_width=True)

st.subheader("Matriz OD — participação do total modelado")
share_matrix = result.pivot(index="origin", columns="destination", values="share_total_pct").fillna(0)
heatmap = px.imshow(share_matrix, labels={"x": "Destino", "y": "Origem", "color": "% do total"}, aspect="auto", title="Matriz sintética (%)")
st.plotly_chart(heatmap, use_container_width=True)

with st.expander("Inspecionar e exportar tabela OD"):
    st.dataframe(result, use_container_width=True, hide_index=True)
    payload = result.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar matriz OD CSV", payload, file_name="synthetic_od_matrix.csv", mime="text/csv")

st.warning("Este protótipo não acessa APIs do Google, Waze ou AWS e não recebe dados de localização. Rotas calculadas por uma API não revelam quantas pessoas efetivamente viajaram. Antes de usar para decisões reais, calibre e valide contra dados observados adequados.")
