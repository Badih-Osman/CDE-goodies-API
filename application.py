import sqlite3

from flask import Flask, jsonify, request

from base_de_donnees import NOM_BASE_DE_DONNEES

application = Flask(__name__)
CLE_API_CDE = "osman"

def obtenir_connexion_bdd():
    connexion = sqlite3.connect(NOM_BASE_DE_DONNEES)
    connexion.row_factory = sqlite3.Row
    return connexion

def est_membre_cde():
    return request.headers.get("X-Cle-API") == CLE_API_CDE

def valider_champs(donnees):
    if "nom" in donnees:
        if not isinstance(donnees["nom"], str) or donnees["nom"].strip() == "":
            return "Le nom doit etre une chaine de caracteres non vide."

    if "prix" in donnees:
        prix = donnees["prix"]
        if not isinstance(prix, int) or isinstance(prix, bool) or prix < 0:
            return "Le prix doit etre un entier positif (en centimes d'euro)."

    for champ in ("photo", "club"):
        if champ in donnees and donnees[champ] is not None:
            if not isinstance(donnees[champ], str):
                return champ + " doit etre une chaine de caracteres."

    return None

@application.route("/api/objets", methods=["GET"])
def lister_objets():
    connexion = obtenir_connexion_bdd()
    lignes = connexion.execute("SELECT * FROM objets").fetchall()
    connexion.close()

    objets = [dict(ligne) for ligne in lignes]
    return jsonify(objets), 200

@application.route("/api/objets/<int:identifiant_objet>", methods=["GET"])
def obtenir_objet(identifiant_objet):
    connexion = obtenir_connexion_bdd()
    ligne = connexion.execute(
        "SELECT * FROM objets WHERE id = ?", (identifiant_objet,)
    ).fetchone()
    connexion.close()

    if ligne is None:
        return jsonify({"erreur": "Objet introuvable."}), 404

    return jsonify(dict(ligne)), 200

@application.route("/api/objets", methods=["POST"])
def creer_objet():
    if not est_membre_cde():
        return jsonify({"erreur": "Seuls les membres du CDE peuvent modifier le catalogue."}), 401

    donnees = request.get_json(silent=True)
    if not isinstance(donnees, dict):
        return jsonify({"erreur": "Le corps de la requete doit etre un objet JSON."}), 400
    if "nom" not in donnees or "prix" not in donnees:
        return jsonify({"erreur": "Les champs nom et prix sont obligatoires."}), 400

    erreur = valider_champs(donnees)
    if erreur:
        return jsonify({"erreur": erreur}), 400

    connexion = obtenir_connexion_bdd()
    curseur = connexion.execute(
        "INSERT INTO objets (nom, photo, prix, club) VALUES (?, ?, ?, ?)",
        (donnees["nom"], donnees.get("photo"), donnees["prix"], donnees.get("club")),
    )
    connexion.commit()
    nouvel_identifiant = curseur.lastrowid

    ligne = connexion.execute(
        "SELECT * FROM objets WHERE id = ?", (nouvel_identifiant,)
    ).fetchone()
    connexion.close()

    return jsonify(dict(ligne)), 201

@application.route("/api/objets/<int:identifiant_objet>", methods=["PATCH"])
def modifier_objet(identifiant_objet):
    if not est_membre_cde():
        return jsonify({"erreur": "Seuls les membres du CDE peuvent modifier le catalogue."}), 401

    donnees = request.get_json(silent=True)
    if not isinstance(donnees, dict):
        return jsonify({"erreur": "Le corps de la requete doit etre un objet JSON."}), 400
    champs_autorises = ["nom", "photo", "prix", "club"]
    if not any(champ in donnees for champ in champs_autorises):
        return jsonify({"erreur": "Fournissez au moins un champ parmi : nom, photo, prix, club."}), 400

    erreur = valider_champs(donnees)
    if erreur:
        return jsonify({"erreur": erreur}), 400

    connexion = obtenir_connexion_bdd()
    ligne = connexion.execute(
        "SELECT * FROM objets WHERE id = ?", (identifiant_objet,)
    ).fetchone()

    if ligne is None:
        connexion.close()
        return jsonify({"erreur": "Objet introuvable."}), 404
    nom = donnees.get("nom", ligne["nom"])
    photo = donnees.get("photo", ligne["photo"])
    prix = donnees.get("prix", ligne["prix"])
    club = donnees.get("club", ligne["club"])

    connexion.execute(
        "UPDATE objets SET nom = ?, photo = ?, prix = ?, club = ? WHERE id = ?",
        (nom, photo, prix, club, identifiant_objet),
    )
    connexion.commit()

    ligne_modifiee = connexion.execute(
        "SELECT * FROM objets WHERE id = ?", (identifiant_objet,)
    ).fetchone()
    connexion.close()

    return jsonify(dict(ligne_modifiee)), 200

@application.route("/api/objets/<int:identifiant_objet>", methods=["DELETE"])
def supprimer_objet(identifiant_objet):
    if not est_membre_cde():
        return jsonify({"erreur": "Seuls les membres du CDE peuvent modifier le catalogue."}), 401

    connexion = obtenir_connexion_bdd()
    ligne = connexion.execute(
        "SELECT * FROM objets WHERE id = ?", (identifiant_objet,)
    ).fetchone()

    if ligne is None:
        connexion.close()
        return jsonify({"erreur": "Objet introuvable."}), 404

    connexion.execute("DELETE FROM objets WHERE id = ?", (identifiant_objet,))
    connexion.commit()
    connexion.close()
    return "", 204

if __name__ == "__main__":
    application.run(debug=True)
