import streamlit as st
import pandas as pd
import os
import datetime

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================

st.set_page_config(page_title="Control de Quinielas", layout="centered")

# Carpeta donde se guardará todo
BASE_DIR = "bases_quinielas_streamlit"
os.makedirs(BASE_DIR, exist_ok=True)

# Lista final de loterías
LOTERIAS = [
    "Primera Día", "Primera Noche",
    "La Suerte Día", "La Suerte Noche",
    "Gana Más", "Lotería Nacional",
    "Loteka", "Leidsa",
    "Loteria Real", "Florida Día",
    "Florida Noche", "New York Tarde",
    "New York Noche", "Anguilla 10:00 AM",
    "Anguilla 1:00 PM", "Anguilla 6:00 PM",
    "Anguilla 9:00 PM"
]

# ==========================
# FUNCIÓN: Archivo mensual
# ==========================

def cargar_mes_actual(loteria):
    hoy = datetime.date.today()
    nombre_archivo = f"{loteria}_{hoy.year}_{hoy.month}.xlsx"
    ruta = os.path.join(BASE_DIR, nombre_archivo)

    if os.path.exists(ruta):
        df = pd.read_excel(ruta)
    else:
        df = pd.DataFrame(columns=["fecha", "numero"])
        df.to_excel(ruta, index=False)

    return df, ruta

# ==========================
# FUNCIÓN: Guardar registro
# ==========================

def registrar_numero(loteria, numero):
    df_mes, ruta_mes = cargar_mes_actual(loteria)
    hoy = datetime.date.today()

    # Añadir registro al mes actual
    df_mes.loc[len(df_mes)] = [hoy, numero]
    df_mes.to_excel(ruta_mes, index=False)

    # Guardar también en historial general
    ruta_historial = os.path.join(BASE_DIR, "historial_quinielas.xlsx")
    if os.path.exists(ruta_historial):
        df_hist = pd.read_excel(ruta_historial)
    else:
        df_hist = pd.DataFrame(columns=["loteria", "fecha", "numero"])

    df_hist.loc[len(df_hist)] = [loteria, hoy, numero]
    df_hist.to_excel(ruta_historial, index=False)

# ==========================
# FUNCIÓN: Estado y días restantes
# ==========================

def revisar_estado_numero(df, numero):
    df_num = df[df["numero"] == numero]
    total_salidas = len(df_num)

    # Estado por cantidad
    if total_salidas == 0:
        estado = "Número Frío"
    elif total_salidas == 1:
        estado = "Número en ascenso"
    elif total_salidas == 2:
        estado = "Número Caliente"
    else:
        estado = "Número Quemado"

    # --- Cálculo días restantes ---
    dias_restantes = 0

    if total_salidas > 0:
        ultima_fecha = df_num["fecha"].max()
        hoy = datetime.date.today()
        diferencia = (hoy - ultima_fecha.date()).days

        if diferencia < 7:
            dias_restantes = 7 - diferencia
        else:
            dias_restantes = 0

    return estado, total_salidas, dias_restantes

# ==========================
# FUNCIÓN: Arrastre
# ==========================

def calcular_arrastres(numero):
    n = int(numero)
    return [(n + 25) % 100, (n + 50) % 100, (n + 75) % 100]

# ==========================
# FUNCIÓN: Reiniciar mes
# ==========================

def reiniciar_mes(loteria):
    hoy = datetime.date.today()
    archivo_nuevo = os.path.join(BASE_DIR, f"{loteria}_{hoy.year}_{hoy.month}.xlsx")
    df_vacio = pd.DataFrame(columns=["fecha", "numero"])
    df_vacio.to_excel(archivo_nuevo, index=False)

# ==========================
# INTERFAZ STREAMLIT
# ==========================

st.title("🎯 Control Inteligente de Quinielas")
st.write("Sistema profesional para análisis mensual con historial anual incluido.")

# Seleccionar lotería
loteria = st.selectbox("Seleccione la lotería", LOTERIAS)

df_mes, ruta_mes = cargar_mes_actual(loteria)

st.subheader(f"📌 Lotería actual: **{loteria}**")

# ==========================================
# PANEL: REGISTRAR QUINIELA
# ==========================================

st.header("📝 Registrar quiniela")

numero_registro = st.text_input("Ingrese un número (00-99):", max_chars=2)

if st.button("Registrar"):
    if numero_registro.isdigit() and 0 <= int(numero_registro) <= 99:
        registrar_numero(loteria, numero_registro.zfill(2))
        st.success(f"Número {numero_registro.zfill(2)} registrado correctamente.")
        st.experimental_rerun()
    else:
        st.error("Número inválido.")

# ==========================================
# PANEL: REVISAR ESTADO
# ==========================================

st.header("🔍 Revisar estado del número")

numero_revisar = st.text_input("Número a revisar (00-99):", max_chars=2)

if st.button("Revisar estado"):
    if numero_revisar.isdigit():
        numero_revisar = numero_revisar.zfill(2)
        estado, salidas, dias_restantes = revisar_estado_numero(df_mes, numero_revisar)

        mensaje = f"**{estado}** — Salidas este mes: **{salidas}**"
        if dias_restantes > 0:
            mensaje += f" — ({dias_restantes} días restantes)"

        st.info(mensaje)
    else:
        st.error("Número inválido.")

# ==========================================
# PANEL: ARRASTRES
# ==========================================

st.header("🔄 Arrastre")

numero_arrastre = st.text_input("Número base (00-99):", key="arrastre")

if st.button("Calcular arrastres"):
    if numero_arrastre.isdigit():
        n = numero_arrastre.zfill(2)
        arr = calcular_arrastres(int(n))
        arr = [str(x).zfill(2) for x in arr]
        st.success(f"Arrastres de {n}: {arr}")
    else:
        st.error("Número inválido.")

# ==========================================
# PANEL: MOSTRAR HISTORIAL
# ==========================================

st.header("📜 Historial del mes")

if st.button("Mostrar historial del mes"):
    st.dataframe(df_mes)

# ==========================================
# PANEL: REINICIAR MES
# ==========================================

st.header("🧹 Reiniciar mes (manteniendo historial anual)")

if st.button("Reiniciar mes"):
    reiniciar_mes(loteria)
    st.success("Mes reiniciado correctamente.")
    st.experimental_rerun()
