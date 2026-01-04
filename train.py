import asyncio
from playwright.async_api import async_playwright

# Этот скрипт мы запускаем РУКАМИ один раз, чтобы получить "паспорт"
async def train_session():
    print("[*] Запуск Тренировки...")
    async with async_playwright() as p:
        # Запускаем браузер в ВИДИМОМ режиме
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
             # Используем реальный User-Agent
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("[!] ВНИМАНИЕ: Сейчас откроется браузер.")
        print("[!] Твоя задача: ВРУЧНУЮ решить капчу (пазл) и принять куки на сайте.")
        print("[!] У тебя есть 60 секунд.")

        try:
            await page.goto("https://www.leboncoin.fr/recherche?text=ford%20fiesta", timeout=60000)

            # Ждем, пока ты решишь все проблемы руками.
            # Я ставлю большую задержку, чтобы ты не спешил.
            await page.wait_for_timeout(60000)

            print("[*] Время вышло. Сохраняем сессию...")

            # ГЛАВНАЯ МАГИЯ: Сохраняем все куки и хранилище в файл
            await context.storage_state(path="session.json")
            print("[+] Сессия успешно сохранена в файл 'session.json'!")

        except Exception as e:
            print(f"[-] Ошибка во время тренировки: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(train_session())
    except KeyboardInterrupt:
        pass
