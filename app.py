import streamlit as st
import time

# ============================================================
# CONFIGURATION
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
    - **pendant la présentation** (démo guidée),
    - **après la présentation** (relecture autonome).

    Parcourez les sections :
    1. Tokens  
    2. Contexte  
    3. Raisonnement  
    4. Choix du mode Copilot  
    5. Internet vs IA  
    6. Pourquoi les ingénieurs doivent s'y intéresser  
    7. Limites et précautions  
    """)

# ============================================================
# ENTÊTE & MESSAGE D'OUVERTURE
# ============================================================

st.title("🧠 Voyage au cœur d'une IA (LLM)")

st.markdown("""
### Pourquoi cette application ?

Cette démonstration a un objectif simple :

- 🎯 **Comprendre comment fonctionne une IA générative**
- 🚀 **Montrer pourquoi l’IA est un tournant majeur dans nos métiers**
- 📈 **Mettre en évidence pourquoi les ingénieurs doivent s’y intéresser pour rester compétitifs**

❗ L'IA ne remplace pas l’ingénieur :  
Elle **augmente** sa capacité à lire, analyser, structurer et produire plus vite.  
Comme Internet a transformé l'accès à l'information, l'IA transforme la manière de l'exploiter.
""")

st.divider()

# ============================================================
# SECTION 1 : TOKENS
# ============================================================

st.header("🧩 1. Qu'est-ce qu'un Token ?")
st.write("""
Les modèles d'IA ne lisent pas les mots comme nous.  
Ils découpent le texte en petites unités appelées **tokens** (mots, sous-mots, lettres).
""")

user_text = st.text_input(
    "Tapez une phrase pour voir comment l'IA la 'tokenise' :",
    "L'ingénierie mécanique évolue vite."
)

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
    st.write(f"Votre phrase contient **{len(tokens)} tokens**.")

    colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
    html = ""

    for i, token in enumerate(tokens):
        html += (
            f'<span style="background:{colors[i%6]}; padding:4px 8px;'
            f'border-radius:4px; margin:3px; display:inline-block;">{token}</span>'
        )

    st.markdown(html, unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 2 : FENÊTRE DE CONTEXTE
# ============================================================

st.header("🪟 2. Input / Output et Fenêtre de Contexte")

context_size = st.slider(
    "Réglez la taille de la fenêtre de contexte :",
    min_value=5, max_value=40, value=15
)

long_text = (
    "Bonjour IA. Je m'appelle Jean. Je suis ingénieur en CVC. "
    "Mon bâtiment actuel a un problème de surchauffe au 3ème étage. "
    "La climatisation est une pompe à chaleur air-eau. Que dois-je vérifier en premier ?"
)

words = long_text.split()

st.subheader("Ce que l'IA 'voit' avant de répondre :")

if context_size < len(words):
    forgotten = " ".join(words[:-context_size])
    remembered = " ".join(words[-context_size:])

    st.markdown(
        f"<span style='color:grey; text-decoration:line-through;'>{forgotten}</span> "
        f"<span style='background:#E6F3FF; font-weight:bold;'>{remembered}</span>",
        unsafe_allow_html=True
    )

    st.warning("⚠️ Texte trop long → l’IA oublie le début.")
    if st.button("Générer Output (🔴 IA a oublié des infos)"):
        st.info("Réponse : L'IA répond sans savoir que vous êtes ingénieur → réponse trop générique.")

else:
    st.success("Tout le texte tient dans la fenêtre → aucune perte d'information.")
    st.markdown(
        f"<span style='background:#E6F3FF; font-weight:bold;'>{long_text}</span>",
        unsafe_allow_html=True
    )

    if st.button("Générer Output (🟢 Toutes les infos présentes)"):
        st.info("Réponse : Analyse complète et contextualisée.")

st.divider()

# ============================================================
# SECTION 3 : RAISONNEMENT
# ============================================================

st.header("⚙️ 3. Capacité de Raisonnement (Chain of Thought)")

problem = (
    "Un ascenseur peut porter 800 kg. 3 personnes sont déjà dedans (75 kg chacune). "
    "Un colis de 200 kg est présent. Combien de personnes supplémentaires peuvent entrer ?"
)

st.info(problem)

mode = st.radio(
    "Mode de réponse :",
    ["Réponse directe (risque d'erreur)", "Raisonnement étape par étape"]
)

if st.button("Lancer l'analyse"):
    if mode == "Réponse directe (risque d'erreur)":
        st.error("**Réponse directe :** 4 personnes (erreur).")
        st.write("→ Pas de calcul → risque d’hallucination.")
    else:
        with st.status("L'IA réfléchit..."):
            steps = [
                "Capacité totale : 800 kg",
                "Poids des 3 personnes : 3 × 75 = 225 kg",
                "Ajout du colis : 225 + 200 = 425 kg",
                "Poids restant : 800 – 425 = 375 kg",
                "Personnes possibles : 375 / 75 = 5"
            ]
            for s in steps:
                st.write("📝", s)
                time.sleep(0.6)
        st.success("➡️ **Réponse correcte : 5 personnes.**")

st.divider()

# ============================================================
# SECTION 4 : CHOISIR LE BON MODE COPILOT
# ============================================================

st.header("🧭 4. Comment choisir le bon mode / modèle Copilot ?")

st.write("""
Ici, nous montrons comment choisir *Automatique*, *Réponse rapide* ou *Réponse approfondie*  
en fonction de la tâche.  
→ **Les curseurs se mettent à jour automatiquement selon la tâche.**
""")

# -------------------------
# PROFILS DE TÂCHES
# -------------------------
TASK_PROFILES = {
    "Rédiger un mail simple à un fournisseur": (1, 5, 2, 2),
    "Résumer un compte-rendu technique": (3, 3, 3, 3),
    "Comparer plusieurs options techniques HVAC": (4, 2, 4, 5),
    "Analyser un avenant contractuel": (5, 2, 5, 5),
    "Préparer une note de synthèse pour arbitrage": (4, 3, 5, 5),
    "Créer une checklist de points à vérifier": (2, 4, 3, 3),
    "Identifier des risques / oublis dans un document": (5, 2, 5, 5)
}

# -------------------------
# SESSION STATE INIT
# -------------------------
if "selected_task" not in st.session_state:
    st.session_state.selected_task = "Préparer une note de synthèse pour arbitrage"

if "manual_override" not in st.session_state:
    st.session_state.manual_override = False

def update_task_profile():
    if not st.session_state.manual_override:
        c, u, crit, t = TASK_PROFILES[st.session_state.selected_task]
        st.session_state.complexity = c
        st.session_state.urgency = u
        st.session_state.criticality = crit
        st.session_state.traceability = t

# Initialize sliders
update_task_profile()

# -------------------------
# PERIMETRE AIP
# -------------------------
st.subheader("Périmètre d’usage")

scope = st.radio(
    "Ces conseils s'appliquent à :",
    ["Activité non AIP", "Activité AIP / liée à la sûreté"]
)

if scope == "Activité AIP / liée à la sûreté":
    st.error("""
    ⛔ **Hors périmètre**  
    Les recommandations IA ne s'appliquent pas aux activités AIP / sûreté / réglementées.  
    Validation humaine obligatoire, respect du cadre interne.
    """)
else:
    st.success("Cette section s’applique aux activités **non AIP** (brouillons, synthèses, pré-analyse).")

    st.selectbox(
        "Quel type de tâche voulez-vous confier à Copilot ?",
        list(TASK_PROFILES.keys()),
        key="selected_task",
        on_change=update_task_profile
    )

    st.checkbox("Ajuster manuellement", key="manual_override")

    col1, col2 = st.columns(2)
    with col1:
        st.slider("Complexité", 1, 5, key="complexity")
        st.slider("Urgence", 1, 5, key="urgency")
    with col2:
        st.slider("Criticité", 1, 5, key="criticality")
        st.slider("Besoin d'explicabilité", 1, 5, key="traceability")

    # Recommandation simple
    st.subheader("Mode recommandé")

    if st.session_state.urgency >= 4 and st.session_state.complexity <= 2:
        st.success("→ **Mode conseillé : Réponse rapide**")
    elif (
        st.session_state.complexity >= 4
        or st.session_state.criticality >= 4
        or st.session_state.traceability >= 4
    ):
        st.success("→ **Mode conseillé : Réponse approfondie (Think deeper)**")
    else:
        st.success("→ **Mode conseillé : Automatique**")

st.divider()

# ============================================================
# SECTION 5 : INTERNET VS IA
# ============================================================

st.header("🌐 5. Internet vs IA dans l’entreprise")

st.markdown("""
### Internet → accès à l'information  
### IA → exploitation de l'information

