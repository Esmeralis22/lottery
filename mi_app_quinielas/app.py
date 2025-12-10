import streamlit as st

st.set_page_config(page_title="Arrastre Animado", layout="centered")
st.title("🎯 Arrastre Interactivo con Animaciones")

st.write("Ingresa un número del 00 al 99 y observa sus arrastres aparecer con animaciones.")

# Entrada del usuario
numero_base = st.number_input("Número base (00-99):", min_value=0, max_value=99, step=1)

if st.button("Calcular arrastres"):
    n = int(numero_base)
    arrastres = [(n + 25) % 100, (n + 50) % 100, (n + 75) % 100]
    arrastres = [str(x).zfill(2) for x in arrastres]

    # Generar HTML con animaciones
    html_content = """
    <style>
    .arrastre-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-top: 20px;
    }
    .arrastre {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        padding: 15px 25px;
        border-radius: 15px;
        opacity: 0;
        transform: translateY(-20px);
        animation: fadeBounce 0.6s forwards;
    }
    @keyframes fadeBounce {
        0% { opacity: 0; transform: translateY(-20px);}
        50% { opacity: 1; transform: translateY(10px);}
        100% { opacity: 1; transform: translateY(0);}
    }
    </style>
    <div class="arrastre-container">
    """

    delay = 0
    for num in arrastres:
        html_content += f'<div class="arrastre" style="animation-delay: {delay}s">{num}</div>'
        delay += 0.2  # retraso entre números

    html_content += "</div>"

    st.markdown(html_content, unsafe_allow_html=True)







