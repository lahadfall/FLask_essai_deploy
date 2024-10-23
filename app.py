from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # Création de bd et de notre première Table
from datetime import datetime    # pour avoir la date de création d'une table

# Création d'instance
app = Flask(__name__)


# Renseigner l'url de notre bd càd oû se trouve notre bd puis créer la
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# création d'une table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_creation = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.utcnow)
    
    def __repr__(self):      
        return f"Todo: {self.name}"
    
'''
Création de données à partir d'un interpréteur python:
from app import db
from app import Task
db.create_all()                 # créer des tables 
task = Task(name= "Flask")      
db.session.add(task)            # ajout de la table dans la db
db.session.commit()             # enregistrer
task = Task.query.all()         # lire la table crée
'''


# Les route ou url en Diango
@app.route("/", methods = ["GET","POST"]) # ça sera notre page d'accueille
def index():
    if request.method == "POST":
        name = request.form['name']
        new_task = Task(name=name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produit"
    else:
        tasks = Task.query.order_by(Task.date_creation)
    return render_template("flask.html", tasks=tasks)

@app.route("/delete/<int:id>/")
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Une erreur s'est produite"
    
@app.route("/update/<int:id>/", methods=["GET","POST"])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Nous ne pouvons pas modifier cette tache"
    else:
        title = "Mise à jour"
        return render_template("update.html", title=title, task=task)

# Notre Deuxième page
@app.route("/A_propos/")
def A_propos():   
    return render_template("A_propos.html")

#On lance l'application
if __name__ == "__main__":
    app.run(debug=True)
    
