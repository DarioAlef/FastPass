let duracao = 30;


export function iniciarTimer() {
    const display = document.getElementById("tempo");
    const campoSenha = document.getElementById("senha");
    const botao = document.getElementById("button");

    display.textContent = formatarTempo(duracao)

    const intervalo = setInterval(() => {
        duracao--;

        if (duracao <= 0) {
            clearInterval(intervalo);
            display.textContent = "00:00";
            campoSenha.disable = true;
            botao.disabled = true;
            alert("⏰ Tempo esgotado! A sessão terminou");
        }
    }, 1000);
}


function formatarTempo(segundos) {
  const min = String(Math.floor(segundos / 60)).padStart(2, "0");
  const seg = String(segundos % 60).padStart(2, "0");
  return `${min}:${seg}`;
}
