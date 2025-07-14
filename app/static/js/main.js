import {iniciarTimer} from "./timer.js"; 

window.addEventListener("load", iniciarTimer);

function validarSenha() {
    const senha = document.getElementById("senha").value;

    const itemDigito = document.getElementById("numero");
    const itemMaiuscula = document.getElementById("maiuscula");
    const itemMinuscula = document.getElementById("minuscula");
    const itemEspecial = document.getElementById("caracterEspecial");
    const itemEspaco = document.getElementById("branco");
    const itemTamanho = document.getElementById("tamanho");

    const temDigito = /[0-9]/.test(senha);
    const temMaiuscula = /[A-Z]/.test(senha);
    const temMinuscula = /[a-z]/.test(senha);
    const temEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(senha);
    const temEspaco = /\s/.test(senha);
    const tamanhoValido = senha.length >= 8;

    atualizarItem(itemDigito, temDigito);
    atualizarItem(itemMaiuscula, temMaiuscula);
    atualizarItem(itemMinuscula, temMinuscula);
    atualizarItem(itemEspecial, temEspecial);
    atualizarItem(itemEspaco, !temEspaco);
    atualizarItem(itemTamanho, tamanhoValido);
}

function atualizarItem(elemento, condicao) {
    if (condicao) {
        elemento.textContent = "✅" + elemento.textContent.slice(2);
        elemento.classList.remove("sucesso");
    } else {
        elemento.textContent = "❌" + elemento.textContent.slice(2);
        elemento.classList.add("sucesso");
    }
}