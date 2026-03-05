from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import engine, crear_db
from models import Inscrito

crear_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- RUTAS DE NAVEGACIÓN ---

# 1. Inicio
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 2. Página del Evento (Detalles)
@app.get("/evento")
async def evento(request: Request):
    return templates.TemplateResponse("evento.html", {"request": request})

# 3. Galería de Fotos
@app.get("/galeria")
async def galeria(request: Request):
    return templates.TemplateResponse("galeria.html", {"request": request})

# 4. Inscripción
@app.get("/inscripcion")
async def inscripcion_view(request: Request):
    return templates.TemplateResponse("inscripcion.html", {"request": request})

# --- LÓGICA DEL FORMULARIO ---

@app.post("/inscribir")
async def inscribir(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    asistencia: str = Form(...),
    mensaje: str = Form(None)
):
    with Session(engine) as session:
        nuevo = Inscrito(
            nombre=nombre, email=email, telefono=telefono, 
            asistencia=asistencia, mensaje=mensaje
        )
        session.add(nuevo)
        session.commit()
    
    # Redirige a la página de inscripción con mensaje de éxito
    return RedirectResponse(url="/inscripcion?msg=gracias", status_code=303)

# --- PANEL ADMIN ---
@app.get("/admin")
async def admin(request: Request):
    with Session(engine) as session:
        resultados = session.exec(select(Inscrito)).all()
    return templates.TemplateResponse("admin.html", {"request": request, "inscritos": resultados})