from flask import Flask, render_template

app = Flask(__name__)

# Chemin vers la page de login
@app.route('/login')
def login():
    # Code pour la page de login (pas encore implémenté)
    return "Page de login"

# Chemin vers la page principale
@app.route('/')
def index():
    # Code pour la page principale avec la barre latérale gauche et les mini-jeux (pas encore implémenté)
    return "Page principale avec barre latérale gauche et mini-jeux"

# Chemin vers le jeu "Trouver joueurs avec image"
@app.route('/jeu/trouver-joueurs-avec-image')
def jeu_trouver_joueurs_avec_image():
    # Code pour le jeu "Trouver joueurs avec image" (pas encore implémenté)
    return "Jeu Trouver joueurs avec image"

# Chemin vers le jeu "Parcours de club"
@app.route('/jeu/parcours-de-club')
def jeu_parcours_de_club():
    # Code pour le jeu "Parcours de club" (pas encore implémenté)
    return "Jeu Parcours de club"

# Chemin vers le jeu "Composition équipe"
@app.route('/jeu/composition-equipe')
def jeu_composition_equipe():
    # Code pour le jeu "Composition équipe" (pas encore implémenté)
    return "Jeu Composition équipe"

if __name__ == '__main__':
    app.run(debug=True)
