from flask import Flask, render_template

app = Flask(__name__)

# Chemin vers la page de login (page principale)
@app.route('/')
def login():
    # Code pour la page de login (pas encore implémenté)
    return render_template('login.html')

# Chemin vers la page principale
@app.route('/index')
def index():
    # Code pour la page principale avec la barre latérale gauche et les mini-jeux (pas encore implémenté)
    return render_template('left_menu.html')

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
