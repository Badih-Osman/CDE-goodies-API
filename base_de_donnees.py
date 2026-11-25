import sqlite3

NOM_BASE_DE_DONNEES = "cde.db"

def creer_base_de_donnees():
    connexion = sqlite3.connect(NOM_BASE_DE_DONNEES)
    curseur = connexion.cursor()
    curseur.execute(
        """
        CREATE TABLE IF NOT EXISTS objets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            photo TEXT,
            prix INTEGER NOT NULL,
            club TEXT
        )
        """
    )
    curseur.execute("SELECT COUNT(*) FROM objets")
    nombre_objets = curseur.fetchone()[0]

    if nombre_objets == 0:
        exemples = [
            ("Sweat a capuche de Polytech Nancy", "https://example.com/hoodie.png", 3500, None),
            ("Autocollant Montagne", "https://example.com/sticker.png", 200, "Club Montagne"),
            ("Sac en toile du Club Photo", "https://example.com/tote.png", 800, "Club Photographie"),
        ]
        curseur.executemany(
            "INSERT INTO objets (nom, photo, prix, club) VALUES (?, ?, ?, ?)",
            exemples,
        )

    connexion.commit()
    connexion.close()
    print("La base de donnees '" + NOM_BASE_DE_DONNEES + "' est prete.")

if __name__ == "__main__":
    creer_base_de_donnees()
