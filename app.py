import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests

# Configuración inicial de la página y estilos
st.set_page_config(
    page_title="Salud Financiera en México",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 998;
    }

    [data-testid="collapsedControl"] {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    [data-testid="collapsedControl"]::after {
        content: "Ver filtros";
        font-weight: 600;
        font-size: 15px;
        color: inherit;
    }

    .main [data-testid="block-container"] > div:first-child {
        position: sticky;
        top: 2.8rem;
        z-index: 999;
        background-color: var(--primary-background-color);
        padding-top: 1rem;
        padding-bottom: 0rem;
        border-bottom: 2px solid #ff4b4b33;
    }

    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 10px;
        background-color: transparent;
        padding: 8px 0 12px 0;
        margin-top: 4px;
        flex-wrap: wrap;
    }
    div[role="radiogroup"] > label {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        border-radius: 50px !important;
        padding: 10px 28px !important;
        color: #8899bb !important;
        border: 1.5px solid #334466 !important;
        cursor: pointer;
        transition: all 0.25s ease;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 8px #0004;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #ff4b4b88 !important;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px #ff4b4b22;
    }
    div[role="radiogroup"] > label[aria-checked="true"] {
        background: linear-gradient(135deg, #ff4b4b 0%, #cc2222 100%) !important;
        border-color: #ff4b4b !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px #ff4b4b55 !important;
        transform: translateY(-1px);
    }

    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -0.02em; }
    h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }

    .analisis-card {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        border: 1px solid #2a2a4a;
        border-left: 4px solid #ff4b4b;
        border-radius: 0 12px 12px 0;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .analisis-titulo {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #ff4b4b;
        margin-bottom: 12px;
    }
    .analisis-lista {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .analisis-lista li {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 1.0rem;
        line-height: 1.6;
        color: #dde4f0;
        padding: 6px 0;
        border-bottom: 1px solid #2a2a4a;
    }
    .analisis-lista li:last-child { border-bottom: none; }
    .analisis-lista li .icono {
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .analisis-lista li b { color: #ffffff; }

    .kpi-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
        border: 1px solid #ff4b4b44;
        border-top: 3px solid #ff4b4b;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 900;
        color: #ff4b4b;
        line-height: 1.1;
        font-family: 'Inter', sans-serif;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #8899bb;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    .kpi-delta {
        font-size: 0.85rem;
        color: #6699cc;
        margin-top: 5px;
    }

    .stButton > button { margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# Encabezado fijo y controles de navegación
top_container = st.container()

with top_container:
    st.title("Cuando el cuerpo paga las cuentas: Anatomía de la tensión financiera y la salud mental en México")
    
    st.markdown("""
        <div style="font-size: 1.05rem; color: #dde4f0; font-weight: 600; margin-top: -10px; margin-bottom: 5px;">
            Por: Josué Rico
        </div>
        <div style="font-size: 0.90rem; color: #8899bb; margin-bottom: 25px;">
            <em>* Análisis elaborado con datos de la <a href="https://www.inegi.org.mx/programas/ensafi/2023/" target="_blank" style="color: #ff4b4b; text-decoration: none; font-weight: 600;">Encuesta Nacional de Salud Financiera (ENSAFI) 2023</a>, levantada por el Instituto Nacional de Estadística y Geografía (INEGI) en colaboración con la CONDUSEF.</em>
        </div>
    """, unsafe_allow_html=True)

    paginas = [
        "1. Ingresos y Brechas",
        "2. Estrés y Geografía",
        "3. Salud Física y Supervivencia",
        "4. El Futuro y el Retiro",
    ]

    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = paginas[0]

    st.session_state.pagina_actual = st.radio(
        "Navegación", paginas,
        index=paginas.index(st.session_state.pagina_actual),
        horizontal=True, label_visibility="collapsed"
    )

# Funciones de carga y procesamiento de datos
@st.cache_data
def load_data():
    try:
        t_modulo   = pd.read_csv("TMODULO.csv",   dtype=str)
        t_sdem     = pd.read_csv("TSDEM.csv",      dtype=str)
        t_hogar    = pd.read_csv("THOGAR.csv",     dtype=str)
        t_vivienda = pd.read_csv("TVIVIENDA.csv",  dtype=str)

        for table in [t_modulo, t_sdem, t_hogar, t_vivienda]:
            table.columns = table.columns.str.strip().str.upper()

        cols_deseadas_modulo = [
            'LLAVEVIV','LLAVEHOG','N_REN','P5_19','P5_19A','P5_22',
            'P8_2_1','P8_2_2','P8_2_3','P8_2_4',
            'P8_3_01','P8_3_1','P8_3_02','P8_3_2','P8_3_04','P8_3_4',
            'P6_10_01','P6_10_1','P6_10_04','P6_10_4','P6_10_06','P6_10_6',
            'P9_3_01','P9_3_1','P9_3_02','P9_3_2','P9_3_05','P9_3_5',
        ]
        cols_finales_modulo = [c for c in cols_deseadas_modulo if c in t_modulo.columns]
        t_modulo   = t_modulo[cols_finales_modulo]
        t_sdem     = t_sdem[['LLAVEVIV','LLAVEHOG','N_REN','SEXO','EDAD']]
        t_hogar    = t_hogar[['LLAVEVIV','LLAVEHOG']]
        t_vivienda = t_vivienda[['LLAVEVIV','ENT']]

        df = pd.merge(t_modulo, t_sdem,     on=['LLAVEVIV','LLAVEHOG','N_REN'], how='left')
        df = pd.merge(df,        t_hogar,    on=['LLAVEVIV','LLAVEHOG'],          how='left')
        df = pd.merge(df,        t_vivienda, on=['LLAVEVIV'],                     how='left')
        return df
    except FileNotFoundError as e:
        st.error(f"Error: No se encontró el archivo {e.filename}.")
        return pd.DataFrame()

df_raw = load_data()
if df_raw.empty:
    st.stop()

def preprocess_data(df):
    df = df.copy()
    df['P5_19'] = pd.to_numeric(df['P5_19'], errors='coerce')
    df['P5_22'] = pd.to_numeric(df['P5_22'], errors='coerce')
    df['EDAD']  = pd.to_numeric(df['EDAD'],  errors='coerce')

    df['P5_19'] = df['P5_19'].replace([98000, 99999], np.nan)
    df['P5_22'] = df['P5_22'].replace([980000, 999888, 999999], np.nan)
    df = df.dropna(subset=['P5_19A', 'EDAD', 'SEXO'])

    emociones_map    = {'P8_2_1':'Ansiedad','P8_2_2':'Tristeza','P8_2_3':'Irritación','P8_2_4':'Frustración'}
    fisico_map       = {'P8_3_01':'Dolor de cabeza','P8_3_1':'Dolor de cabeza',
                        'P8_3_02':'Gastritis/Colitis','P8_3_2':'Gastritis/Colitis',
                        'P8_3_04':'Falta de sueño','P8_3_4':'Falta de sueño'}
    supervivencia_map= {'P6_10_01':'Pidió prestado','P6_10_1':'Pidió prestado',
                        'P6_10_04':'Vendió/Empeñó','P6_10_4':'Vendió/Empeñó',
                        'P6_10_06':'Usó Crédito','P6_10_6':'Usó Crédito'}
    retiro_map       = {'P9_3_01':'Apoyos gobierno','P9_3_1':'Apoyos gobierno',
                        'P9_3_02':'Pensión/AFORE','P9_3_2':'Pensión/AFORE',
                        'P9_3_05':'Seguirá trabajando','P9_3_5':'Seguirá trabajando'}

    for col_dict in [emociones_map, fisico_map, supervivencia_map, retiro_map]:
        for col, name in col_dict.items():
            if col in df.columns:
                df[name] = df[col].map({'1': 1, '2': 0}).fillna(0)

    def calcular_ingreso(income, frequency):
        if pd.isna(income) or pd.isna(frequency): return None
        return {'1': income*4.33,'2': income*2.16,'3': income,'4': income/12}.get(str(frequency), None)

    df['Ingreso_mensual'] = df.apply(lambda r: calcular_ingreso(r['P5_19'], r['P5_19A']), axis=1)
    df['Ingreso_mensual'] = pd.to_numeric(df['Ingreso_mensual'], errors='coerce')
    df['Brecha']  = df['P5_22'] - df['Ingreso_mensual']
    df['Genero']  = df['SEXO'].map({'1':'Hombre','2':'Mujer'})

    def clasificar_generacion(edad):
        if edad < 27:   return "Gen Z (<27)"
        elif edad <= 43: return "Millennials (28-43)"
        elif edad <= 59: return "Gen X (44-59)"
        else:            return "Boomers (60+)"
    df['Generacion'] = df['EDAD'].apply(clasificar_generacion)

    df = df.dropna(subset=['Ingreso_mensual', 'Brecha'])
    return df, list(emociones_map.values())

df_clean, lista_emociones = preprocess_data(df_raw)

# Sidebar y lógica de filtros
opciones_genero_lista     = list(df_clean['Genero'].dropna().unique())
opciones_generacion_lista = ["Gen Z (<27)","Millennials (28-43)","Gen X (44-59)","Boomers (60+)"]

if 'sel_genero'     not in st.session_state: st.session_state.sel_genero     = opciones_genero_lista[:]
if 'sel_generacion' not in st.session_state: st.session_state.sel_generacion = opciones_generacion_lista[:]

st.sidebar.header("Filtros de Análisis")
st.sidebar.markdown("Combina género y generación para personalizar la vista.")

generos = st.sidebar.multiselect(
    "Género", options=opciones_genero_lista,
    default=st.session_state.sel_genero, key="ms_genero"
)
generaciones = st.sidebar.multiselect(
    "Generación", options=opciones_generacion_lista,
    default=st.session_state.sel_generacion, key="ms_generacion"
)

st.session_state.sel_genero     = generos     if generos     else opciones_genero_lista[:]
st.session_state.sel_generacion = generaciones if generaciones else opciones_generacion_lista[:]

df_clean_filtered = df_clean.copy()
if generos:      df_clean_filtered = df_clean_filtered[df_clean_filtered['Genero'].isin(generos)]
if generaciones: df_clean_filtered = df_clean_filtered[df_clean_filtered['Generacion'].isin(generaciones)]

if df_clean_filtered.empty:
    st.error("La combinación de filtros no arroja resultados. Ajusta los filtros en la barra lateral.")
    st.stop()

# Funciones auxiliares para componentes UI y gráficas
def mejorar_fuentes(fig):
    fig.update_layout(
        font=dict(size=14, family="Inter, Arial"),
        title_font=dict(size=19, family="Inter, Arial"),
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
        hoverlabel=dict(font_size=14),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    fig.for_each_yaxis(lambda y: y.update(title_text='Número de personas') if y.title.text == 'count' else ())
    return fig

def botones_navegacion():
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    idx_actual = paginas.index(st.session_state.pagina_actual)
    with col1:
        if idx_actual > 0:
            if st.button("← Anterior", use_container_width=True):
                st.session_state.pagina_actual = paginas[idx_actual - 1]; st.rerun()
    with col3:
        if idx_actual < len(paginas) - 1:
            if st.button("Siguiente →", use_container_width=True):
                st.session_state.pagina_actual = paginas[idx_actual + 1]; st.rerun()
        else:
            if st.button("Volver al Inicio", use_container_width=True):
                st.session_state.pagina_actual = paginas[0]; st.rerun()

def _es_nan(valor):
    if valor is None:
        return True
    try:
        return np.isnan(float(valor))
    except (TypeError, ValueError):
        return True

def safe_kpi(valor_numerico, valor_formateado, label, delta=None):
    if _es_nan(valor_numerico):
        return ""
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-value">{valor_formateado}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>"""

def safe_pct(series):
    try:
        v = series.mean() * 100
        return v if not np.isnan(v) else np.nan
    except Exception:
        return np.nan

def render_kpis(kpi_list):
    validos = []
    for num, fmt, label, delta in kpi_list:
        html = safe_kpi(num, fmt, label, delta)
        if html:
            validos.append(html)
    if not validos:
        return
    cols = st.columns(len(validos))
    for col, html in zip(cols, validos):
        with col:
            st.markdown(html, unsafe_allow_html=True)

def analisis_card(titulo, puntos):
    items_html = "".join(
        f'<li><span class="icono">—</span><span>{p}</span></li>'
        for p in puntos
    )
    st.markdown(f"""
    <div class="analisis-card">
        <div class="analisis-titulo">{titulo}</div>
        <ul class="analisis-lista">{items_html}</ul>
    </div>""", unsafe_allow_html=True)

# Procesamiento de rangos e indicadores
p_low  = df_clean_filtered['Ingreso_mensual'].quantile(0.025)
p_high = df_clean_filtered['Ingreso_mensual'].quantile(0.975)
df_trimmed = df_clean_filtered[
    (df_clean_filtered['Ingreso_mensual'] >= p_low) &
    (df_clean_filtered['Ingreso_mensual'] <= p_high)
].copy()

orden_ingreso = ['$0 - $5k','>$5k - $10k','>$10k - $15k','>$15k - $20k','>$20k - $25k','> $25k']
def agrupar_ingreso(i):
    if i<=5000: return orden_ingreso[0]
    elif i<=10000: return orden_ingreso[1]
    elif i<=15000: return orden_ingreso[2]
    elif i<=20000: return orden_ingreso[3]
    elif i<=25000: return orden_ingreso[4]
    else: return orden_ingreso[5]

orden_brecha = ['< 0 (Superávit)','$0 - $5k','>$5k - $10k','>$10k - $15k','>$15k - $20k',
                '>$20k - $25k','>$25k - $30k','>$30k - $35k','> $35k']
def agrupar_brecha(b):
    if b<0:        return orden_brecha[0]
    elif b<=5000:  return orden_brecha[1]
    elif b<=10000: return orden_brecha[2]
    elif b<=15000: return orden_brecha[3]
    elif b<=20000: return orden_brecha[4]
    elif b<=25000: return orden_brecha[5]
    elif b<=30000: return orden_brecha[6]
    elif b<=35000: return orden_brecha[7]
    else:          return orden_brecha[8]

df_trimmed['Rango_Ingreso'] = df_trimmed['Ingreso_mensual'].apply(agrupar_ingreso)
df_trimmed['Rango_Brecha']  = df_trimmed['Brecha'].apply(agrupar_brecha)

mediana_hombres = df_trimmed[df_trimmed['Genero']=='Hombre']['Ingreso_mensual'].median()
mediana_mujeres = df_trimmed[df_trimmed['Genero']=='Mujer']['Ingreso_mensual'].median()
try:
    brecha_pct = ((mediana_hombres - mediana_mujeres) / mediana_hombres * 100) if mediana_hombres > 0 else np.nan
except Exception:
    brecha_pct = np.nan

pct_en_deficit = safe_pct(df_trimmed['Brecha'] > 0)
pct_ansiedad   = safe_pct(df_trimmed['Ansiedad']) if 'Ansiedad' in df_trimmed.columns else np.nan

deficit_positivo = df_trimmed[df_trimmed['Brecha'] > 0]['Brecha']
mediana_brecha = deficit_positivo.median() if not deficit_positivo.empty else np.nan

# Lógica de renderizado según la página seleccionada
if st.session_state.pagina_actual == paginas[0]:

    st.header("¿Cuánto ganamos realmente y cómo impacta el género y la edad?")
    st.markdown("---")

    delta_brecha = (f"Hombres ${mediana_hombres:,.0f} vs Mujeres ${mediana_mujeres:,.0f}"
                    if not _es_nan(mediana_hombres) and not _es_nan(mediana_mujeres) else None)
    render_kpis([
        (brecha_pct,     f"{brecha_pct:.0f}%",       "Brecha salarial de género",  delta_brecha),
        (pct_en_deficit, f"{pct_en_deficit:.0f}%",   "Hogares en déficit mensual", "Gastan más de lo que ganan"),
        (mediana_brecha, f"${mediana_brecha:,.0f}",  "Déficit mensual mediano",    "Entre quienes tienen faltante"),
        (pct_ansiedad,   f"{pct_ansiedad:.0f}%",     "Con ansiedad financiera",    "Del total encuestado"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    analisis_card("El ciclo de vida productivo roto", [
        "La <b>Generación Z</b> arranca con un ingreso de <b>$6,928 MXN</b>, el punto de entrada más bajo del mercado laboral formal.",
        "Los <b>Millennials</b> alcanzan el pico de liquidez con <b>$8,000 MXN</b>, pero es aquí donde la desigualdad entre hombres y mujeres empieza a dispararse hacia los altos ingresos.",
        "La <b>Generación X</b> enfrenta una caída adelantada en sus bolsillos: la mitad de ellos sobrevive con <b>$7,000 MXN</b> o menos, un claro síntoma de que están siendo expulsados del mercado formal.",
        "Los <b>Boomers</b> colapsan en subsistencia con <b>$5,000 MXN</b>, desmintiendo la idea de que la vejez trae acumulación.",
    ])

    analisis_card("La brecha salarial de género", [
        "Los <b>hombres</b> concentran su ingreso central en <b>$8,208 MXN</b>, con una distribución más amplia hacia ingresos altos.",
        "Las <b>mujeres</b> se agrupan abruptamente en al rededr de los <b>$6,000 MXN</b>, una brecha del <b>36%</b> respecto a los hombres.",
        "Las labores de <b>cuidado no remuneradas</b> y la precariedad laboral atrapan a las mujeres en la base de la pirámide.",
        "Esta asfixia financiera es un <b>fallo sistémico</b>, no individual: el mercado no compensa el trabajo invisible.",
    ])

    st.caption(
        "*Nota metodológica: La expectativa del crecimiento del ingreso conforme a la edad y experiencia se fundamenta "
        "empíricamente en la Teoría del Capital Humano (Becker, 1964; Mincer, 1974) y la Hipótesis del Ciclo de Vida "
        "(Modigliani, 1954).*"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    media   = df_trimmed['Ingreso_mensual'].mean()
    mediana = df_trimmed['Ingreso_mensual'].median()

    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Ingreso Promedio (Media)",    f"${media:,.0f} MXN")
    col_m2.metric("Ingreso Central (Mediana)",   f"${mediana:,.0f} MXN")

    fig1 = px.histogram(df_trimmed, x="Ingreso_mensual", nbins=50,
                        title="Distribución de Ingresos Mensuales (MXN)",
                        labels={'Ingreso_mensual': 'Ingreso Mensual (MXN)'})
    fig1.add_vline(x=media,   line_dash="dash",  line_color="red",   annotation_text="Media")
    fig1.add_vline(x=mediana, line_dash="solid", line_color="green", annotation_text="Mediana")
    fig1.update_yaxes(title_text="Número de personas")
    st.plotly_chart(mejorar_fuentes(fig1), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.violin(df_trimmed, x="Ingreso_mensual", y="Genero", color="Genero",
                         box=True, points=False,
                         title="Distribución por Género (MXN)",
                         labels={'Ingreso_mensual':'Ingreso Mensual (MXN)','Genero':'Género'})
        st.plotly_chart(mejorar_fuentes(fig2), use_container_width=True)
    with col2:
        df_altos = df_clean_filtered[df_clean_filtered['Ingreso_mensual'] > 25000]
        if not df_altos.empty:
            conteo = df_altos['Genero'].value_counts().reset_index()
            conteo.columns = ['Genero','Cantidad']
            fig3 = px.bar(conteo, x='Genero', y='Cantidad', text='Cantidad', color='Genero',
                          title="Personas con ingresos > $25k MXN",
                          labels={'Cantidad':'Número de personas','Genero':'Género'})
            fig3.update_traces(textposition='outside')
            st.plotly_chart(mejorar_fuentes(fig3), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.header("¿El salario alcanza o vivimos en déficit crónico?")

    analisis_card("Déficit crónico: la norma, no la excepción", [
        "La distribución de la brecha se concentra masivamente <b>a la derecha del punto de equilibrio</b>: más necesidades que ingresos.",
        "Este déficit <b>detona en la etapa Millennial</b> cuando llegan hipotecas, hijos y deudas y no se recupera en etapas posteriores.",
        "La capacidad de generar ahorro o construir patrimonio queda <b>prácticamente nula</b> para la mayoría de la población.",
        "El salario formal dejó de ser garantía de solvencia: es una <b>herramienta para administrar faltantes</b>, no para prosperar.",
    ])

    b_low  = df_trimmed['Brecha'].quantile(0.05)
    b_high = df_trimmed['Brecha'].quantile(0.95)
    df_brecha_visual = df_trimmed[(df_trimmed['Brecha'] >= b_low) & (df_trimmed['Brecha'] <= b_high)]

    fig4 = px.histogram(df_brecha_visual, x="Brecha", nbins=50,
                        color_discrete_sequence=[px.colors.qualitative.Plotly[0]],
                        title="Brecha: Déficit (-) vs Superávit (+) (MXN)",
                        labels={'Brecha':'Déficit (-) / Superávit (+)'})
    fig4.add_vline(x=0, line_color="white", line_dash="dash", annotation_text="Equilibrio")
    fig4.update_yaxes(title_text="Número de personas")
    st.plotly_chart(mejorar_fuentes(fig4), use_container_width=True)

    botones_navegacion()


elif st.session_state.pagina_actual == paginas[1]:

    st.header("¿Es el estrés financiero una crisis de alcance nacional?")

    pct_tristeza    = safe_pct(df_trimmed['Tristeza'])    if 'Tristeza'    in df_trimmed.columns else np.nan
    pct_frustracion = safe_pct(df_trimmed['Frustración']) if 'Frustración' in df_trimmed.columns else np.nan
    render_kpis([
        (pct_ansiedad,    f"{pct_ansiedad:.0f}%",    "Población con ansiedad financiera", "Del total encuestado"),
        (pct_tristeza,    f"{pct_tristeza:.0f}%",    "Reporta tristeza por dinero",        "Del total encuestado"),
        (pct_frustracion, f"{pct_frustracion:.0f}%", "Experimenta frustración",             "Del total encuestado"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    analisis_card("Una crisis que no respeta fronteras estatales", [
        "En <b>múltiples estados</b> del país, casi la mitad de la población vive con <b>ansiedad constante</b> por el dinero.",
        "El estrés financiero <b>no es regional ni aislado</b>: es una crisis sistémica que atraviesa todo el territorio nacional.",
        "La falta de liquidez está mermando <b>silenciosamente la salud mental</b> y el bienestar de los hogares mexicanos.",
    ])

    dic_estados = {
        '01':'Aguascalientes','02':'Baja California','03':'Baja California Sur','04':'Campeche',
        '05':'Coahuila de Zaragoza','06':'Colima','07':'Chiapas','08':'Chihuahua','09':'Distrito Federal',
        '10':'Durango','11':'Guanajuato','12':'Guerrero','13':'Hidalgo','14':'Jalisco',
        '15':'México','16':'Michoacán de Ocampo','17':'Morelos','18':'Nayarit','19':'Nuevo León',
        '20':'Oaxaca','21':'Puebla','22':'Querétaro','23':'Quintana Roo','24':'San Luis Potosí',
        '25':'Sinaloa','26':'Sonora','27':'Tabasco','28':'Tamaulipas','29':'Tlaxcala',
        '30':'Veracruz de Ignacio de la Llave','31':'Yucatán','32':'Zacatecas',
    }

    if 'ENT' in df_trimmed.columns and 'Ansiedad' in df_trimmed.columns:
        df_mapa = df_trimmed.copy()
        df_mapa['ENT'] = df_mapa['ENT'].astype(str).str.zfill(2)
        df_mapa['Nombre_Estado'] = df_mapa['ENT'].map(dic_estados)
        ansiedad_estado = df_mapa.groupby('Nombre_Estado')['Ansiedad'].mean().reset_index()
        ansiedad_estado['Ansiedad'] *= 100
        try:
            url_geojson = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
            mx_geojson  = requests.get(url_geojson, timeout=10).json()
            fig_mapa = px.choropleth(
                ansiedad_estado, geojson=mx_geojson, locations='Nombre_Estado',
                featureidkey='properties.name', color='Ansiedad',
                color_continuous_scale="Reds",
                title="Ansiedad Financiera por Estado (%)"
            )
            fig_mapa.update_geos(fitbounds="locations", visible=False)
            fig_mapa.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(mejorar_fuentes(fig_mapa), use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo cargar el mapa: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.header("¿Cómo se traduce la falta de dinero en crisis psicológica?")

    analisis_card("El déficit como generador de angustia", [
        "En el estrato de subsistencia (<b>$0–$5,000 MXN</b>), más de la mitad de la población reporta <b>ansiedad y tristeza crónica</b>.",
        "El detonante no es solo el bajo salario, sino la <b>magnitud del faltante mensual</b>: a mayor déficit, mayor colapso emocional.",
        "Las <b>mujeres</b> somatizan una carga de angustia significativamente mayor ante las mismas carencias económicas.",
        "Los <b>Millennials</b> son la generación más asfixiada: sus picos de ansiedad <b>superan el 80%</b> ante desfases severos.",
        "El estrés financiero <b>no es una preocupación pasajera</b>: es un fallo estructural que erosiona la salud mental de la fuerza laboral.",
    ])

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        tabla_ingreso = (df_trimmed.groupby('Rango_Ingreso')[lista_emociones]
                         .mean().reindex(orden_ingreso).dropna(how='all') * 100)
        fig_h1 = px.imshow(tabla_ingreso, color_continuous_scale="Reds", aspect="auto",
                           title="Estrés por Nivel de Ingreso (%)")
        fig_h1.update_traces(texttemplate="%{z:.1f}%", textfont_size=13)
        st.plotly_chart(mejorar_fuentes(fig_h1), use_container_width=True)
    with col_h2:
        tabla_brecha = (df_trimmed.groupby('Rango_Brecha')[lista_emociones]
                        .mean().reindex(orden_brecha).dropna(how='all') * 100)
        fig_h2 = px.imshow(tabla_brecha, color_continuous_scale="Reds", aspect="auto",
                           title="Estrés por Magnitud de Déficit (%)")
        fig_h2.update_traces(texttemplate="%{z:.1f}%", textfont_size=13)
        st.plotly_chart(mejorar_fuentes(fig_h2), use_container_width=True)

    botones_navegacion()


elif st.session_state.pagina_actual == paginas[2]:

    st.header("¿Hasta qué punto la asfixia económica nos enferma físicamente?")

    cols_fisicas = ['Dolor de cabeza','Gastritis/Colitis','Falta de sueño']
    render_kpis([
        (safe_pct(df_trimmed[c]) if c in df_trimmed.columns else np.nan,
         f"{safe_pct(df_trimmed[c]):.0f}%" if c in df_trimmed.columns else "",
         c, "Del total encuestado")
        for c in cols_fisicas
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    analisis_card("El cuerpo paga la deuda que no se puede saldar", [
        "A medida que el déficit mensual se agudiza, el <b>insomnio crónico</b> escala de forma alarmante, privando al cuerpo de su capacidad de recuperación.",
        "La <b>gastritis y colitis</b> se disparan en los estratos de mayor escasez, evidenciando que el organismo absorbe materialmente el impacto de las deudas.",
        "Las <b>migrañas y dolores de cabeza</b> acompañan a los niveles más altos de estrés financiero, cerrando el círculo psicosomático.",
        "Las <b>mujeres</b> reportan una prevalencia de síntomas físicos drásticamente superior ante los mismos niveles de insolvencia que los hombres.",
        "<b>Millennials y Gen X</b> en su apogeo productivo y con mayores cargas familiares exhiben los picos críticos más altos de deterioro físico.",
    ])

    cols_fisicas_presentes = [c for c in cols_fisicas if c in df_trimmed.columns]
    if cols_fisicas_presentes:
        df_sint = (df_trimmed.groupby('Rango_Brecha')[cols_fisicas_presentes]
                   .mean().reindex(orden_brecha).dropna(how='all').reset_index())
        for c in cols_fisicas_presentes: df_sint[c] *= 100
        fig_sint = px.line(df_sint, x='Rango_Brecha', y=cols_fisicas_presentes, markers=True,
                           title="Síntomas Físicos según Déficit Mensual",
                           labels={'value':'Porcentaje (%)','Rango_Brecha':'Déficit Mensual','variable':'Síntoma'})
        st.plotly_chart(mejorar_fuentes(fig_sint), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.header("¿A qué recurrimos cuando el dinero ya no alcanza?")

    cols_sup = ['Pidió prestado','Vendió/Empeñó','Usó Crédito']
    render_kpis([
        (safe_pct(df_clean_filtered[c]) if c in df_clean_filtered.columns else np.nan,
         f"{safe_pct(df_clean_filtered[c]):.0f}%" if c in df_clean_filtered.columns else "",
         c, "Del total encuestado")
        for c in cols_sup
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    analisis_card("Estrategias de supervivencia: lo informal antes que lo formal", [
        "<b>Pedir prestado</b> a familia o conocidos es la estrategia dominante, superando casi por cuatro veces al crédito bancario.",
        "Vender o empeñar activos es el <b>segundo recurso más común</b>, revelando el alto costo patrimonial de la escasez de liquidez.",
        "El <b>crédito formal</b> tarjetas, préstamos bancarios es el menos utilizado, evidenciando exclusión o desconfianza del sistema financiero.",
        "Esta constante se mantiene <b>sin importar la edad ni el género</b>: la red informal es el verdadero amortiguador económico de los hogares mexicanos.",
    ])

    cols_sup_presentes = [c for c in cols_sup if c in df_clean_filtered.columns]
    if cols_sup_presentes:
        df_sup_plot = df_clean_filtered[cols_sup_presentes].mean().reset_index()
        df_sup_plot.columns = ['Estrategia','Porcentaje']
        df_sup_plot['Porcentaje'] *= 100
        fig_sup = px.bar(df_sup_plot, x='Estrategia', y='Porcentaje', text_auto='.1f',
                         color='Estrategia',
                         color_discrete_sequence=['#ff4b4b', '#3366cc', '#8899bb'],
                         title="Medios utilizados frente a la falta de liquidez",
                         labels={'Estrategia':'Estrategia utilizada','Porcentaje':'Población (%)'})
        fig_sup.update_traces(textposition='outside')
        st.plotly_chart(mejorar_fuentes(fig_sup), use_container_width=True)

    botones_navegacion()


elif st.session_state.pagina_actual == paginas[3]:

    st.header("¿Es el retiro una etapa de descanso o una obligación de seguir trabajando?")

    cols_ret = ['Seguirá trabajando','Pensión/AFORE','Apoyos gobierno']
    render_kpis([
        (safe_pct(df_clean_filtered[c]) if c in df_clean_filtered.columns else np.nan,
         f"{safe_pct(df_clean_filtered[c]):.0f}%" if c in df_clean_filtered.columns else "",
         c, "Del total encuestado")
        for c in cols_ret
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    analisis_card("El retiro que nunca llega", [
        "La necesidad de <b>seguir trabajando</b> domina las proyecciones de retiro en todas las cohortes, con niveles cercanos o superiores al <b>70%</b>.",
        "Los <b>hombres</b> reportan mayor expectativa de acceso a <b>Pensión o AFORE</b>, reflejo de trayectorias laborales con más formalidad.",
        "Las <b>mujeres</b> muestran un respaldo institucional significativamente menor: son excluidas del sistema de ahorro formal en todas las etapas de vida.",
        "Ante esa exclusión, las mujeres dependen más de los <b>apoyos gubernamentales</b> como su única red de seguridad para la vejez.",
        "Esta fractura no es accidental: es la <b>factura final de décadas</b> de brecha salarial, informalidad y trabajo de cuidados no remunerado.",
    ])

    cols_retiro_presentes = [c for c in cols_ret if c in df_clean_filtered.columns]
    if cols_retiro_presentes:
        orden_gen = ["Gen Z (<27)","Millennials (28-43)","Gen X (44-59)","Boomers (60+)"]
        df_ret = df_clean_filtered.groupby('Generacion')[cols_retiro_presentes].mean().reindex(orden_gen).dropna(how='all').reset_index()
        df_ret_melt = df_ret.melt(id_vars='Generacion', var_name='Fuente de Ingreso', value_name='Porcentaje')
        df_ret_melt['Porcentaje'] *= 100
        fig_ret = px.bar(df_ret_melt, x='Generacion', y='Porcentaje', color='Fuente de Ingreso',
                         barmode='group', text_auto='.1f',
                         color_discrete_sequence=['#ff4b4b', '#3366cc', '#8899bb'],
                         title="Comparativa Generacional de Fuentes de Retiro",
                         labels={'Generacion':'Generación','Porcentaje':'Porcentaje (%)'})
        fig_ret.update_traces(textposition='outside')
        st.plotly_chart(mejorar_fuentes(fig_ret), use_container_width=True)

    botones_navegacion()