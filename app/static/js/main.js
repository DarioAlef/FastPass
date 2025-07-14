import {iniciarTimer} from "./timer.js"; 

let usuarioAtual = null;
let tempoInicio = null;

window.addEventListener("load", async () => {
    await verificarUsuario();
    
    if (usuarioAtual) {
        mostrarJogo();
    } else {
        mostrarModalCadastro();
    }
});

async function verificarUsuario() {
    const emailSalvo = localStorage.getItem('userEmail');
    if (emailSalvo) {
        try {
            const response = await fetch(`/user/${emailSalvo}`);
            if (response.ok) {
                usuarioAtual = await response.json();
                return true;
            }
        } catch (error) {
            console.error('Erro ao verificar usuário:', error);
        }
    }
    return false;
}

function mostrarModalCadastro() {
    document.getElementById('modalCadastro').style.display = 'block';
    document.getElementById('conteudoPrincipal').style.display = 'none';
    
    document.getElementById('formCadastro').addEventListener('submit', async (e) => {
        e.preventDefault();
        await cadastrarUsuario();
    });
}

async function cadastrarUsuario() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome, email })
        });
        
        if (response.ok) {
            const result = await response.json();
            usuarioAtual = { id: result.id, nome: result.nome, email };
            localStorage.setItem('userEmail', email);
            mostrarJogo();
        } else {
            const error = await response.json();
            alert(error.detail || 'Erro ao cadastrar');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
    }
}

function mostrarJogo() {
    document.getElementById('modalCadastro').style.display = 'none';
    document.getElementById('conteudoPrincipal').style.display = 'block';
    document.getElementById('nomeUsuario').textContent = usuarioAtual.nome;
    
    // Configura o botão de ranking
    document.getElementById('btnRanking').addEventListener('click', mostrarRanking);
    
    tempoInicio = Date.now();
    iniciarTimer();
    document.getElementById("button").addEventListener("click", validarSenha);
}

async function mostrarRanking() {
    const modal = document.getElementById('modalRanking');
    const container = document.getElementById('rankingContainer');
    
    modal.style.display = 'block';
    container.innerHTML = '<div class="loading">Carregando ranking...</div>';
    
    try {
        const response = await fetch('/senha/ranking');
        if (response.ok) {
            const data = await response.json();
            exibirRanking(data.ranking);
        } else {
            container.innerHTML = '<div class="no-data">Erro ao carregar ranking</div>';
        }
    } catch (error) {
        console.error('Erro ao carregar ranking:', error);
        container.innerHTML = '<div class="no-data">Erro ao conectar com o servidor</div>';
    }
}

function exibirRanking(ranking) {
    const container = document.getElementById('rankingContainer');
    
    if (ranking.length === 0) {
        container.innerHTML = '<div class="no-data">Nenhum dado disponível ainda</div>';
        return;
    }
    
    let html = '';
    ranking.forEach((item, index) => {
        const positionIcon = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : item.posicao;
        const topClass = index < 3 ? 'top-3' : '';
        
        html += `
            <div class="ranking-item ${topClass}">
                <div class="ranking-position">${positionIcon}</div>
                <div class="ranking-info">
                    <div class="ranking-nome">${item.nome}</div>
                    <div class="ranking-email">${item.email}</div>
                </div>
                <div class="ranking-stats">
                    <div class="ranking-tempo">${item.melhor_tempo}s</div>
                    <div class="ranking-total">${item.total_senhas} senha(s)</div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function fecharModalRanking() {
    document.getElementById('modalRanking').style.display = 'none';
}

// Fecha o modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modalRanking');
    if (event.target === modal) {
        fecharModalRanking();
    }
}

async function validarSenha() {
    const senha = document.getElementById("senha").value;

    const itemDigito = document.getElementById("numero");
    const itemMaiuscula = document.getElementById("maiuscula");
    const itemMinuscula = document.getElementById("minuscula");
    const itemEspecial = document.getElementById("caracterEspecial");
    const itemEspaco = document.getElementById("branco");
    const itemTamanho = document.getElementById("tamanho");
    const itemRepetido = document.getElementById("repetido");

    const temDigito = /[0-9]/.test(senha);
    const temMaiuscula = /[A-Z]/.test(senha);
    const temMinuscula = /[a-z]/.test(senha);
    const temEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(senha);
    const temEspaco = /\s/.test(senha);
    const tamanhoValido = senha.length >= 8 && senha.length <= 12;
    const semRepetido = !/(.)\1/.test(senha);

    atualizarItem(itemDigito, temDigito);
    atualizarItem(itemMaiuscula, temMaiuscula);
    atualizarItem(itemMinuscula, temMinuscula);
    atualizarItem(itemEspecial, temEspecial);
    atualizarItem(itemEspaco, !temEspaco);
    atualizarItem(itemTamanho, tamanhoValido);
    atualizarItem(itemRepetido, semRepetido);

    const senhaValida = temDigito && temMaiuscula && temMinuscula && 
                       temEspecial && !temEspaco && tamanhoValido && semRepetido;

    if (senhaValida) {
        const tempoFinal = Date.now();
        const tempoCompletado = Math.round((tempoFinal - tempoInicio) / 1000);
        
        await salvarSenhaValida(senha, tempoCompletado);
    }
}

async function salvarSenhaValida(senha, tempoCompletado) {
    try {
        const response = await fetch('/senha/salvar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                senha: senha,
                tempo_completado: tempoCompletado,
                user_id: usuarioAtual.id
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            alert(`🎉 Parabéns! Senha válida criada em ${tempoCompletado} segundos!`);
            
            await mostrarEstatisticas();
        } else {
            console.error('Erro ao salvar senha');
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}

async function mostrarEstatisticas() {
    try {
        const response = await fetch(`/senha/melhor-tempo/${usuarioAtual.id}`);
        if (response.ok) {
            const result = await response.json();
            console.log(`Seu melhor tempo: ${result.melhor_tempo} segundos`);
        }
    } catch (error) {
        console.error('Erro ao obter estatísticas:', error);
    }
}

function atualizarItem(elemento, condicao) {
    if (condicao) {
        elemento.textContent = "✅" + elemento.textContent.slice(2);
        elemento.classList.add("sucesso");
    } else {
        elemento.textContent = "❌" + elemento.textContent.slice(2);
        elemento.classList.remove("sucesso");
    }
}