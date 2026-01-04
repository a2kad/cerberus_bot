import asyncio
import random  # <--- ВОТ ЧЕГО НЕ ХВАТАЛО
from playwright.async_api import async_playwright
import sys

class Cerberus:
    def __init__(self, target_text):
        self.target_text = target_text # Мы ищем текст, а не URL

    async def scout(self):
        print("[*] Запуск теста маскировки (Stealth Audit)...")

        async with async_playwright() as p:
            try:
                # Подключаемся к твоему Chrome
                browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                context = browser.contexts[0]
                page = context.pages[0]

                # Идем на сайт-детектор
                print("[*] Навигация на bot.sannysoft.com...")
                await page.goto("https://bot.sannysoft.com/", timeout=60000)

                await page.wait_for_timeout(3000)

                # Делаем полный скриншот
                print("[*] Делаем снимок отчета...")
                await page.screenshot(path="stealth_report.png", full_page=True)

                print("[+] Отчет сохранен: stealth_report.png")
                print("[*] Проверь файл. Если таблицы зеленые - твой код идеален.")

            except Exception as e:
                print(f"[-] Ошибка: {e}")
            finally:
                print("[*] Тест завершен.")

if __name__ == "__main__":
    TARGET = "Opel Astra"
    bot = Cerberus(TARGET)
    try:
        asyncio.run(bot.scout())
    except KeyboardInterrupt:
        sys.exit()
