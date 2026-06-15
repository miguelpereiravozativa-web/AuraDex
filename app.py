# app.py
import streamlit as st
import time
import random
import plotly.graph_objects as go
import urllib.parse

# Configurações Iniciais
st.set_page_config(
    page_title="AuraDex | Teste de Aura",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Variáveis de Monetização
MERCADO_PAGO_URL = "https://www.mercadopago.com.br/checkout/v1/payment/redirect/96a53283-cdf7-4a89-86e7-61a34a30ca24/payment-option-form/?source=link&preference-id=174157336-6d7ca9a8-aa35-47b8-83f3-952643d015f4&router-request-id=a7047bbd-779a-4a86-a7c2-ba381b7bb692&p=6e8c9c12e0da30523a2c349449d161bd"
PRECO_PREMIUM = 1.99
BASE_URL = "https://auradex.streamlit.app" # Altere para o seu link final

# Estilos CSS Personalizados
st.markdown("""
<style>
    /* Tema Escuro e Cartões */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #A0AAB2;
        margin-bottom: 40px;
    }
    .card {
        background-color: #1A1C23;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid #2D303E;
    }
    .premium-lock {
        background: linear-gradient(135deg, #1A1C23 0%, #2A2135 100%);
        border: 1px solid #FFD700;
        text-align: center;
    }
    .btn-pay {
        background: linear-gradient(90deg, #009EE3, #00C6FF);
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 15px;
    }
    .final-card {
        background: linear-gradient(180deg, #2b2e4a 0%, #1a1c29 100%);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
    }
    .final-card h2 { margin: 0; color: #FFD700; }
    .final-card p { margin: 5px 0; color: #E0E0E0; }
    .rank-text {
        font-size: 4rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

# Tipos de Aura
TIPOS_AURA = [
    "Reforço", "Emissão", "Manipulação", 
    "Materialização", "Transmutação", "Especialização"
]

# Banco de Perguntas (15 Perguntas focadas nas métricas solicitadas)
PERGUNTAS = [
    {
        "texto": "1. Como você atua em uma crise ou perigo iminente?",
        "opcoes": [
            ("Enfrento de frente, usando força e coragem.", "Reforço"),
            ("Analiso a situação de longe e ataco estrategicamente.", "Emissão"),
            ("Mantenho a calma e organizo os outros ao meu redor.", "Manipulação"),
            ("Crio uma ferramenta ou solução prática na hora.", "Materialização"),
            ("Me adapto rapidamente e engano o inimigo.", "Transmutação"),
            ("Sigo minha intuição, algo me diz o que fazer.", "Especialização")
        ]
    },
    {
        "texto": "2. Qual característica mais se destaca em você?",
        "opcoes": [
            ("Persistência inabalável", "Reforço"),
            ("Independência forte", "Emissão"),
            ("Liderança e controle", "Manipulação"),
            ("Disciplina rigorosa", "Materialização"),
            ("Criatividade e imprevisibilidade", "Transmutação"),
            ("Inteligência e visão única", "Especialização")
        ]
    },
    {
        "texto": "3. Como você prefere resolver um conflito com alguém?",
        "opcoes": [
            ("Sendo direto e honesto, mesmo que doa.", "Reforço"),
            ("Mando uma mensagem clara e me afasto para esfriar.", "Emissão"),
            ("Converso para trazer a pessoa para o meu lado.", "Manipulação"),
            ("Estabeleço regras e limites claros.", "Materialização"),
            ("Mudo de assunto até o clima melhorar.", "Transmutação"),
            ("Percebo as emoções ocultas e resolvo a raiz do problema.", "Especialização")
        ]
    },
    {
        "texto": "4. O que é mais importante em um plano?",
        "opcoes": [
            ("Ação imediata", "Reforço"),
            ("Alcance e impacto", "Emissão"),
            ("Controle das variáveis", "Manipulação"),
            ("Estrutura e detalhes", "Materialização"),
            ("Planos B, C e D", "Transmutação"),
            ("O propósito maior", "Especialização")
        ]
    },
    {
        "texto": "5. Quando você sente uma forte emoção, você:",
        "opcoes": [
            ("Deixa transparecer na hora.", "Reforço"),
            ("A projeta nas suas ações e trabalho.", "Emissão"),
            ("Usa para influenciar os outros.", "Manipulação"),
            ("Foca em um hobby ou objeto para se acalmar.", "Materialização"),
            ("Muda de humor rapidamente.", "Transmutação"),
            ("A emoção me dá insights e revelações.", "Especialização")
        ]
    },
    {
        "texto": "6. Seu maior defeito geralmente é ser:",
        "opcoes": [
            ("Teimoso e impaciente", "Reforço"),
            ("Impulsivo e volátil", "Emissão"),
            ("Controlador e argumentativo", "Manipulação"),
            ("Nervoso e muito detalhista", "Materialização"),
            ("Inconstante e mentiroso", "Transmutação"),
            ("Incompreendido e isolado", "Especialização")
        ]
    },
    {
        "texto": "7. Como você aprende uma nova habilidade?",
        "opcoes": [
            ("Repetição até a exaustão física/mental.", "Reforço"),
            ("Testando os limites do que consigo fazer.", "Emissão"),
            ("Estudando a teoria e depois aplicando nos outros.", "Manipulação"),
            ("Focando intensamente em um único aspecto por vez.", "Materialização"),
            ("Misturando com algo que já sei para criar algo novo.", "Transmutação"),
            ("Apenas 'pego' o jeito de forma não convencional.", "Especialização")
        ]
    },
    {
        "texto": "8. Em um grupo, seu papel é:",
        "opcoes": [
            ("O tanque / linha de frente", "Reforço"),
            ("O suporte de longa distância", "Emissão"),
            ("O líder / estrategista", "Manipulação"),
            ("O especialista técnico", "Materialização"),
            ("O curinga / improvisador", "Transmutação"),
            ("O conselheiro sábio", "Especialização")
        ]
    },
    {
        "texto": "9. Você valoriza mais pessoas que são:",
        "opcoes": [
            ("Leais e sinceras", "Reforço"),
            ("Livres e dinâmicas", "Emissão"),
            ("Úteis e organizadas", "Manipulação"),
            ("Precisas e confiáveis", "Materialização"),
            ("Divertidas e astutas", "Transmutação"),
            ("Profundas e autênticas", "Especialização")
        ]
    },
    {
        "texto": "10. Qual ambiente você prefere?",
        "opcoes": [
            ("Ao ar livre, natureza, academia.", "Reforço"),
            ("Locais amplos com boa visão.", "Emissão"),
            ("Meu escritório ou ambiente que controlo.", "Manipulação"),
            ("Laboratório, oficina ou ateliê.", "Materialização"),
            ("Cidades agitadas, festas, mudança de cenário.", "Transmutação"),
            ("Bibliotecas antigas, templos, locais isolados.", "Especialização")
        ]
    },
    {
        "texto": "11. Como você lida com regras?",
        "opcoes": [
            ("Sigo se fizerem sentido para mim.", "Reforço"),
            ("Tendo a ignorá-las se me atrapalham.", "Emissão"),
            ("Uso as regras a meu favor.", "Manipulação"),
            ("Sigo estritamente para manter a ordem.", "Materialização"),
            ("Encontro as brechas nelas.", "Transmutação"),
            ("Crio as minhas próprias.", "Especialização")
        ]
    },
    {
        "texto": "12. O que mais te assusta?",
        "opcoes": [
            ("Ser fraco ou inútil", "Reforço"),
            ("Ficar preso ou contido", "Emissão"),
            ("Perder o controle da situação", "Manipulação"),
            ("O caos absoluto e a falha de planejamento", "Materialização"),
            ("O tédio e a rotina infinita", "Transmutação"),
            ("Perder quem eu sou", "Especialização")
        ]
    },
    {
        "texto": "13. Como você gasta seu dinheiro livre?",
        "opcoes": [
            ("Comida, experiências físicas, treinos.", "Reforço"),
            ("Viagens e locomoção.", "Emissão"),
            ("Investimentos ou coisas que geram status.", "Manipulação"),
            ("Colecionáveis, equipamentos e itens físicos de valor.", "Materialização"),
            ("Apostas, jogos, surpresas, coisas inusitadas.", "Transmutação"),
            ("Doações, conhecimentos raros, antiguidades.", "Especialização")
        ]
    },
    {
        "texto": "14. Diante de um desafio impossível, você:",
        "opcoes": [
            ("Tenta até quebrar a parede.", "Reforço"),
            ("Atira tudo que tem antes de recuar.", "Emissão"),
            ("Procura aliados para dividir o fardo.", "Manipulação"),
            ("Constrói a ferramenta perfeita para a situação.", "Materialização"),
            ("Faz o impossível parecer possível com um truque.", "Transmutação"),
            ("Encontra uma saída que ninguém mais viu.", "Especialização")
        ]
    },
    {
        "texto": "15. Se você pudesse ter um superpoder básico, seria:",
        "opcoes": [
            ("Super força/regeneração", "Reforço"),
            ("Disparar energia/teletransporte", "Emissão"),
            ("Controle mental/telecinese", "Manipulação"),
            ("Criar objetos do nada", "Materialização"),
            ("Mudar as propriedades físicas das coisas", "Transmutação"),
            ("Prever o futuro/ler memórias", "Especialização")
        ]
    }
]

# Inicialização do Estado
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'home'
if 'respostas' not in st.session_state:
    st.session_state.respostas = []
if 'scores' not in st.session_state:
    st.session_state.scores = {tipo: 0 for tipo in TIPOS_AURA}
if 'usuario' not in st.session_state:
    st.session_state.usuario = {}
if 'premium_unlocked' not in st.session_state:
    st.session_state.premium_unlocked = False

# Funções de Navegação
def mudar_etapa(nova_etapa):
    st.session_state.etapa = nova_etapa

# ==========================================
# PÁGINA INICIAL
# ==========================================
if st.session_state.etapa == 'home':
    st.markdown('<p class="main-title">⚡ AuraDex ⚡</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Descubra seu perfil de aura e seu potencial oculto.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Bem-vindo!</h3>
            <p>Este sistema avançado analisa sua personalidade, emoções e reações para determinar sua afinidade de energia espiritual e Habilidade Exclusiva.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("COMEÇAR TESTE", use_container_width=True, type="primary"):
            mudar_etapa('cadastro')
            st.rerun()

# ==========================================
# CADASTRO
# ==========================================
elif st.session_state.etapa == 'cadastro':
    st.markdown('<p class="main-title">⚡ Cadastro ⚡</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("form_cadastro"):
        nome = st.text_input("Primeiro Nome *")
        idade = st.number_input("Idade *", min_value=10, max_value=120, step=1)
        apelido = st.text_input("Apelido (Opcional)")
        
        submitted = st.form_submit_button("Prosseguir", use_container_width=True)
        if submitted:
            if nome.strip() == "":
                st.error("Por favor, preencha seu primeiro nome.")
            else:
                st.session_state.usuario = {
                    "nome": nome,
                    "idade": idade,
                    "apelido": apelido if apelido else nome
                }
                mudar_etapa('teste')
                st.rerun()

# ==========================================
# TESTE GRATUITO
# ==========================================
elif st.session_state.etapa == 'teste':
    st.markdown('<p class="main-title">⚡ Análise de Aura ⚡</p>', unsafe_allow_html=True)
    st.progress(0, text="Progresso: 0%")
    
    with st.form("form_teste"):
        respostas_temp = []
        for i, pergunta in enumerate(PERGUNTAS):
            st.markdown(f"**{pergunta['texto']}**")
            opcoes_texto = [op[0] for op in pergunta["opcoes"]]
            resp = st.radio("Selecione:", opcoes_texto, key=f"q_{i}", label_visibility="collapsed")
            respostas_temp.append(resp)
            st.markdown("---")
            
        submit_teste = st.form_submit_button("FINALIZAR E ANALISAR", use_container_width=True)
        
        if submit_teste:
            st.session_state.respostas = respostas_temp
            # Calcular scores
            for i, resp_texto in enumerate(respostas_temp):
                for opcao, tipo in PERGUNTAS[i]["opcoes"]:
                    if resp_texto == opcao:
                        st.session_state.scores[tipo] += 1
            mudar_etapa('resultado_free')
            st.rerun()

# ==========================================
# BLOQUEIO PREMIUM & RESULTADO PARCIAL
# ==========================================
elif st.session_state.etapa == 'resultado_free':
    st.markdown('<p class="main-title">⚡ Resultado Parcial ⚡</p>', unsafe_allow_html=True)
    
    scores = st.session_state.scores
    tipo_predominante = max(scores, key=scores.get)
    total_pontos = sum(scores.values())
    confianca = int((scores[tipo_predominante] / total_pontos) * 100) + random.randint(20, 40)
    if confianca > 99: confianca = 99
    
    st.session_state.tipo_principal = tipo_predominante
    
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h2 style="color: #A0AAB2;">Tipo Predominante:</h2>
        <h1 style="color: #FFD700; font-size: 2.5rem;">{tipo_predominante}</h1>
        <p>Afinidade Base Calculada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Confiança da Análise: {confianca}%**")
    st.progress(confianca)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # PAYWALL
    st.markdown(f"""
    <div class="card premium-lock">
        <h2>🔒 Relatório Premium Bloqueado</h2>
        <p style="color:#ddd; margin-bottom: 20px;">Desbloqueie todo o seu potencial e descubra seus dados completos.</p>
        <div style="text-align: left; max-width: 300px; margin: 0 auto; color: #4CAF50;">
            <b>Benefícios Exclusivos:</b><br>
            ✓ Tipo principal e secundário detalhados<br>
            ✓ Potencial máximo estimado<br>
            ✓ Simulação do Teste da Folha<br>
            ✓ Hexágono de Afinidades (Gráfico Radar)<br>
            ✓ Geração de Habilidade Exclusiva<br>
            ✓ Carta Visual Personalizada<br>
        </div>
        <br>
        <a href="{MERCADO_PAGO_URL}" target="_blank" class="btn-pay">DESBLOQUEAR POR R$ {PRECO_PREMIUM:.2f}</a>
    </div>
    """, unsafe_allow_html=True)
    
# ==========================================
# RELATÓRIO PREMIUM
# ==========================================
elif st.session_state.etapa == 'relatorio_premium':
    st.success("✅ Acesso Premium Desbloqueado!")
    
    # Processamento de Dados Premium
    scores = st.session_state.scores
    tipos_ordenados = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    tipo_principal = tipos_ordenados[0][0]
    tipo_secundario = tipos_ordenados[1][0]
    
    potencial = random.randint(8500, 150000)
    ranks = ["D", "C", "B", "A", "S", "SS"]
    rank_idx = min(5, int((potencial - 8500) / 25000))
    rank_final = ranks[rank_idx]
    
    nome_usuario = st.session_state.usuario['apelido']
    
    st.markdown('<p class="main-title">⚡ Dossiê Completo ⚡</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. PERFIL
    st.subheader("👤 Perfil de Aura")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <h4>Tipo Principal</h4>
            <h2 style="color: #FFD700;">{tipo_principal}</h2>
            <h4>Tipo Secundário</h4>
            <h3 style="color: #A0AAB2;">{tipo_secundario}</h3>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h4>Classificação Global</h4>
            <p class="rank-text">Rank {rank_final}</p>
            <p>Potencial de Aura: {potencial:,}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 2. TESTE DA FOLHA (ANIMAÇÃO)
    st.subheader("🍃 Teste da Folha (Simulação da Taça d'Água)")
    st.write("Iniciando fluxo de Nen...")
    
    placeholder = st.empty()
    animacoes = ["💧 Colocando água...", "🍃 Colocando a folha...", "⚡ Focando a aura..."]
    for anim in animacoes:
        placeholder.markdown(f"### {anim}")
        time.sleep(0.8)
    
    msg_folha = ""
    if tipo_principal == "Reforço": msg_folha = "💧⬆️ O volume da água aumentou e transbordou do copo!"
    elif tipo_principal == "Emissão": msg_folha = "💧🎨 A água mudou de cor bruscamente!"
    elif tipo_principal == "Manipulação": msg_folha = "🍃🔄 A folha começou a se mover sozinha na superfície!"
    elif tipo_principal == "Materialização": msg_folha = "💧✨ Impurezas cristalizadas apareceram na água!"
    elif tipo_principal == "Transmutação": msg_folha = "💧👅 A água mudou completamente de sabor (ficou doce)!"
    elif tipo_principal == "Especialização": msg_folha = "🌀 Fenômeno estranho: a folha secou e a água começou a flutuar!"
    
    placeholder.markdown(f"### {msg_folha}")
    
    st.markdown("---")
    
    # 3. HEXÁGONO DE AFINIDADES
    st.subheader("⬡ Hexágono de Afinidades")
    
    # Lógica de distribuição adjacente baseada em Hunter x Hunter
    ordem_hx = ["Reforço", "Emissão", "Manipulação", "Especialização", "Materialização", "Transmutação"]
    idx_principal = ordem_hx.index(tipo_principal)
    
    valores_radar = []
    for tipo in ordem_hx:
        if tipo == tipo_principal:
            valores_radar.append(100)
        else:
            # Distância no ciclo
            dist = min(abs(ordem_hx.index(tipo) - idx_principal), 6 - abs(ordem_hx.index(tipo) - idx_principal))
            if dist == 1: valores_radar.append(random.randint(70, 80))
            elif dist == 2: valores_radar.append(random.randint(50, 60))
            elif dist == 3: valores_radar.append(random.randint(0, 40) if tipo != "Especialização" else 0)
            
    # Especialização (0 a não ser que seja vizinho ou o próprio)
    if tipo_principal != "Especialização" and "Especialização" in ordem_hx:
        idx_esp = ordem_hx.index("Especialização")
        if min(abs(idx_esp - idx_principal), 6 - abs(idx_esp - idx_principal)) > 1:
            valores_radar[idx_esp] = 0

    # Fechar o ciclo do radar
    ordem_hx.append(ordem_hx[0])
    valores_radar.append(valores_radar[0])
    
    fig = go.Figure(data=go.Scatterpolar(
        r=valores_radar,
        theta=ordem_hx,
        fill='toself',
        fillcolor='rgba(255, 215, 0, 0.4)',
        line=dict(color='#FFD700')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#2D303E'),
            angularaxis=dict(gridcolor='#2D303E')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 4. GERADOR DE HABILIDADE
    st.subheader("⚔️ Sua Habilidade Exclusiva")
    
    prefixos = ["Sombra", "Chama", "Eco", "Vórtice", "Corte", "Manto", "Visão", "Coração"]
    sufixos = ["Absoluto(a)", "Fragmentado(a)", "das Feras", "Ilusório(a)", "do Trovão", "Etéreo(a)"]
    hab_nome = f"{random.choice(prefixos)} {random.choice(sufixos)}"
    
    raridades = ["Incomum", "Raro", "Épico", "Lendário", "Mítico"]
    raridade = raridades[rank_idx if rank_idx < len(raridades) else -1]
    
    st.markdown(f"""
    <div class="card">
        <h3 style="color: #00C6FF;">{hab_nome}</h3>
        <p><b>Raridade:</b> {raridade}</p>
        <p><b>Descrição:</b> Uma técnica desenvolvida subconscientemente que reflete seus desejos mais profundos. Permite aplicar {tipo_principal} em situações críticas.</p>
        <p>🟢 <b>Força:</b> Altamente eficaz contra tipos que não conseguem prever táticas adaptativas.</p>
        <p>🔴 <b>Fraqueza:</b> Consome grande parte do potencial se ativada com o estado emocional abalado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 5. CARTA FINAL
    st.subheader("🃏 Sua Carta Hunter/Aura")
    st.markdown(f"""
    <div class="final-card">
        <h2>{nome_usuario.upper()}</h2>
        <br>
        <div style="font-size: 5rem; line-height: 1;">{"★" * (rank_idx + 1)}</div>
        <br>
        <p style="color: #FFD700; font-weight: bold; font-size: 1.2rem;">[{tipo_principal}]</p>
        <p>Sub: {tipo_secundario}</p>
        <h1 class="rank-text" style="font-size: 3rem;">RANK {rank_final}</h1>
        <p style="margin-top:20px;"><b>Técnica:</b> {hab_nome}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 6. COMPARTILHAMENTO
    st.markdown("<br>", unsafe_allow_html=True)
    texto_share = f"Fiz o teste no AuraDex!\n👤 Nome: {nome_usuario}\n⚡ Tipo: {tipo_principal}\n🏆 Rank: {rank_final}\n⚔️ Habilidade: {hab_nome}\nDescubra o seu em: {BASE_URL}"
    url_share = f"https://wa.me/?text={urllib.parse.quote(texto_share)}"
    
    st.markdown(f"""
    <div style="text-align: center;">
        <a href="{url_share}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 1.1rem;">
            📱 Compartilhar Resultado no WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)
