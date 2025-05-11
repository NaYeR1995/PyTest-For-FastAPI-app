from fastapi import FastAPI
from contextlib import asynccontextmanager
from identity_service.routes.general_router import general_router
from identity_service.routes.user_router import user_router
from identity_service.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    print(f"{settings.TESTING_MODE}")
    yield
    print("Application shutdown")




app = FastAPI(lifespan=lifespan)
@app.get('/')
def home():
    return{"message": "Welcome at Our App!"}


app.include_router(router=general_router)
app.include_router(router=user_router)