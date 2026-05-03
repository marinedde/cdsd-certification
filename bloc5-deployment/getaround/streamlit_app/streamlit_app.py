import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

# ── Configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="GetAround Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div { color: #e0e0e0 !important; }
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-top: 3px solid #e63946;
    }
    [data-testid="stMetricValue"] { color: #e63946 !important; font-size: 1.8em !important; }
    h1 { color: #1a1a2e !important; }
    h3 { color: #457b9d !important; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e63946, #c1121f) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Données ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_excel("get_around_delay_analysis.xlsx")

@st.cache_data
def compute_analysis(df):
    connected = df[df["previous_ended_rental_id"].notna()].copy()
    prev_delay = df[["rental_id", "delay_at_checkout_in_minutes"]].rename(
        columns={"rental_id": "previous_ended_rental_id",
                 "delay_at_checkout_in_minutes": "prev_driver_delay"}
    )
    connected = connected.merge(prev_delay, on="previous_ended_rental_id", how="left")
    problematic = connected[
        connected["prev_driver_delay"] > connected["time_delta_with_previous_rental_in_minutes"]
    ]
    results = []
    for scope in ["all", "connect", "mobile"]:
        df_scope = connected if scope == "all" else connected[connected["checkin_type"] == scope]
        df_prob = problematic if scope == "all" else problematic[problematic["checkin_type"] == scope]
        for t in range(0, 721, 30):
            solved = df_prob[df_prob["prev_driver_delay"] <= t]
            blocked = df_scope[df_scope["time_delta_with_previous_rental_in_minutes"] < t]
            results.append({
                "scope": scope, "threshold": t,
                "cases_solved": len(solved),
                "pct_solved": round(len(solved) / len(df_prob) * 100, 1) if len(df_prob) > 0 else 0,
                "rentals_blocked": len(blocked),
                "pct_blocked": round(len(blocked) / len(df) * 100, 1)
            })
    return connected, problematic, pd.DataFrame(results)

df = load_data()
connected, problematic, df_results = compute_analysis(df)
df_delay = df[df["delay_at_checkout_in_minutes"].notna()].copy()


# ── Sidebar — meme pattern qu'OncoPrint ─────────────────────────
st.sidebar.title("GetAround")
st.sidebar.markdown("Analytics Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Vue generale", "Analyse des retards", "Simulateur de seuil", "Prediction de prix"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Jedha CDSD - Bloc 5")
st.sidebar.caption("Deploiement 2026")
st.sidebar.caption(f"{len(df):,} locations analysees")
st.sidebar.caption("GradientBoosting R2=0.756")


# ══════════════════════════════════════════════════════════════════
# PAGE 1 — VUE GENERALE
# ══════════════════════════════════════════════════════════════════
if page == "Vue generale":
    st.title("Vue generale")
    st.markdown("Analyse des retards au checkout pour aider le **Product Manager** a definir le seuil minimum entre deux locations.")
    st.markdown("---")

    total_late = len(df_delay[df_delay["delay_at_checkout_in_minutes"] > 0])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total locations", f"{len(df):,}")
    col2.metric("Retours en retard", f"{total_late:,}",
                f"{total_late/len(df_delay)*100:.1f}% des retours")
    col3.metric("Cas problematiques", f"{len(problematic):,}",
                f"{len(problematic)/len(connected)*100:.1f}% des enchainées")
    col4.metric("Delai median retard",
                f"+{df_delay[df_delay['delay_at_checkout_in_minutes']>0]['delay_at_checkout_in_minutes'].median():.0f} min")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        checkin_counts = df["checkin_type"].value_counts().reset_index()
        checkin_counts.columns = ["Type", "Nombre"]
        fig = px.pie(checkin_counts, values="Nombre", names="Type",
                     title="Repartition des types de checkin",
                     color_discrete_map={"mobile": "#4361ee", "connect": "#e63946"},
                     hole=0.4)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(showlegend=False, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Retards par type de checkin")
        late_stats = []
        for ctype in ["mobile", "connect"]:
            sub = df_delay[df_delay["checkin_type"] == ctype]
            late_sub = sub[sub["delay_at_checkout_in_minutes"] > 0]
            late_stats.append({
                "Type": ctype.capitalize(),
                "Total retours": f"{len(sub):,}",
                "En retard": f"{len(late_sub):,}",
                "Pct en retard": f"{len(late_sub)/len(sub)*100:.1f}%",
                "Delai median": f"{late_sub['delay_at_checkout_in_minutes'].median():.0f} min",
            })
        st.dataframe(pd.DataFrame(late_stats), use_container_width=True, hide_index=True)

        prob_by_type = problematic["checkin_type"].value_counts().reset_index()
        prob_by_type.columns = ["Type", "Cas"]
        fig2 = px.bar(prob_by_type, x="Type", y="Cas", color="Type", text="Cas",
                      title="Cas problematiques par type",
                      color_discrete_map={"mobile": "#4361ee", "connect": "#e63946"})
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False, height=240, margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.info("57.5% des conducteurs rendent la voiture en retard (mediane +9 min). Mobile est plus problematique (61.4%) que Connect (42.9%). Sur les locations enchainées, 218 cas ont cause un impact direct sur le conducteur suivant.")


# ══════════════════════════════════════════════════════════════════
# PAGE 2 — ANALYSE DES RETARDS
# ══════════════════════════════════════════════════════════════════
elif page == "Analyse des retards":
    st.title("Analyse des retards")
    st.markdown("Distribution detaillee des delais au checkout et impact sur les conducteurs suivants.")
    st.markdown("---")

    checkin_filter = st.selectbox(
        "Filtrer par type de checkin",
        ["Tous", "Mobile uniquement", "Connect uniquement"]
    )
    if checkin_filter == "Mobile uniquement":
        df_plot = df_delay[df_delay["checkin_type"] == "mobile"]
    elif checkin_filter == "Connect uniquement":
        df_plot = df_delay[df_delay["checkin_type"] == "connect"]
    else:
        df_plot = df_delay.copy()

    df_filtered = df_plot[
        (df_plot["delay_at_checkout_in_minutes"] >= -300) &
        (df_plot["delay_at_checkout_in_minutes"] <= 600)
    ]
    fig = px.histogram(
        df_filtered, x="delay_at_checkout_in_minutes",
        color="checkin_type", nbins=80,
        title="Distribution des delais au checkout",
        labels={"delay_at_checkout_in_minutes": "Delai (minutes)", "checkin_type": "Type"},
        color_discrete_map={"mobile": "#4361ee", "connect": "#e63946"},
        barmode="overlay", opacity=0.75
    )
    fig.add_vline(x=0, line_dash="dash", line_color="#333",
                  annotation_text="Heure prevue", annotation_position="top right")
    fig.update_layout(height=380, margin=dict(t=50, b=40, l=40, r=20))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.histogram(
            connected[connected["time_delta_with_previous_rental_in_minutes"] <= 720],
            x="time_delta_with_previous_rental_in_minutes",
            color="checkin_type", nbins=50,
            title="Temps entre deux locations consecutives",
            labels={"time_delta_with_previous_rental_in_minutes": "Temps (min)", "checkin_type": "Type"},
            color_discrete_map={"mobile": "#4361ee", "connect": "#e63946"},
            barmode="overlay", opacity=0.75
        )
        fig2.update_layout(height=320, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.histogram(
            problematic[problematic["prev_driver_delay"] <= 600],
            x="prev_driver_delay", color="checkin_type", nbins=40,
            title="Retards causant un impact sur le conducteur suivant",
            labels={"prev_driver_delay": "Retard precedent (min)", "checkin_type": "Type"},
            color_discrete_map={"mobile": "#4361ee", "connect": "#e63946"},
            barmode="overlay", opacity=0.75
        )
        fig3.update_layout(height=320, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig3, use_container_width=True)

    st.info(f"La majorite des retards problematiques sont inferieurs a 120 minutes. Le time delta median entre deux locations est de {connected['time_delta_with_previous_rental_in_minutes'].median():.0f} minutes.")


# ══════════════════════════════════════════════════════════════════
# PAGE 3 — SIMULATEUR DE SEUIL
# ══════════════════════════════════════════════════════════════════
elif page == "Simulateur de seuil":
    st.title("Simulateur de seuil")
    st.markdown("Trouvez le meilleur compromis entre **cas problematiques resolus** et **revenus impactes**.")
    st.markdown("---")

    col_ctrl, col_graph = st.columns([1, 2])

    with col_ctrl:
        st.markdown("### Parametres")
        threshold = st.slider("Seuil minimum (minutes)", 0, 720, 120, step=30)
        scope = st.radio(
            "Scope",
            ["all", "connect", "mobile"],
            format_func=lambda x: {
                "all": "Toutes les voitures",
                "connect": "Connect uniquement",
                "mobile": "Mobile uniquement"
            }[x]
        )

        n_prob = len(problematic) if scope == "all" else len(
            problematic[problematic["checkin_type"] == scope]
        )
        row = df_results[
            (df_results["threshold"] == threshold) &
            (df_results["scope"] == scope)
        ].iloc[0]

        st.markdown("---")
        st.metric("Cas resolus",
                  f"{int(row['cases_solved'])} / {n_prob}",
                  f"{row['pct_solved']}% des cas problematiques")
        st.metric("Locations bloquees",
                  f"{int(row['rentals_blocked'])}",
                  f"-{row['pct_blocked']}% du revenu",
                  delta_color="inverse")

        if row["pct_solved"] >= 60 and row["pct_blocked"] <= 5:
            st.success(f"Bon compromis a {threshold} min")
        elif row["pct_solved"] < 40:
            st.warning("Seuil trop bas")
        else:
            st.warning("Impact eleve sur les revenus")

    with col_graph:
        df_scope_plot = df_results[df_results["scope"] == scope]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_scope_plot["threshold"], y=df_scope_plot["pct_solved"],
            mode="lines+markers", name="% cas resolus",
            line=dict(color="#2a9d8f", width=2.5), marker=dict(size=5)
        ))
        fig.add_trace(go.Scatter(
            x=df_scope_plot["threshold"], y=df_scope_plot["pct_blocked"],
            mode="lines+markers", name="% locations bloquees",
            line=dict(color="#e63946", width=2.5), marker=dict(size=5)
        ))
        fig.add_vline(x=threshold, line_dash="dash", line_color="#457b9d", line_width=2,
                      annotation_text=f"  {threshold} min",
                      annotation_font_color="#457b9d")
        fig.update_layout(
            title=f"Trade-off - scope : {scope}",
            xaxis_title="Seuil (minutes)", yaxis_title="Pourcentage (%)",
            hovermode="x unified", height=350,
            legend=dict(orientation="h", y=-0.25),
            margin=dict(t=50, b=70, l=40, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            df_results[df_results["scope"].isin(["all", "connect", "mobile"])],
            x="threshold", y="pct_solved", color="scope",
            title="% cas resolus selon le scope", markers=True,
            color_discrete_map={"all": "#457b9d", "connect": "#e63946", "mobile": "#4361ee"}
        )
        fig2.update_layout(height=260, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Tableau comparatif")
    key = df_results[
        (df_results["scope"] == scope) &
        (df_results["threshold"].isin([30, 60, 120, 180, 240, 360]))
    ][["threshold", "cases_solved", "pct_solved", "rentals_blocked", "pct_blocked"]].copy()
    key.columns = ["Seuil (min)", "Cas resolus", "% resolus", "Locations bloquees", "% bloquees"]
    st.dataframe(key, use_container_width=True, hide_index=True)

    st.success("Recommandation : seuil 120 minutes sur toutes les voitures - resout 67.4% des cas en bloquant seulement 3.1% des locations.")


# ══════════════════════════════════════════════════════════════════
# PAGE 4 — PREDICTION DE PRIX
# ══════════════════════════════════════════════════════════════════
elif page == "Prediction de prix":
    st.title("Prediction du prix journalier")
    st.markdown("Estimez le prix optimal grace au modele **GradientBoostingRegressor** (R2=0.756, RMSE=+-16 EUR).")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Caracteristiques")
        model_key = st.selectbox("Marque", sorted([
            "Citroen", "Renault", "Peugeot", "BMW", "Audi", "Nissan",
            "Mitsubishi", "Mercedes", "Volkswagen", "Toyota", "SEAT",
            "Subaru", "Ferrari", "Maserati", "Porsche", "Opel"
        ]))
        col_a, col_b = st.columns(2)
        with col_a:
            mileage = st.number_input("Kilometrage", 0, 500000, 50000, 5000)
        with col_b:
            engine_power = st.number_input("Puissance (ch)", 50, 500, 120, 10)
        fuel = st.selectbox("Carburant", ["diesel", "petrol", "hybrid_petrol", "electro"])
        paint_color = st.selectbox("Couleur", ["black", "white", "grey", "silver",
                                                "red", "blue", "brown", "beige",
                                                "green", "orange"])
        car_type = st.selectbox("Type", ["sedan", "suv", "estate", "hatchback",
                                          "coupe", "convertible", "van", "subcompact"])

    with col2:
        st.markdown("### Equipements")
        col_c, col_d = st.columns(2)
        with col_c:
            private_parking = st.toggle("Parking prive", value=True)
            has_gps = st.toggle("GPS", value=True)
            has_ac = st.toggle("Climatisation", value=True)
            automatic = st.toggle("Boite auto", value=False)
        with col_d:
            has_connect = st.toggle("Getaround Connect", value=True)
            speed_reg = st.toggle("Regulateur vitesse", value=False)
            winter_tires = st.toggle("Pneus hiver", value=False)

        st.markdown("---")
        st.markdown("#### Recapitulatif")
        st.markdown(f"""
- **{model_key}** - {car_type} - {fuel}
- {mileage:,} km - {engine_power} ch - {paint_color}
- GPS: {'Oui' if has_gps else 'Non'} | Clim: {'Oui' if has_ac else 'Non'} | Connect: {'Oui' if has_connect else 'Non'}
        """)

        if st.button("Predire le prix", type="primary", use_container_width=True):
            mk = "Citroën" if model_key == "Citroen" else model_key
            payload = {"input": [{
                "model_key": mk, "mileage": mileage,
                "engine_power": engine_power, "fuel": fuel,
                "paint_color": paint_color, "car_type": car_type,
                "private_parking_available": int(private_parking),
                "has_gps": int(has_gps),
                "has_air_conditioning": int(has_ac),
                "automatic_car": int(automatic),
                "has_getaround_connect": int(has_connect),
                "has_speed_regulator": int(speed_reg),
                "winter_tires": int(winter_tires)
            }]}
            try:
                resp = requests.post(
                "https://marinedde-getaround-api.hf.space/predict", json=payload, timeout=10
                )
                pred = resp.json()["prediction"][0]
                st.success(f"Prix recommande : **{pred:.0f} EUR/jour**")
                st.caption("GradientBoostingRegressor - R2=0.756 - RMSE=+-16 EUR")
            except Exception:
                st.error("API non accessible. Verifiez que FastAPI tourne sur http://127.0.0.1:8000")