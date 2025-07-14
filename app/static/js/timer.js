function formatarTempo(segundos) {
  const min = String(Math.floor(segundos / 60)).padStart(2, "0");
  const seg = String(segundos % 60).padStart(2, "0");
  return `${min}:${seg}`;
}

export function iniciarTimer() {
    let duracao = 30; // Movido para dentro da função para reinicializar sempre
    const display = document.getElementById("tempo");
    const campoSenha = document.getElementById("senha");
    const botao = document.getElementById("button");

    // Atualiza o display inicial
    display.textContent = formatarTempo(duracao);

    const intervalo = setInterval(() => {
        duracao--;
        
        // Atualiza o display a cada segundo
        display.textContent = formatarTempo(duracao);
        
        // Muda a cor quando resta pouco tempo
        if (duracao <= 10) {
            display.parentElement.classList.add("timer-critico");
        }
        
        if (duracao <= 0) {
            clearInterval(intervalo);
            display.textContent = "00:00";
            campoSenha.disabled = true;
            botao.disabled = true;
            alert("⏰ Tempo esgotado! A sessão terminou");
        }
    }, 1000);
    
    // Retorna o intervalo para poder cancelar se necessário
    return intervalo;
}