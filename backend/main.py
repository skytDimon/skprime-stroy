import os
import httpx
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "")
TELEGRAM_PROXY = os.getenv("TELEGRAM_PROXY")
TELEGRAM_API_URL = os.getenv("TELEGRAM_API_URL", "https://api.telegram.org")


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
    otherDetails: str = ""


async def send_telegram_notification(form: ContactForm):
    print(f"DEBUG: Starting telegram sending for {form.name}...")
    if not TELEGRAM_BOT_TOKEN:
        print("DEBUG: NO BOT TOKEN")
        return

    chat_ids = [chat_id.strip() for chat_id in TELEGRAM_CHAT_IDS.split(",") if chat_id.strip()]
    print(f"DEBUG: Found chat_ids: {chat_ids}")
    if not chat_ids:
        print("DEBUG: NO CHAT IDS CONFIGURED")
        return
        
    object_type_mapping = {
        "industrial": "Промышленное здание",
        "administrative": "Административное здание",
        "warehouse": "Складской комплекс",
        "infrastructure": "Инженерная инфраструктура",
        "turnkey": "Возведение «под ключ»",
        "special_works": "Отдельные виды работ",
        "other": "Другое"
    }
    
    russian_object_type = object_type_mapping.get(form.objectType, form.objectType)
    
    text = (
        "🏗 <b>Новая заявка с сайта ПРАЙМ-СТРОЙ</b>\n\n"
        f"👤 <b>Имя:</b> {form.name}\n"
        f"📞 <b>Телефон:</b> {form.phone}\n"
        f"🏭 <b>Что нужно:</b> {russian_object_type}"
    )
    
    if form.otherDetails:
        text += f"\n📝 <b>Доп. информация:</b> {form.otherDetails}"

    url = f"{TELEGRAM_API_URL}/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    client_options = {"timeout": 15.0}
    if TELEGRAM_PROXY:
        client_options["proxy"] = TELEGRAM_PROXY
        print(f"DEBUG: Using proxy {TELEGRAM_PROXY}")
    
    async with httpx.AsyncClient(**client_options) as client:
        for chat_id in chat_ids:
            try:
                response = await client.post(
                    url,
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "HTML"
                    }
                )
                print(f"Telegram sent to {chat_id}, status: {response.status_code}, response: {response.text}")
            except Exception as e:
                print(f"Failed to send telegram to {chat_id}: {e}")
        
        print("DEBUG: Finished processing all chat_ids")


@app.post("/api/contact")
async def submit_contact(form: ContactForm, background_tasks: BackgroundTasks):
    print(f"[ЗАЯВКА] {form.name} | {form.phone} | {form.objectType}")
    
    background_tasks.add_task(send_telegram_notification, form)
    
    return {"status": "ok", "message": "Заявка принята. Мы свяжемся с вами в течение одного рабочего дня."}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
