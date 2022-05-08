from fastapi import FastAPI
from app.core import config #Importamos la configuración
from app.products import router as product_router #Importamos el archivo router de products y le ponemos un
#apodo para que no se confunda con los archivos router.py de otros modulos (user, orders, etc.)
from app.user import router as user_router
from app.auth import router as auth_router
from app.database import models #Aqui importamos todos lod modelos para que asi Alembic no nos genere errores
#mas adelante
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "Mi App", version = "0.0.1") #Creamos la app instanciando FastAPI, como siempre, y
#le ponemos los metadatos que queramos (buscar que otros metadatos podemos poner.....)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(product_router.api_router)
app.include_router(user_router.api_router)
app.include_router(auth_router.api_router)





