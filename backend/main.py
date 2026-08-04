import os
import httpx
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8290958205:AAEEgNb30OJYz2VOgdVipt5P0W_TZLetaBI")
TELEGRAM_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "2117749294,821740830")


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


async def send_telegram_notification(form: ContactForm):
    if not TELEGRAM_BOT_TOKEN:
        return

    chat_ids = [chat_id.strip() for chat_id in TELEGRAM_CHAT_IDS.split(",") if chat_id.strip()]
    
    text = (
        "🏗 <b>Новая заявка с сайта ПРАЙМ-СТРОЙ</b>\n\n"
        f"👤 <b>Имя:</b> {form.name}\n"
        f"📞 <b>Телефон:</b> {form.phone}\n"
        f"🏭 <b>Что нужно:</b> {form.objectType}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        for chat_id in chat_ids:
            try:
                response = await client.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "HTML"
                    },
                    timeout=10.0
                )
                print(f"Telegram sent to {chat_id}, status: {response.status_code}, response: {response.text}")
            except Exception as e:
                print(f"Failed to send telegram to {chat_id}: {e}")


@app.post("/api/contact")
async def submit_contact(form: ContactForm, background_tasks: BackgroundTasks):
    print(f"[ЗАЯВКА] {form.name} | {form.phone} | {form.objectType}")
    
    background_tasks.add_task(send_telegram_notification, form)
    
    return {"status": "ok", "message": "Заявка принята. Мы свяжемся с вами в течение одного рабочего дня."}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
