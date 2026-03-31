import streamlit as st
import time
import random

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Comprendre l'IA : Sous le capot",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("📌 Comment utiliser cette démo")
    st.write("""
    Cette application sert :
    - pendant la présentation (démo guidée),
    - après la présentation (relecture autonome).

    Contenu :
    1. Tokens  
    2. Contexte  
    3. Raisonnement  
    4. Mode Copilot  
    5. Internet vs IA  
    6. Pourquoi les ingénieurs s’y intéressent  
    7. D'autres éléments  
    8. Limites & précautions
    """)

# ============================================================
# INTRO
# ============================================================

st.title("🧠 Voyage au cœur d'une IA (LLM)")

st.markdown("""
### Pourquoi cette application ?

Cette démonstration a 3 objectifs :

- 🎯 Comprendre comment fonctionne une IA générative  
- 🚀 Montrer pourquoi l’IA est un **tournant majeur** dans nos métiers  
- 📈 Expliquer pourquoi les ingénieurs ont **tout intérêt à s’y intéresser**

❗ L’IA ne remplace pas l’ingénieur :  
Elle **augmente** notre capacité à lire, analyser, structurer, comparer et produire plus vite.
""")

st.divider()


###############################################################
# SECTION 1 — TOKENS
###############################################################
st.header("🧩 1. Qu'est-ce qu'un Token ?")

st.write("Les modèles d’IA découpent le texte en petites unités (mots, sous-mots, lettres).")

user_text = st.text_input("Exemple :", "L'ingénierie mécanique évolue vite.")

def simulate_tokenization(text):
    text = text.replace("'", "' ")
    words = text.split()
    tokens = []
    for word in words:
        if len(word) > 6:
            tokens.append(word[:4])
            tokens.append(word[4:])
        else:
            tokens.append(word)
    return tokens

if user_text:
    tokens = simulate_tokenization(user_text)
    st.write(f"→ **{len(tokens)} tokens**")

    colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
    out = ""
    for i, t in enumerate(tokens):
        out += f"<span style='background:{colors[i%6]}; padding:4px; margin:3px; border-radius:3px'>{t}</span>"
    st.markdown(out, unsafe_allow_html=True)

st.divider()


###############################################################
# SECTION 2 — CONTEXTE
###############################################################
st.header("🪟 2. Fenêtre de Contexte")

context_size = st.slider("Taille de la fenêtre :", 5, 40, 15)

long_text = (
    "Bonjour IA. Je m'appelle Jean. Je suis ingénieur en CVC. "
    "Mon bâtiment actuel a un problème de surchauffe au 3e étage. "
    "La climatisation est une PAC air-eau. Que dois-je vérifier ?"
)

words = long_text.split()

if context_size < len(words):
    forgotten = " ".join(words[:-context_size])
    remembered = " ".join(words[-context_size:])
    st.markdown(
        f"<span style='color:grey;text-decoration:line-through;'>{forgotten}</span> "
        f"<span style='background:#E6F3FF;font-weight:bold'>{remembered}</span>",
        unsafe_allow_html=True
    )
    st.warning("L’IA oublie le début.")
else:
    st.success("Toute l'information rentre.")
    st.markdown(f"<span style='background:#E6F3FF'>{long_text}</span>", unsafe_allow_html=True)

st.divider()


###############################################################
# SECTION 3 — RAISONNEMENT
###############################################################
st.header("⚙️ 3. Capacité de Raisonnement")

problem = (
    "Un ascenseur supporte 800 kg. 3 personnes (75 kg) + un colis de 200 kg sont dedans. "
    "Combien de personnes peuvent encore entrer ?"
)
st.info(problem)

mode = st.radio("Mode :", ["Direct", "Raisonnement étape par étape"])

if st.button("Lancer"):
    if mode == "Direct":
        st.error("→ Réponse directe (erronée) : 4 personnes")
    else:
        with st.status("Réflexion en cours..."):
            steps = [
                "Poids actuel : 3×75 = 225",
                "225 + 200 = 425",
                "Reste : 800 – 425 = 375",
                "375 / 75 = 5"
            ]
            for s in steps:
                st.write("📝", s)
                time.sleep(0.5)
        st.success("→ Réponse correcte : **5 personnes**")

st.divider()


###############################################################
# SECTION 4 — MODE COPILOT
###############################################################

st.header("🧭 4. Comment choisir le bon mode Copilot ?")

TASK_PROFILES = {
    "Rédiger un mail simple": (1, 5, 2, 2),
    "Résumer un CR technique": (3, 3, 3, 3),
    "Comparer options HVAC": (4, 2, 4, 5),
    "Analyser un avenant": (5, 2, 5, 5),
    "Préparer une note d’arbitrage": (4, 3, 5, 5),
}

if "task" not in st.session_state:
    st.session_state.task = "Préparer une note d’arbitrage"
if "manual" not in st.session_state:
    st.session_state.manual = False

