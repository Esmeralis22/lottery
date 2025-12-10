import streamlit as st
import pandas as pd
import os
import datetime

# ==========================
# CONFIGURACIÓN
# ==========================

st.set_page_config(page_title="Control de Quinielas", layout="centered")

# Carpeta para guardar bases
BASE_DIR = "bases_quinielas_streamlit"
os.makedirs(BASE_DIR, exist_ok=True)

# Lista de todas las loterías
LOTERIAS = [
    "Primera Día", "Primera Noche",
    "La Suerte Día", "La Suerte Noche",
    "Gana Más", "Lotería Nacional",
    "Loteka", "Leidsa",
    "Loteria Real", "Florida Día",
    "Florida Noche", "New York Tarde",
    "New York Noche",
    "Anguilla 10:00 AM", "Anguilla 1:00 PM",
    "Anguilla 6:00 PM", "Anguilla 9:00 PM"
]

# ==========================
# FUNCIONES DE BASE DE DATOS
# ==========================

def cargar_mes_actual(loteria):
    """Carga o crea el archivo mensual de la lotería"""
    hoy = datetime.date.today()
    nombre_archivo = f"{loteria}_{hoy.year}_{hoy.month}.xlsx"
    ruta = os.path.join(BASE_DIR, nombre_archivo)
    if os.path.exists(ruta):
        df = pd.read_excel(ruta)
    else:
        df = pd.DataFrame(columns=["fecha", "numero"])
        df.to_excel(ruta, index=False)
    return df, ruta

def registrar_numero(loteria, numero):
    """Registra un número en la lotería del mes actual y en historial anual"""
    df_mes, ruta_mes = cargar_mes_actual(loteria)
    hoy = datetime.date.today()
    df_mes.loc[len(df_mes)] = [hoy, numero]
    df_mes.to_excel(ruta_mes, index=False)

    # Historial anual
    ruta_historial = os.path.join(BASE_DIR, "historial_quinielas.xlsx")
    if os.path.exists(ruta_historial):
        df_hist = pd.read_excel(ruta_historial)
    else:
        df_hist = pd.DataFrame(columns=["loteria", "fecha", "numero"])
    df_hist.loc[len(df_hist)] = [loteria, hoy, numero]
    df_hist.to_excel(ruta_historial, index=False)

def reiniciar_mes(loteria):
    """Reinicia el archivo del mes actual sin borrar historial anual"""
    hoy = datetime.date.today()
    ruta = os.path.join(BASE_DIR, f"{loteria}_{hoy.year}_{hoy.month}.xlsx")
    df_vacio = pd.DataFrame(columns=["fecha", "numero"])
    df_vacio.to_excel(ruta, index=False)

# ==========================
# FUNCIONES DE ESTADO
# ==========================

def revisar_estado_numero(df_mes, numero):
    """
    Devuelve el estado de un número según cantidad de salidas y días restantes.
    Reglas:
    - Max 3 veces por mes
    - Primera salida → Número en ascenso
    - 2ª → Número Caliente
    - 3ª → Número Quemado
    - Bloqueo de 7 días desde última salida
    """
    numero = numero.zfill(2)
    df_num = df_mes[df_mes["numero"] == numero]
    total_salidas = len(df_num)

    # Determinar estado textual
    if total_salidas == 0:
        estado = "Número en ascenso"  # Primera vez → en ascenso
    elif total_salidas == 1:
        estado = "Número Caliente"
    elif total_salidas == 2:
        estado = "Número Quemado"
    else:
        estado = "Número Quemado"

    # Días restantes para poder salir de nuevo
    dias_restantes = 0
    if total_salidas > 0:
        ultima_fecha = pd.to_datetime(df_num["fecha"].max()).date()
        hoy = datetime.date.today()
        diferencia = (hoy - ultima_fecha).days
        if diferencia < 7:
            dias_restantes = 7 - diferencia
        else:
            dias_restantes = 0

    return estado, total_salidas, dias_restantes

# ==========================
# FUNCIONES DE ARRASTRES
# ==========================

def calcular_arrastres(numero):
    n = int(numero)
    return [(n + 25) % 100, (n + 50) % 100, (n + 75) % 100]

# ==========================
# INTERFAZ STREAMLIT
# ==========================

st.title("🎯 Control Inteligente de Quinielas")
st.write("Sistema mensual con historial anual y días restantes según reglas de primera posición.")

# Selección de lotería
loteria = st.selectbox("Seleccione la lotería", LOTERIAS)

df_mes, ruta_mes = cargar_mes_actual(loteria)

st.subheader(f"📌 Lotería actual: {loteria}")

# ==========================
# PANEL: REGISTRAR NÚMERO
# ==========================

st.header("📝 Registrar número")

numero_registro = st.text_input("Ingrese un número (00-99):", max_chars=2, key="registro")

if st.button("Registrar número"):
    if numero_registro.isdigit() and 0 <= int(numero_registro) <= 99:
        numero_registro = numero_registro.zfill(2)
        registrar_numero(loteria, numero_registro)
        st.success(f"Número {numero_registro} registrado correctamente.")
    else:
        st.error("Número inválido.")

# ==========================
# PANEL: REVISAR ESTADO
# ==========================

st.header("🔍 Revisar estado del número")

numero_revisar = st.text_input("Número a revisar (00-99):", max_chars=2, key="revisar")

if st.button("Revisar estado"):
    if numero_revisar.isdigit() and 0 <= int(numero_revisar) <= 99:
        numero_revisar = numero_revisar.zfill(2)
        estado, salidas, dias_restantes = revisar_estado_numero(df_mes, numero_revisar)
        mensaje = f"**{estado}** — Salidas este mes: **{salidas}**"
        if dias_restantes > 0:
            mensaje += f" — ({dias_restantes} días restantes para poder salir de nuevo)"
        st.info(mensaje)
    else:
        st.error("Número inválido.")

# ==========================
# PANEL: ARRASTRES
# ==========================

st.header("🔄 Arrastre")

numero_arrastre = st.text_input("Número base (00-99):", key="arrastre")

if st.button("Calcular arrastres"):
    if numero_arrastre.isdigit() and 0 <= int(numero_arrastre) <= 99:
        n = numero_arrastre.zfill(2)
        arr = calcular_arrastres(n)
        arr = [str(x).zfill(2) for x in arr]
        st.success(f"Arrastres de {n}: {arr}")
    else:
        st.error("Número inválido.")

# ==========================
# PANEL: MOSTRAR HISTORIAL
# ==========================

st.header("📜 Historial del mes")

if st.button("Mostrar historial del mes"):
    st.dataframe(df_mes)

# ==========================
# PANEL: REINICIAR MES
# ==========================

st.header("🧹 Reiniciar mes (historial anual no se borra)")

if st.button("Reiniciar mes"):
    reiniciar_mes(loteria)
    st.success("Mes reiniciado correctamente.")


