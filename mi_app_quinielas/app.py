import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Arrastre Interactivo Live", layout="centered")
st.title("🎰 Arrastre Slot Machine Interactivo")

st.write("Usa las flechas arriba/abajo para cambiar el número base y ver sus arrastres animados al instante.")

# HTML + CSS + JS para número base editable y arrastres animados
html_code = """
<div style="text-align:center;">
    <h3>Número Base</h3>
    <div id="base" tabindex="0" style="
        display:inline-block;
        font-size:3rem;
        font-weight:bold;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color:white;
        padding:20px 30px;
        border-radius:15px;
        cursor:pointer;
        user-select:none;
    ">00</div>

    <h3 style="margin-top:30px;">Arrastres</h3>
    <div id="arrastres" style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap;"></div>
</div>

<style>
@keyframes fadeBounce {
    0% { opacity: 0; transform: translateY(-20px);}
    50% { opacity: 1; transform: translateY(10px);}
    100% { opacity: 1; transform: translateY(0);}
}
.arrastre {
    font-size: 2.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    color: white;
    padding: 15px 25px;
    border-radius: 15px;
    opacity: 0;
    transform: translateY(-20px);
    animation: fadeBounce 0.6s forwards;
}
</style>

<script>
const baseDiv = document.getElementById("base");
const arrDiv = document.getElementById("arrastres");

function updateArrastres(n){
    arrDiv.innerHTML = "";
    let offsets = [25,50,75];
    offsets.forEach((o,i)=>{
        let num = (parseInt(n) + o) % 100;
        let span = document.createElement("div");
        span.className = "arrastre";
        span.style.animationDelay = (i*0.2)+"s";
        span.innerText = num.toString().padStart(2,"0");
        arrDiv.appendChild(span);
    });
}

// Inicializar arrastres
updateArrastres(0);

// Manejo de teclas
baseDiv.addEventListener("keydown", (e)=>{
    let val = parseInt(baseDiv.innerText);
    if(e.key === "ArrowUp") val = (val + 1) % 100;
    if(e.key === "ArrowDown") val = (val - 1 + 100) % 100;
    baseDiv.innerText = val.toString().padStart(2,"0");
    updateArrastres(val);
});

// Manejo de click para seleccionar y poder usar flechas
baseDiv.addEventListener("click", ()=>{ baseDiv.focus(); });
</script>
"""

components.html(html_code, height=400)








