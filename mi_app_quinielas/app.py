import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Arrastre Interactivo Editable", layout="centered")
st.title("🎰 Arrastre by Esteban")

st.write("Escribe directamente el número base (00-99) y observa sus arrastres animados automáticamente.")

# HTML + CSS + JS para input estilizado y arrastres
html_code = """
<div style="text-align:center;">
    <h3>Número Base</h3>
    <input id="base" type="number" min="0" max="99" value="0" style="
        font-size:3rem;
        font-weight:bold;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color:white;
        padding:20px 30px;
        border-radius:15px;
        border:none;
        width:100px;
        text-align:center;
    ">

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
const baseInput = document.getElementById("base");
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

// Actualizar arrastres al cambiar el input
baseInput.addEventListener("input", ()=>{
    let val = parseInt(baseInput.value) || 0;
    if(val < 0) val = 0;
    if(val > 99) val = 99;
    baseInput.value = val;
    updateArrastres(val);
});
</script>
"""

components.html(html_code, height=400)









