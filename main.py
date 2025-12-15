import sys
from playwright.sync_api import sync_playwright
from src.config import Config
from src.services.email_service import EmailService
from src.services.state_service import StateService
from src.pages.epic_free_games_page import EpicFreeGamesPage

def main():
    with sync_playwright() as p:
        print("Iniciando browser...")
        browser = p.chromium.launch(
            headless=Config.HEADLESS, 
            args=['--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent=Config.USER_AGENT,
            viewport=Config.VIEWPORT,
            locale=Config.LOCALE,
            timezone_id=Config.TIMEZONE,
            geolocation={'latitude': -23.5505, 'longitude': -46.6333}, # São Paulo
            permissions=['geolocation']
        )
        page = context.new_page()
        
        epic_page = EpicFreeGamesPage(page)
        
        try:
            # Load state
            last_checked_games = StateService.get_last_processed_games()
            
            epic_page.go_to_free_games(Config.EPIC_GAMES_URL)
            found_games = epic_page.get_free_game_cards()
            
            if not found_games:
                print("Nenhum jogo grátis encontrado com o padrão esperado.")
                sys.exit(0)

            current_game_titles = []
            for game in found_games:
                title = game['title']
                availability = game['availability']
                current_game_titles.append(title)
                
                print(f"Jogo encontrado: {title}")
                print(f"Disponibilidade: {availability}")
                
                if title not in last_checked_games:
                    screenshot_path = epic_page.take_screenshot(game['card_element'], game['index'])
                    
                    print(f"Enviando notificação para: {title}")
                    EmailService.send_notification(title, availability, screenshot_path)
                else:
                    print(f"O jogo '{title}' já foi notificado anteriormente.")

            # Save state
            StateService.save_current_games(current_game_titles)

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == '__main__':
    main()
