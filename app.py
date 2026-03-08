import os
from dotenv import load_dotenv
# ... otros imports ...
from flask import Flask, render_template, request, redirect, url_for
from sqlmodel import Session, select
from database import engine, crear_db
from models import Inscrito

# Crear DB al arrancar
crear_db()

app = Flask(__name__)

# Cargar variables del archivo .env
load_dotenv()

# --- RUTAS ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/evento")
def evento():
    return render_template("evento.html")

@app.route("/galeria")
def galeria():
    api_key = os.environ.get("GOOGLE_API_KEY")
    folder_id = os.environ.get("GOOGLE_FOLDER_ID")
    return render_template("galeria.html", api_key=api_key, folder_id=folder_id)

@app.route("/inscripcion")
def inscripcion_view():
    return render_template("inscripcion.html")

@app.route("/inscribir", methods=["POST"])
def inscribir():
    nuevo = Inscrito(
        nombre=request.form["nombre"],
        email=request.form["email"],
        telefono=request.form["telefono"],
        asistencia=request.form["asistencia"],
        mensaje=request.form.get("mensaje")
    )
    with Session(engine) as session:
        session.add(nuevo)
        session.commit()
    return redirect(url_for('inscripcion_view', msg='gracias'))

@app.route("/admin")
def admin():
    with Session(engine) as session:
        inscritos = session.exec(select(Inscrito)).all()
    return render_template("admin.html", inscritos=inscritos)

if __name__ == "__main__":
    app.run()