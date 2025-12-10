import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ============================
# CONFIGURACIÓN INICIAL
# ============================

st.set_page_config(page_title="Control de Quinielas", layout="centered")

LOTERIAS = [
    "Primera Día", "Primera Noche",
    "La Suerte Día", "La Suerte Noche",
    "Gana Más", "Lotería Nacional",
    "Loteka", "Leidsa",
    "Lotería Real",
    "Florida Día", "Florida Noche",
    "New York Tarde", "New York Noche",
    "Anguilla 10:00 AM", "Anguilla 1:00 PM",
    "Anguilla 6:00 PM", "Anguilla 9:00 PM"
]

BASE_DIR = "bases_quinielas_streamlit"
os.makedirs(BASE_DIR, exist_ok=True)

HISTORIAL_GLOBAL = os.path.join(BASE_DIR, "historial_quinielas.xlsx")


# ============================
# FUNCIONES AUXILIARES
# ============================

def cargar_mes_actual(loteria):
    """Carga el archivo del mes correspondiente."""
    ahora = datetime.now()
    archivo = os.path.join(
        BASE_DIR,
        f"{loteria}_{ahora.year}_{ahora.month:02d}.xlsx"
    )

    if os.path.exists(archivo):
        return pd.read_excel(archivo), archivo
    else:
        df = pd.DataFrame(columns=["fecha", "numero"])
        df.to_excel(archivo, index=False)
        return df, archivo


def guardar_mes_actual(df, archivo):
    df.to_excel(archivo, index=False)


def registrar_historial_global(loteria, numero):
    """Guarda de forma permanente TODA la historia del año."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    if os.path.exists(HISTORIAL_GLOBAL):
        df = pd.read_excel(HISTORIAL_GLOBAL)
    else:
        df = pd.DataFrame(columns=["fecha", "loteria", "numero"])

    df.loc[len(df)] = [fecha, loteria, numero]
    df.to_excel(HISTORIAL_GLOBAL, index=False)


def estado_numero(df, numero):
    """Devuelve FRÍO / ASCENSO / CALIENTE / QUEMADO + días restantes."""
    now = datetime.now()

    df_num = df[df["numero"] == numero]

    conteo = len(df_num)

    # DÍAS RESTANTES
    if conteo > 0:
        ultima_fecha = pd.to_datetime(df_num["fecha"].iloc[-1])
        dias_pasados = (now - ultima_fecha).days
        dias_restantes = max(0, 7 - dias_pasados)
    else:
        dias_restantes = None

    # ESTADO
    if conteo == 0:
        return "Número frío", dias_restantes
    elif conteo == 1:
        return "Número en ascenso", dias_restantes
    elif conteo == 2:
        return "Número caliente", dias_restantes
    else:
        return "Número quemado", dias_restantes


def calcular_arrastre(numero):
    """Devuelve los arrastres tipo 00 → 25 → 50 → 75."""
    n = int(numero)
    arrastres = [
        f"{(n + 25) % 100:02d}",
        f"{(n + 50) % 100:02d}",
        f"{(n + 75) % 100:02d}"
    ]
    return arrastres


def reiniciar_mes(loteria):
    """Reinicia SOLO el mes actual pero deja historial global intacto."""
    ahora = datetime.now()
    archivo = os.path.join(
        BASE_DIR, f"{loteria}_{ahora.year}_{ahora.month:02d}.xlsx"
    )
    df = pd.DataFrame(columns=["fecha", "numero"])
    df.to_excel(archivo, index=False)


# ============================
# INTERFAZ STREAMLIT
# ============================

st.title("📊 Sistema Web de Quinielas por Lotería")
st.subheader("Control mensual + historial anual")

# Selección de lotería
loteria = st.selectbox("Seleccione la lotería:", LOTERIAS)

df_mes, archivo_mes = cargar_mes_actual(loteria)

st.write(f"**Archivo del mes:** `{os.path.basename(archivo_mes)}`")

st.divider()

# ============================
# REGISTRO DE QUINIELA
# ============================

st.header("🟢 Registrar quiniela")

numero_reg = st.text_input("Ingrese número (00-99):", max_chars=2)

if st.button("Registrar en primera posición"):
    if numero_reg.isdigit() and len(numero_reg) == 2:

        fecha = datetime.now().strftime("%Y-%m-%d")

        df_mes.loc[len(df_mes)] = [fecha, numero_reg]
        guardar_mes_actual(df_mes, archivo_mes)

        registrar_historial_global(loteria, numero_reg)

        st.success(f"Registrado {numero_reg} en {loteria}")

    else:
        st.error("Número inválido. Use formato 00-99")


st.divider()

# ============================
# REVISAR ESTADO DE QUINIELA
# ============================

st.header("🔍 Revisar estado del número")

numero_rev = st.text_input("Número a revisar:", max_chars=2)

if st.button("Revisar estado"):
    if numero_rev.isdigit() and len(numero_rev) == 2:
        estado, dias_rest = estado_numero(df_mes, numero_rev)

        if dias_rest is not None:
            st.info(f"📌 Estado: **{estado}** (faltan {dias_rest} días)")
        else:
            st.info(f"📌 Estado: **{estado}**")

    else:
        st.error("Número inválido")


st.divider()

# ============================
# ARRASTRES
# ============================

st.header("🎯 Calcular arrastres")

num_arr = st.text_input("Número para arrastre:", max_chars=2)

if st.button("Mostrar arrastres"):
    if num_arr.isdigit() and len(num_arr) == 2:
        arr = calcular_arrastre(num_arr)
        st.success(f"Arrastres de {num_arr}: {arr[0]}, {arr[1]}, {arr[2]}")
    else:
        st.error("Número inválido")


st.divider()

# ============================
# MOSTRAR HISTORIAL
# ============================

st.header("📜 Historial mensual de esta lotería")

if st.button("Mostrar historial mensual"):
    st.dataframe(df_mes)


# ============================
# REINICIAR MES
# ============================

st.divider()
st.header("🧹 Reiniciar mes")

if st.button("Reiniciar mes actual"):
    reiniciar_mes(loteria)
    st.success(f"Mes reiniciado para {loteria}. El historial anual se mantiene.")
