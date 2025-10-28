from fastapi import APIRouter


router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/")
def scrape(cnpj: str):
    return {"cnpj": cnpj}
