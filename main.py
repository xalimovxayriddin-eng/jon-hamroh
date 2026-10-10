import flet as ft
import random
import datetime
from google import genai
from google.genai import types

# API Kalit va Xarakter sozlamalari
GEMINI_API_KEY = "AQ.Ab8RN6JRTyaytO4_ZPMryRvNXDOJSJ2G6Qqj702Pa56xLzLc4g"
client = genai.Client(api_key=GEMINI_API_KEY)

def main(page: ft.Page):
    page.title = "Jon Hamroh"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 650

    # Uyqu va charchoq mantiqi
    page.session.set("is_sleeping", False)
    page.session.set("charchoq", 0)

    # 1. Status matni (Uyg'oq yoki Uxlayotganini ko'rsatadi)
    status_text = ft.Text("😊 JON UYG'OQ", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)

    # 2. Suhbat matni ko'rinadigan joy
    chat_text = ft.Text(
        "Jon: Eshitaman jo'ra, xohlasang gapir, xohlasang yoz!", 
        size=16, text_align=ft.TextAlign.CENTER, width=350
    )

    def process_logic(text_input):
        is_sleeping = page.session.get("is_sleeping")
        charchoq = page.session.get("charchoq")
        hozirgi_vaqt = datetime.datetime.now().strftime("%H:%M")

        config = types.GenerateContentConfig(
            system_instruction=(
                f"Sening isming Jon. Sen 17-18 yoshlardagi oddiy, samimiy va biroz erkatoy o'zbek yigitidursan. "
                f"Hozir soat roppa-rosa {hozirgi_vaqt}. "
                f"Hech qachon ilmiy gapirma, misollar yechma. Suhbatdoshing bilan juda sodda, qisqa va ko'cha tilida gaplash. "
                f"Har doim javoblaring juda qisqa, 1-2 ta gapdan iborat bo'lsin."
            ),
            temperature=0.7,
        )

        if is_sleeping:
            if any(word in text_input.lower() for word in ["tur", "uyg'on", "hey", "tur o'rningdan"]):
                page.session.set("is_sleeping", False)
                page.session.set("charchoq", 0)
                status_text.value = "😊 JON UYG'OQ"
                status_text.color = ft.colors.GREEN
                javob = "Oh! Voy, kechirasiz! Yana uxlab qolibmanmi? 🥱 Kalla ketibdi charchoqdan. Gapiraver jo'ra!"
            else:
                javob = "zzz... xur-pish... mmm... (Jon uxlab yotibdi, uni uyg'otish uchun 'tur' deb yozing)"
        else:
            charchoq += random.randint(20, 35)
            page.session.set("charchoq", charchoq)

            if charchoq >= 100:
                page.session.set("is_sleeping", True)
                status_text.value = "😴 JON UXLAB QOLDI"
                status_text.color = ft.colors.RED
                javob = "Men senga hozir aytmoqchi edimki... nima edi haligi... mmm... uykum kelyapti... zzz..."
            else:
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash', contents=text_input, config=config
                    )
                    javob = response.text
                except Exception as e:
                    javob = f"Xato yuz berdi: {str(e)}"

        chat_text.value = f"Jon: {javob}"
        btn_yuborish.disabled = False
        btn_yuborish.text = "XABAR YUBORISH"
        page.update()

    def button_click(e):
        text = entry_box.value.strip()
        if not text:
            return
        entry_box.value = ""
        btn_yuborish.disabled = True
        btn_yuborish.text = "Jon o'ylamoqda..."
        page.update()
        
        # Alohida oqimda ishga tushirish (Ilova qotib qolmasligi uchun)
        threading.Thread(target=process_logic, args=(text,)).start()

    # 3. Matn kiritish katagi va Tugma
    entry_box = ft.TextField(hint_text="Jonnga biror narsa yozing...", width=350, border_radius=10)
    btn_yuborish = ft.ElevatedButton(
        text="XABAR YUBORISH", width=350, height=50, on_click=button_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    page.add(
        ft.Container(content=status_text, margin=ft.margin.only(top=30, bottom=20)),
        ft.Container(content=chat_text, padding=20, bgcolor=ft.colors.SURFACE_VARIANT, border_radius=15, width=370),
        ft.Container(height=20),
        entry_box,
        ft.Container(height=10),
        btn_yuborish
    )

if __name__ == '__main__':
    ft.app(target=main)
