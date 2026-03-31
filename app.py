import streamlit as st
import time

# Configuration de la page
st.set_page_config(page_title="Comprendre l'IA : Sous le capot", page_icon="🧠", layout="centered")

st.title("🧠 Voyage au cœur d'une IA (LLM)")
st.write("Cette interface interactive explique les concepts clés du fonctionnement des modèles de langage comme GPT ou Gemini.")

st.divider()

# --- SECTION 1 : LES TOKENS ---
st.header("🧩 1. Qu'est-ce qu'un Token ?")
st.write("Les modèles d'IA ne lisent pas les mots comme nous. Ils découpent le texte en petits morceaux appelés **tokens**. Un token peut être un mot entier, une syllabe, ou même une seule lettre.")

user_text = st.text_input("Tapez une phrase pour voir comment l'IA la 'tokenise' :", "L'ingénierie mécanique évolue vite.")

def simulate_tokenization(text):
    # Simulation basique de tokenisation (séparation par espaces/apostrophes et quelques sous-mots)
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
    
    # Affichage visuel des tokens avec des couleurs
    colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
    token_html = ""
    for i, token in enumerate(tokens):
        color = colors[i % len(colors)]
        token_html += f'<span style="background-color:{color}; color:black; padding:4px 8px; border-radius:4px; margin:2px; display:inline-block; font-family:monospace;">{token}</span>'
    
    st.markdown(token_html, unsafe_allow_html=True)

st.divider()

# --- SECTION 2 : FENÊTRE DE CONTEXTE ET INPUT/OUTPUT ---
st.header("🪟 2. Input / Output et Fenêtre de Contexte")
st.write("Le **contexte** est la mémoire à court terme de l'IA. Si un texte (Input) est plus long que sa **fenêtre de contexte**, l'IA 'oublie' le début de la conversation pour pouvoir générer la suite (Output).")

context_size = st.slider("Réglez la taille de la fenêtre de contexte (en nombre de mots/tokens) :", min_value=5, max_value=40, value=15)

long_text = "Bonjour IA. Je m'appelle Jean. Je suis ingénieur en CVC. Mon bâtiment actuel a un problème de surchauffe au 3ème étage. La climatisation est une pompe à chaleur air-eau. Que dois-je vérifier en premier ?"
words = long_text.split()

st.subheader("Ce que l'IA 'voit' avant de répondre :")
if context_size < len(words):
    forgotten_text = " ".join(words[:-context_size])
    remembered_text = " ".join(words[-context_size:])
    
    st.markdown(f"<span style='color:grey; text-decoration:line-through;'>{forgotten_text}</span> <span style='background-color:#E6F3FF; font-weight:bold; padding:2px;'>{remembered_text}</span>", unsafe_allow_html=True)
    st.warning(f"⚠️ La fenêtre de contexte est trop petite. L'IA a oublié le début (dont votre prénom et votre métier !).")
    
    if st.button("Générer la réponse (Output) 🔴"):
        st.info("Output : Vous devriez vérifier les paramètres de votre pompe à chaleur air-eau ou les vannes du 3ème étage. (Note: l'IA a oublié que vous étiez ingénieur, sa réponse risque d'être trop basique).")
else:
    st.markdown(f"<span style='background-color:#E6F3FF; font-weight:bold; padding:2px;'>{long_text}</span>", unsafe_allow_html=True)
    st.success("✅ Le texte entier rentre dans la fenêtre de contexte. L'IA a toutes les informations.")
    
    if st.button("Générer la réponse (Output) 🟢"):
        st.info("Output : Bonjour Jean, en tant qu'ingénieur CVC, vous savez que pour votre PAC air-eau, il faut vérifier le débit d'eau froide vers les terminaux du 3ème étage et la consigne de la régulation de zone.")

st.divider()

# --- SECTION 3 : CAPACITÉ DE RAISONNEMENT ---
st.header("⚙️ 3. Capacité de Raisonnement (Chain of Thought)")
st.write("Les modèles modernes ne se contentent pas de deviner le mot suivant. On leur apprend à **réfléchir étape par étape** avant de donner la réponse finale (Output).")

problem = "Un ascenseur peut porter 800 kg. Chaque personne pèse en moyenne 75 kg, et il y a déjà 3 personnes dedans. Il y a un colis de 200 kg. Combien de personnes supplémentaires peuvent entrer ?"

st.write("**Problème posé à l'IA :**")
st.info(problem)

reasoning_mode = st.radio("Comment l'IA doit-elle traiter le problème ?", ["Réponse directe (Risque d'erreur)", "Réflexion étape par étape (Raisonnement actif)"])

if st.button("Lancer l'analyse"):
    if reasoning_mode == "Réponse directe (Risque d'erreur)":
        with st.spinner("Génération de l'output..."):
            time.sleep(1)
        st.error("**Output direct :** L'ascenseur peut encore prendre 4 personnes.")
        st.write("*(L'IA a répondu trop vite sans faire les calculs intermédiaires, ce qui mène souvent à des hallucinations ou des erreurs).*")
    else:
        with st.status("L'IA réfléchit...", expanded=True) as status:
            st.write("📝 **Étape 1 :** Capacité totale = 800 kg.")
            time.sleep(1)
            st.write("📝 **Étape 2 :** Poids actuel des 3 personnes = 3 * 75 kg = 225 kg.")
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
st.caption("Développé pour illustrer les concepts de base de l'Intelligence Artificielle générative.")
