# chatbot.py
# Logique principale du chatbot IA avec memoire de conversation.
# Utilise Mistral AI (gratuit)
# Compatible Python 3.6+

import os
from mistralai import Mistral
from dotenv import load_dotenv
from memory import MemoireConversation

# Charger la cle API depuis le fichier .env
load_dotenv()

# Initialiser le client Mistral
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Personnalite du chatbot
PERSONNALITE = """
Tu es un assistant pedagogique pour lyceens en specialite NSI
(Numerique et Sciences Informatiques).
Tu expliques les concepts informatiques de facon claire et simple,
avec des exemples concrets adaptes au programme de Terminale NSI.
Tu utilises un ton encourage et bienveillant.
Tu reponds toujours en francais.
"""


def verifier_cle_api():
    """
    Verifie que la cle API Mistral est bien configuree.
    """
    cle = os.getenv("MISTRAL_API_KEY")
    if not cle:
        print("ERREUR : Cle API Mistral manquante !")
        print("Cree un fichier .env a la racine du projet avec :")
        print("MISTRAL_API_KEY=ta-cle-api-ici")
        return False
    print("Cle API Mistral detectee avec succes.")
    return True


def chat(message, memoire):
    """
    Envoie un message au modele Mistral et retourne la reponse.

    Parametres
    ----------
    message : str
                Le message de l utilisateur
    memoire : MemoireConversation
                L objet qui gere l historique de conversation

    Retour
    ------
    str : La reponse du modele, ou un message d erreur
    """
    # Ajouter le message de l utilisateur a la memoire
    memoire.ajouter_message("user", message)

    try:
        # Appel a l API Mistral avec l historique complet
        reponse = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": PERSONNALITE},
            ] + memoire.obtenir_historique()
        )

        # Extraire le texte de la reponse
        reponse_texte = reponse.choices[0].message.content

        # Sauvegarder la reponse dans la memoire
        memoire.ajouter_message("assistant", reponse_texte)

        return reponse_texte

    except Exception as e:
        # Retirer le dernier message utilisateur en cas d erreur
        memoire.historique.pop()
        return "Erreur lors de l appel API : {}".format(str(e))


def chat_en_boucle():
    """
    Lance une conversation interactive dans le terminal.
    Tapez 'quitter' pour arreter, 'reset' pour reinitialiser.
    """
    print("\n" + "="*50)
    print("  Chatbot NSI - Assistant IA (Mistral)")
    print("  Tapez 'quitter' pour arreter")
    print("  Tapez 'reset' pour reinitialiser la conversation")
    print("  Tapez 'stats' pour voir les statistiques")
    print("="*50 + "\n")

    # Verifier la cle API avant de demarrer
    if not verifier_cle_api():
        return

    memoire = MemoireConversation(taille_max=10)

    while True:
        try:
            message = input("Vous : ").strip()
        except KeyboardInterrupt:
            print("\nAu revoir !")
            break

        if not message:
            continue

        if message.lower() == "quitter":
            print("Au revoir !")
            break

        if message.lower() == "reset":
            memoire.reinitialiser()
            continue

        if message.lower() == "stats":
            stats = memoire.resume_stats()
            print("\nStatistiques de la conversation :")
            for cle, valeur in stats.items():
                print("   {} : {}".format(cle, valeur))
            print()
            continue

        print("\nAssistant : ", end="", flush=True)
        reponse = chat(message, memoire)
        print(reponse)
        print()


# Test rapide : python3 src/chatbot.py
if __name__ == "__main__":
    chat_en_boucle()