def update_profile():
    if not st.session_state.manual:
        c,u,crit,t = TASK_PROFILES[st.session_state.task]
        st.session_state.complexity = c
        st.session_state.urgency = u
        st.session_state.criticality = crit
        st.session_state.traceability = t

update_profile()

scope = st.radio(
    "Périmètre d’activité :",
    ["Activité non AIP", "Activité AIP / sûreté réglementée"]
)

if scope == "Activité AIP / sûreté réglementée":
    st.error("Recommandations IA inapplicables. Validation humaine obligatoire.")
else:
    st.success("OK pour activités **non AIP**.")

    st.selectbox("Type de tâche :", list(TASK_PROFILES.keys()), key="task", on_change=update_profile)
    st.checkbox("Ajuster manuellement", key="manual")

    col1, col2 = st.columns(2)
    with col1:
        st.slider("Complexité", 1, 5, key="complexity")
        st.slider("Urgence", 1, 5, key="urgency")
    with col2:
        st.slider("Criticité métier", 1, 5, key="criticality")
        st.slider("Besoin d’explicabilité", 1, 5, key="traceability")

    st.subheader("Mode conseillé")
    if st.session_state.urgency >= 4 and st.session_state.complexity <= 2:
        st.success("→ Mode : **Réponse rapide**")
    elif st.session_state.complexity >= 4 or st.session_state.criticality >= 4:
        st.success("→ Mode : **Réponse approfondie (Think deeper)**")
    else:
        st.success("→ Mode : **Automatique**")

st.divider()


###############################################################
# SECTION 5 — INTERNET VS IA
###############################################################

st.header("🌐 5. Internet vs IA")

st.markdown("""
- Internet → accès à l'information  
- IA → exploitation de l'information  
""")

st.divider()


###############################################################
# SECTION 6 — POURQUOI LES INGÉNIEURS
###############################################################

st.header("🚀 6. Pourquoi les ingénieurs doivent s’y intéresser")

st.markdown("""
### L’IA permet :
- lire plus vite  
- analyser plus vite  
- comparer plus vite  
- structurer plus vite  
- rédiger plus vite  

### Ce que cela change :
→ plus de temps pour l’analyse, les arbitrages, le raisonnement et la décision  
""")

st.success("L’IA **augmente** l’ingénieur — elle ne le remplace pas.")

st.divider()


###############################################################
# SECTION 7 — NOUVEAUX MODULES INTERACTIFS
###############################################################
st.header("🧪 7. Autres éléments")



# 7.1 REFORMULATION / AMPLIFICATION DU PROMPT
st.subheader("🛠️ Transformer un prompt flou → prompt structuré")

raw = st.text_input("Votre prompt flou :", "Analyse ce document")

if raw:
    st.write("➡️ **Version améliorée** :")
    st.code(f"""
Contexte : {raw}

Objectif de l'analyse :
- Décrire clairement ce que vous souhaitez obtenir

Contraintes :
- Préciser les limites, enjeux, exigences

Format attendu :
- Liste structurée, tableau comparatif, résumé, etc.

Questions si info manquante :
- Quels éléments clés ne sont pas fournis ?
""")

st.divider()

# 7.2 BON USAGE / MAUVAIS USAGE
st.subheader("⚖️ Bon usage vs Mauvais usage")

options = {
    "Je lui demande un brouillon de note": True,
    "Je lui demande d’approuver une modification contractuelle": False,
    "Je lui demande d’identifier des points d’attention": True,
    "Je lui demande de valider la conformité sûreté": False,
}

choice = st.selectbox("Choisissez un cas :", list(options.keys()))
ok = options[choice]

if ok:
    st.success("Usage approprié ✔ (assisté, non engageant)")
else:
    st.error("Usage interdit ❌ (validation humaine obligatoire)")

st.divider()


###############################################################
# SECTION 8 — LIMITES & DISCLAIMERS
###############################################################
st.header("⚠️ 8. Limites et précautions d’usage")

st.warning("""
### Limites des modèles
- peuvent inventer (hallucinations)
- manquer d’un implicite métier
- mal comprendre un contexte flou
- répondre trop confiant même si faux  
""")

st.error("""
### Hors périmètre
⚠️ Non applicable aux activités :
- AIP  
- sûreté réglementée  
- validation contractuelle / qualité / sûreté  
""")

st.info("L’IA accélère. Elle ne valide pas.")



########
#9
####

st.header("9. En savoir +")

raw = st.text_input("""
Gardez à l'esprit que ce qui est impossible aujourd'hui ne le sera peut-être plus demain, car les avancées dans ce domaine sont extrêmement rapides.")
Voici quelques ressources pour en savoir plus:

""")

st.link_button("NotebookLM : l'IA dans l'ingénierie (ne pas ajouter d'informations confidentielles).", "https://notebooklm.google.com/notebook/6ff8483b-4e44-4fcf-a3cf-570b3f0d1788")

st.caption("Merci ;) ")
