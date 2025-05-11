from fastapi import APIRouter
from identity_service.routes.depn import SessionDep
from identity_service.services.general import health_check

general_router = APIRouter(tags=["General"])


@general_router.get('/health', status_code=200)
async def get_health(db:SessionDep):
    return await health_check(db)
                