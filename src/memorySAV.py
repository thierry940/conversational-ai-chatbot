# memory.py
# Gestion de la memoire de conversation pour le chatbot IA.
# Compatible Python 3.6+

class MemoireConversation:

    def __init__(self, taille_max=10):
        self.historique = []
        self.taille_max = taille_max
        self.nombre_messages_total = 0

    def ajouter_message(self, role, contenu):
        if role not in ("user", "assistant"):
            raise ValueError("Role invalide : utiliser 'user' ou 'assistant'.")
        if not contenu or not contenu.strip():
            raise ValueError("Le contenu du message ne peut pas etre vide.")

        self.historique.append({
            "role": role,
            "content": contenu.strip()
        })
        self.nombre_messages_total += 1

        # Supprimer les messages les plus anciens si depassement
        if len(self.historique) > self.taille_max:
            self.historique = self.historique[-self.taille_max:]

    def obtenir_historique(self):
        return list(self.historique)

    def reinitialiser(self):
        self.historique = []
        print("Conversation reinitialisee.")

    def nombre_messages(self):
        return len(self.historique)

    def est_vide(self):
        return len(self.historique) == 0

    def dernier_message(self):
        if self.est_vide():
            return None
        return self.historique[-1]

    def messages_par_role(self, role):
        return [msg for msg in self.historique if msg["role"] == role]

    def afficher_historique(self):
        if self.est_vide():
            print("Historique vide.")
            return

        print("\n" + "="*50)
        print("Historique ({} messages)".format(self.nombre_messages()))
        print("="*50)
        for i, msg in enumerate(self.historique, 1):
            role_label = "User" if msg["role"] == "user" else "Assistant"
            print("\n[{}] {} :".format(i, role_label))
            contenu = msg["content"]
            print("    " + (contenu[:100] + "..." if len(contenu) > 100 else contenu))
        print("\n" + "="*50 + "\n")

    def resume_stats(self):
        return {
            "messages_en_memoire":  self.nombre_messages(),
            "messages_total":       self.nombre_messages_total,
            "messages_utilisateur": len(self.messages_par_role("user")),
            "messages_assistant":   len(self.messages_par_role("assistant")),
            "taille_max":           self.taille_max,
        }

    def __repr__(self):
        return "MemoireConversation(messages={}, taille_max={})".format(
            self.nombre_messages(), self.taille_max
        )


# Test rapide : python3 src/memory.py
if __name__ == "__main__":

    print("Test de la classe MemoireConversation\n")

    memoire = MemoireConversation(taille_max=6)

    memoire.ajouter_message("user",      "Qu est-ce qu un arbre binaire ?")
    memoire.ajouter_message("assistant", "Un arbre binaire est une structure de donnees...")
    memoire.ajouter_message("user",      "Quelle est sa complexite de recherche ?")
    memoire.ajouter_message("assistant", "La complexite est O(log n) en moyenne...")
    memoire.ajouter_message("user",      "Et pour un arbre degenere ?")
    memoire.ajouter_message("assistant", "Dans le pire cas, elle devient O(n)...")

    memoire.afficher_historique()

    print("Statistiques :")
    for cle, valeur in memoire.resume_stats().items():
        print("   {} : {}".format(cle, valeur))

    print("\nAjout d un 7eme message (taille_max=6)...")
    memoire.ajouter_message("user", "Merci pour ces explications !")
    print("   Messages en memoire : {} (le plus ancien supprime)".format(
        memoire.nombre_messages()
    ))

    print("\nReinitialisation...")
    memoire.reinitialiser()
    print("   Historique vide : {}".format(memoire.est_vide()))
    print("   Repr : {}".format(memoire))