Comme Internet a transformé nos pratiques dans les années 2000,  
**l’IA transforme notre travail d’ingénieur : synthèse, comparaison, lecture, structuration.**
""")

st.divider()

# ============================================================
# SECTION 6 : POURQUOI LES INGÉNIEURS DOIVENT S’Y INTÉRESSER
# ============================================================

st.header("🚀 6. Pourquoi les ingénieurs ont tout intérêt à s’intéresser à l’IA")

st.markdown("""
### Ce que l’IA apporte concrètement :
- Lire plus vite  
- Comparer plus vite  
- Structurer plus vite  
- Rédiger plus vite  
- Identifier des risques plus vite  

### Pourquoi cela compte :
Le temps gagné sur les tâches répétitives = plus de temps pour :  
- l’analyse,  
- la prise de recul,  
- la prise de décision,  
- les sujets à forte valeur ajoutée.
""")

st.success("L’IA ne remplace pas l’ingénieur → elle augmente sa capacité d’analyse.")

st.divider()

# ============================================================
# DISCLAIMER FINAL
# ============================================================

st.header("⚠️ 7. Limites et précautions d’usage")

st.warning("""
### 🚨 À connaître absolument
Les IA génératives peuvent :
- inventer (hallucinations),
- mal comprendre des consignes ambiguës,
- omettre des informations,
- répondre avec certitude tout en ayant tort.

→ Toujours relire, vérifier, challenger.
""")

st.error("""
### ❌ Hors périmètre
Cette démonstration ne s’applique pas :
- aux **activités importantes pour la sûreté (AIP)**,
- aux activités **réglementées / engageantes**,
- aux documents nécessitant validation qualité/sûreté/contractuelle.

Elle ne doit être utilisée que pour des **brouillons, pré-analyses, structurations, synthèses**.
""")

st.info("""
### L’IA est un assistant, pas une source d’autorité.
Elle accélère, elle ne valide pas.
""")

st.caption("Démo pédagogique — IA générative, Copilot et bonnes pratiques d’usage.")
