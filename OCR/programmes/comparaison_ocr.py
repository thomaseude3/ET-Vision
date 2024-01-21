def comparer_listes_types(liste1, liste2):
    # Fonction pour supprimer les espaces, les tirets et les barres obliques
    def nettoyer_chaine(chaine):
        return chaine.replace(" ", "").replace("-", "").replace("/", "").replace("—", "").replace("'", "").replace("‘", "").replace("-", "")

    # Appliquer la fonction de nettoyage et comparer les chaînes nettoyées
    chaine1 = nettoyer_chaine(liste1[0])
    chaine2 = nettoyer_chaine(liste2[0])

    # Comparer les chaînes nettoyées
    if chaine1 == chaine2:
        return "Les deux types sont identiques."
    else:
        # Trouver les différences entre les deux chaînes
        differences = []
        for i, (c1, c2) in enumerate(zip(chaine1, chaine2)):
            if c1 != c2:
                differences.append(f"Position {i + 1}: '{c1}' dans le produit, '{c2}' dans l'étiquette.")

        if differences:
            return "Différences trouvées entre les types:\n" + "\n".join(differences)
        else:
            return "Aucune différence trouvée."

def comparer_listes_refs(liste1, liste2):
    # Fonction pour supprimer les espaces, les tirets et les barres obliques
    def nettoyer_chaine(chaine):
        return chaine.replace(" ", "").replace("-", "").replace("/", "").replace("—", "").replace("'", "").replace("‘", "").replace("-", "")

    # Appliquer la fonction de nettoyage et comparer les chaînes nettoyées
    chaine1 = nettoyer_chaine(liste1[0])
    chaine2 = nettoyer_chaine(liste2[0])

    # Comparer les chaînes nettoyées
    if chaine1 == chaine2:
        return "Les deux références sont identiques."
    else:
        # Trouver les différences entre les deux chaînes
        differences = []
        for i, (c1, c2) in enumerate(zip(chaine1, chaine2)):
            if c1 != c2:
                differences.append(f"Position {i + 1}: '{c1}' dans l'étiquette', '{c2}' dans le produit.")

        if differences:
            return "Différences trouvées entre les références:\n" + "\n".join(differences)
        else:
            return "Aucune différence trouvée."