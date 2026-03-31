import streamlit as st
import time

# Configuration de la page
st.set_page_config(
    page_title="Comprendre l'IA : Sous le capot",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Voyage au cœur d'une IA (LLM)")
st.write(
    "Cette interface interactive explique les concepts clés du fonctionnement des modèles "
    "de langage comme GPT ou Gemini, puis montre comment choisir le bon mode de Copilot "
    "et comment relier l'arrivée de l'IA à ce que les entreprises ont vécu avec Internet."
)

st.divider()

# ============================================================
# SECTION 1 : LES TOKENS
# ============================================================
st.header("🧩 1. Qu'est-ce qu'un Token ?")
st.write(
    "Les modèles d'IA ne lisent pas les mots comme nous. Ils découpent le texte en petits "
    "morceaux appelés **tokens**. Un token peut être un mot entier, une syllabe, ou même "
    "une seule lettre."
)

user_text = st.text_input(
    "Tapez une phrase pour voir comment l'IA la 'tokenise' :",
    "L'ingénierie mécanique évolue vite."
)

def simulate_tokenization(text):
    # Simulation basique de tokenisation
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
    st.write(f"Votre phrase a été découpée en **{len(tokens)} tokens** :")

    colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
    token_html = ""
    for i, token in enumerate(tokens):
        color = colors[i % len(colors)]
        token_html += (
            f'<span style="background-color:{color}; color:black; padding:4px 8px; '
            f'border-radius:4px; margin:2px; display:inline-block; font-family:monospace;">'
            f'{token}</span>'
        )

    st.markdown(token_html, unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 2 : FENÊTRE DE CONTEXTE ET INPUT/OUTPUT
# ============================================================
st.header("🪟 2. Input / Output et Fenêtre de Contexte")
st.write(
    "Le **contexte** est la mémoire à court terme de l'IA. Si un texte (Input) est plus long "
    "que sa **fenêtre de contexte**, l'IA 'oublie' le début de la conversation pour pouvoir "
    "générer la suite (Output)."
)

context_size = st.slider(
    "Réglez la taille de la fenêtre de contexte (en nombre de mots/tokens) :",
    min_value=5,
    max_value=40,
    value=15
)

long_text = (
    "Bonjour IA. Je m'appelle Jean. Je suis ingénieur en CVC. "
    "Mon bâtiment actuel a un problème de surchauffe au 3ème étage. "
    "La climatisation est une pompe à chaleur air-eau. Que dois-je vérifier en premier ?"
)
words = long_text.split()

st.subheader("Ce que l'IA 'voit' avant de répondre :")
if context_size < len(words):
    forgotten_text = " ".join(words[:-context_size])
    remembered_text = " ".join(words[-context_size:])

    st.markdown(
        f"<span style='color:grey; text-decoration:line-through;'>{forgotten_text}</span> "
        f"<span style='background-color:#E6F3FF; font-weight:bold; padding:2px;'>{remembered_text}</span>",
        unsafe_allow_html=True
    )
    st.warning(
        "⚠️ La fenêtre de contexte est trop petite. L'IA a oublié le début "
        "(dont votre prénom et votre métier !)."
    )

    if st.button("Générer la réponse (Output) 🔴"):
        st.info(
            "Output : Vous devriez vérifier les paramètres de votre pompe à chaleur air-eau "
            "ou les vannes du 3ème étage. "
            "(Note : l'IA a oublié que vous étiez ingénieur, sa réponse risque d'être trop basique)."
        )
else:
    st.markdown(
        f"<span style='background-color:#E6F3FF; font-weight:bold; padding:2px;'>{long_text}</span>",
        unsafe_allow_html=True
    )
    st.success("✅ Le texte entier rentre dans la fenêtre de contexte. L'IA a toutes les informations.")

    if st.button("Générer la réponse (Output) 🟢"):
        st.info(
            "Output : Bonjour Jean, en tant qu'ingénieur CVC, vous savez que pour votre PAC air-eau, "
            "il faut vérifier le débit d'eau froide vers les terminaux du 3ème étage et la consigne "
            "de la régulation de zone."
        )

st.divider()

# ============================================================
# SECTION 3 : CAPACITÉ DE RAISONNEMENT
# ============================================================
st.header("⚙️ 3. Capacité de Raisonnement")
st.write(
    "Les modèles modernes ne se contentent pas de deviner le mot suivant. "
    "On peut leur demander de **prendre plus ou moins de temps pour raisonner** "
    "avant de fournir leur réponse finale."
)

problem = (
    "Un ascenseur peut porter 800 kg. Chaque personne pèse en moyenne 75 kg, "
    "et il y a déjà 3 personnes dedans. Il y a un colis de 200 kg. "
    "Combien de personnes supplémentaires peuvent entrer ?"
)

st.write("**Problème posé à l'IA :**")
st.info(problem)

reasoning_mode = st.radio(
    "Comment l'IA doit-elle traiter le problème ?",
    ["Réponse directe (Risque d'erreur)", "Réflexion étape par étape (Raisonnement actif)"]
)

if st.button("Lancer l'analyse"):
    if reasoning_mode == "Réponse directe (Risque d'erreur)":
        with st.spinner("Génération de l'output..."):
            time.sleep(1)
        st.error("**Output direct :** L'ascenseur peut encore prendre 4 personnes.")
        st.write(
            "*(L'IA a répondu trop vite sans faire les calculs intermédiaires, "
            "ce qui mène souvent à des erreurs.)*"
        )
    else:
        with st.status("L'IA réfléchit...", expanded=True) as status:
            st.write("📝 **Étape 1 :** Capacité totale = 800 kg.")
            time.sleep(1)
            st.write("📝 **Étape 2 :** Poids actuel des 3 personnes = 3 × 75 kg = 225 kg.")
            time.sleep(1)
            st.write("📝 **Étape 3 :** Poids du colis = 200 kg. Poids total actuel = 225 + 200 = 425 kg.")
            time.sleep(1)
            st.write("📝 **Étape 4 :** Poids restant disponible = 800 - 425 = 375 kg.")
            time.sleep(1)
            st.write("📝 **Étape 5 :** Nombre de personnes supplémentaires = 375 / 75 = 5 personnes.")
            time.sleep(1)
            status.update(label="Raisonnement terminé !", state="complete", expanded=False)

        st.success("**Output final :** L'ascenseur peut encore accueillir 5 personnes supplémentaires.")

st.divider()

# ============================================================
# SECTION 4 : COMMENT CHOISIR LE BON MODE / MODÈLE COPILOT
# ============================================================
st.header("🧭 4. Comment choisir le bon mode / modèle Copilot ?")
st.write(
    "Dans Copilot, on ne choisit pas seulement *ce qu'on demande* : on choisit aussi "
    "**la manière dont l'IA doit travailler**. Pour un besoin simple, une réponse rapide suffit. "
    "Pour une tâche complexe, risquée ou très métier, il faut un mode plus réfléchi."
)

st.subheader("4.1 Votre besoin métier")
task = st.selectbox(
    "Quel type de tâche voulez-vous confier à Copilot ?",
    [
        "Rédiger un mail simple à un fournisseur",
        "Résumer un compte-rendu technique",
        "Comparer plusieurs options techniques HVAC / groupe froid",
        "Analyser un avenant contractuel ou une clause sensible",
        "Préparer une note de synthèse pour arbitrage",
        "Créer une checklist de points à vérifier",
        "Identifier les risques / oublis dans un document",
    ]
)

col1, col2 = st.columns(2)
with col1:
    complexity = st.slider("Complexité de la tâche", 1, 5, 3)
    urgency = st.slider("Urgence / besoin de vitesse", 1, 5, 3)
with col2:
    criticality = st.slider("Criticité métier / impact si erreur", 1, 5, 4)
    traceability = st.slider("Besoin de justification / explicabilité", 1, 5, 4)

st.subheader("4.2 Recommandation guidée")

def recommend_mode(task, complexity, urgency, criticality, traceability):
    # Cas très simples et urgents
    if urgency >= 4 and complexity <= 2 and criticality <= 2:
        return {
            "mode": "⚡ Réponse rapide",
            "model": "GPT-5.3 Quick response (ou équivalent rapide)",
            "why": (
                "Votre besoin privilégie la vitesse. La tâche est simple, peu risquée, "
                "et peut être traitée sans raisonnement approfondi."
            ),
            "use_for": [
                "mails simples",
                "reformulation de texte",
                "résumé court",
                "mise en forme rapide",
                "questions factuelles simples"
            ],
            "avoid_for": [
                "analyse contractuelle sensible",
                "comparaison multi-critères",
                "décision engageante",
                "documents techniques complexes"
            ],
            "prompt_tip": (
                "Réponds en 5 points maximum, style professionnel, ton direct, "
                "et propose une version prête à envoyer."
            )
        }

    # Cas très critiques / complexes
    if complexity >= 4 or criticality >= 4 or traceability >= 4:
        return {
            "mode": "🧠 Réponse approfondie",
            "model": "GPT-5.4 Think deeper (ou mode approfondi équivalent)",
            "why": (
                "La tâche demande plus de recul, une meilleure structuration et moins de risque d'erreur. "
                "C'est adapté aux cas où il faut comparer, vérifier, justifier ou détecter des oublis."
            ),
            "use_for": [
                "analyse de clauses",
                "revue d'avenants",
                "comparaison d'options techniques",
                "synthèse pour arbitrage",
                "analyse de risques"
            ],
            "avoid_for": [
                "micro-demandes du quotidien",
                "messages courts à faible enjeu"
            ],
            "prompt_tip": (
                "Analyse la demande en distinguant : hypothèses, points d'attention, risques, "
                "et recommandations. Si une information manque, liste les questions à poser."
            )
        }

    # Cas intermédiaires
    return {
        "mode": "🤖 Automatique",
        "model": "Sélection automatique par Copilot",
        "why": (
            "Votre besoin est intermédiaire : ni trivial, ni extrêmement critique. "
            "Laisser Copilot arbitrer entre vitesse et profondeur est souvent le meilleur compromis."
        ),
        "use_for": [
            "travail courant",
            "première ébauche",
            "questions mixtes",
            "synthèses de niveau intermédiaire"
        ],
        "avoid_for": [
            "validation finale d'un sujet engageant"
        ],
        "prompt_tip": (
            "Commencez en automatique pour la première réponse, puis basculez en "
            "réponse approfondie si vous voulez une analyse plus robuste."
        )
    }

rec = recommend_mode(task, complexity, urgency, criticality, traceability)

st.success(f"**Mode conseillé :** {rec['mode']}")
st.info(f"**Modèle / profil conseillé :** {rec['model']}")

st.write("**Pourquoi ?**")
st.write(rec["why"])

col_a, col_b = st.columns(2)

with col_a:
    st.write("**✅ Pertinent pour :**")
    for item in rec["use_for"]:
        st.write(f"- {item}")

with col_b:
    st.write("**⚠️ À éviter pour :**")
    for item in rec["avoid_for"]:
        st.write(f"- {item}")

st.write("**💡 Astuce de prompt :**")
st.code(rec["prompt_tip"], language="text")

st.subheader("4.3 Exemples adaptés à un service contrat HVAC / groupe froid / nucléaire")

examples = {
    "Rédiger un mail simple à un fournisseur": {
        "mode": "⚡ Réponse rapide",
        "example": (
            "Exemple : reformuler un mail de relance documentaire, clarifier une demande de planning, "
            "ou demander la dernière révision d'un document."
        )
    },
    "Résumer un compte-rendu technique": {
        "mode": "🤖 Automatique",
        "example": (
            "Exemple : extraire les 5 décisions, 3 actions et 2 points bloquants d'une réunion technique."
        )
    },
    "Comparer plusieurs options techniques HVAC / groupe froid": {
        "mode": "🧠 Réponse approfondie",
        "example": (
            "Exemple : comparer 3 architectures de distribution d'eau glacée selon maintenance, robustesse, "
            "exploitabilité, interfaces contrat et impacts planning."
        )
    },
    "Analyser un avenant contractuel ou une clause sensible": {
        "mode": "🧠 Réponse approfondie",
        "example": (
            "Exemple : repérer les formulations ambiguës, les transferts de responsabilité, "
            "les risques de claims ou les écarts par rapport au contrat de base."
        )
    },
    "Préparer une note de synthèse pour arbitrage": {
        "mode": "🧠 Réponse approfondie",
        "example": (
            "Exemple : préparer une note 'décision à prendre' avec options, avantages, risques, impacts coûts/délais."
        )
    },
    "Créer une checklist de points à vérifier": {
        "mode": "🤖 Automatique",
        "example": (
            "Exemple : construire une checklist de revue d'un dossier fournisseur ou d'une réponse à consultation."
        )
    },
    "Identifier les risques / oublis dans un document": {
        "mode": "🧠 Réponse approfondie",
        "example": (
            "Exemple : détecter les exigences manquantes, interfaces oubliées, hypothèses implicites "
            "ou points non couverts dans un document technique/contractuel."
        )
    }
}

selected_example = examples[task]
st.write(f"**Mode généralement pertinent :** {selected_example['mode']}")
st.write(selected_example["example"])

st.warning(
    "🔒 En environnement nucléaire ou sur un sujet contractuel engageant, l'IA doit être utilisée "
    "comme **assistant d'analyse et de préparation**, pas comme validateur final. "
    "La validation humaine reste indispensable avant toute décision, émission ou engagement."
)

st.divider()

# ============================================================
# SECTION 5 : INTERNET VS IA DANS L'ENTREPRISE
# ============================================================
st.header("🌐 5. Faire le parallèle entre l'arrivée d'Internet et l'arrivée de l'IA")
st.write(
    "L'arrivée de l'IA en entreprise ressemble, à plusieurs égards, à l'arrivée d'Internet : "
    "au début, on y voit surtout un outil 'impressionnant'. Puis, très vite, cela devient un "
    "**nouveau réflexe de travail**."
)

st.subheader("5.1 Le parallèle en une phrase")
st.markdown(
    """
- **Internet a changé l'accès à l'information.**
- **L'IA change l'exploitation de l'information.**
    """
)

comparison_view = st.radio(
    "Choisissez un angle de comparaison :",
    [
        "Accès à l'information",
        "Gain de productivité",
        "Nouveaux risques",
        "Impact sur les métiers",
        "Cas concret pour un service contrat HVAC / groupe froid"
    ]
)

if comparison_view == "Accès à l'information":
    st.info(
        "Hier avec Internet : on accède plus vite aux documents, fournisseurs, normes, échanges, catalogues."
    )
    st.success(
        "Aujourd'hui avec l'IA : on ne se contente plus d'accéder à l'information, "
        "on lui demande de la trier, la résumer, la comparer, détecter des écarts, et préparer une synthèse."
    )

elif comparison_view == "Gain de productivité":
    st.info(
        "Hier avec Internet : moins de temps perdu à chercher une information dispersée."
    )
    st.success(
        "Aujourd'hui avec l'IA : moins de temps perdu à lire 50 pages pour trouver "
        "les 5 points qui comptent vraiment."
    )

elif comparison_view == "Nouveaux risques":
    st.info(
        "Hier avec Internet : risque d'information non fiable, non à jour, non maîtrisée."
    )
    st.success(
        "Aujourd'hui avec l'IA : mêmes risques, plus un risque supplémentaire : "
        "obtenir une réponse fluide mais inexacte, incomplète ou trop confiante."
    )

elif comparison_view == "Impact sur les métiers":
    st.info(
        "Hier avec Internet : les métiers n'ont pas disparu, mais la façon de travailler a changé."
    )
    st.success(
        "Aujourd'hui avec l'IA : l'expert ne disparaît pas. En revanche, l'expert qui sait "
        "piloter l'IA travaille plus vite, plus haut dans la chaîne de valeur, et passe moins "
        "de temps sur les tâches répétitives."
    )

else:
    st.info(
        "Dans un service contrat HVAC / groupe froid en environnement nucléaire, Internet a surtout "
        "accéléré la circulation des documents et des échanges. L'IA, elle, peut accélérer la "
        "lecture utile des documents."
    )
    st.success(
        "Exemples : comparer des clauses, extraire les exigences d'un cahier des charges, "
        "préparer une note de synthèse, repérer des points d'interface oubliés, ou proposer "
        "une trame de questions à poser à un fournisseur."
    )

st.subheader("5.2 Avant / Après : ce qui change dans la pratique")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🌐 Quand Internet est arrivé")
    st.write("- On a trouvé l'information plus vite")
    st.write("- On a échangé plus vite")
    st.write("- On a moins dépendu du papier")
    st.write("- On a appris à vérifier les sources")
    st.write("- On a dû créer des règles d'usage et de cybersécurité")

with col_right:
    st.markdown("### 🧠 Avec l'IA aujourd'hui")
    st.write("- On comprend l'information plus vite")
    st.write("- On produit des synthèses plus vite")
    st.write("- On délègue la première lecture ou la première trame")
    st.write("- On doit vérifier les réponses et les hypothèses")
    st.write("- On doit définir quand l'IA aide... et quand l'humain tranche")

st.subheader("5.3 Ce que cela veut dire pour votre service")
maturity = st.select_slider(
    "À quel niveau de maturité voulez-vous illustrer l'usage de l'IA ?",
    options=[
        "Niveau 1 - Découverte",
        "Niveau 2 - Assistant personnel",
        "Niveau 3 - Standardisation d'équipe",
        "Niveau 4 - Appui aux décisions",
        "Niveau 5 - Intégration dans les processus"
    ],
    value="Niveau 3 - Standardisation d'équipe"
)

if maturity == "Niveau 1 - Découverte":
    st.write(
        "**Message clé :** l'IA sert d'abord à gagner du temps sur les tâches à faible enjeu : "
        "résumer, reformuler, préparer une trame."
    )

elif maturity == "Niveau 2 - Assistant personnel":
    st.write(
        "**Message clé :** chaque ingénieur / contract manager peut avoir un copilote personnel "
        "pour préparer ses notes, ses relances, ses synthèses et ses checklists."
    )

elif maturity == "Niveau 3 - Standardisation d'équipe":
    st.write(
        "**Message clé :** l'IA permet d'harmoniser les pratiques : mêmes structures de notes, "
        "mêmes checklists, mêmes trames d'analyse, même qualité minimale de synthèse."
    )

elif maturity == "Niveau 4 - Appui aux décisions":
    st.write(
        "**Message clé :** l'IA peut préparer les arbitrages, mais ne décide pas. "
        "Elle met en évidence options, impacts, risques et questions ouvertes."
    )

else:
    st.write(
        "**Message clé :** l'IA peut être intégrée aux routines de travail : "
        "revue documentaire, préparation de réunions, extraction d'exigences, "
        "pré-contrôle de cohérence, capitalisation de retour d'expérience."
    )

st.subheader("5.4 Message de conclusion prêt à présenter")
final_message = """
Hier, Internet a permis à l'entreprise de mieux accéder à l'information.
Aujourd'hui, l'IA permet à l'entreprise de mieux exploiter cette information.

Dans un service contrat HVAC / groupe froid / nucléaire, cela ne remplace ni l'expertise,
ni la responsabilité, ni la validation humaine. En revanche, cela réduit fortement
le temps passé à chercher, relire, trier et reformuler, pour concentrer l'effort
sur ce qui a le plus de valeur : l'analyse, l'anticipation des risques et la décision.
"""
st.code(final_message.strip(), language="text")

st.divider()
st.caption(
    "Développé pour illustrer les concepts de base de l'Intelligence Artificielle générative, "
    "les modes de Copilot, et leur impact concret en environnement industriel."
)
