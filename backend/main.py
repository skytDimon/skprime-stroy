from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="ПРАЙМ-СТРОЙ API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactForm(BaseModel):
    name: str
    phone: str
    objectType: str


@app.post("/api/contact")
async def submit_contact(form: ContactForm):
    # TODO: подключить отправку на почту / в CRM
    print(f"[ЗАЯВКА] {form.name} | {form.phone} | {form.objectType}")
    return {"status": "ok", "message": "Заявка принята. Мы свяжемся с вами в течение одного рабочего дня."}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
