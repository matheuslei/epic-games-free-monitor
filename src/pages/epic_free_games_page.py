from playwright.sync_api import Page
from dateutil import parser, tz
from datetime import timedelta
from src.services.workflow_service import WorkflowService

class EpicFreeGamesPage:
    def __init__(self, page: Page):
        self.page = page

    def go_to_free_games(self, url):
        print(f"Acessando {url} ...")
        self.page.goto(url, timeout=60000)
        print(f"Título da página: {self.page.title()}")

    def get_free_game_cards(self):
        print("Aguardando carregamento dos elementos...")
        try:
            # Wait for at least one "Grátis -" span
            self.page.locator('div').filter(has=self.page.locator('span', has_text="Grátis -")).first.wait_for(state="visible", timeout=15000)
        except Exception as e:
            print(f"Não foi possível encontrar o elemento com texto 'Grátis -'. Erro: {e}")
            return []

        # Find spans with "Grátis -"
        spans = self.page.locator('span', has_text="Grátis -")
        count = spans.count()
        print(f"Elementos de tempo 'Grátis -' encontrados: {count}")
        
        games = []
        for i in range(count):
            span = spans.nth(i)
            card_container = self._find_card_container(span)
            
            if card_container and card_container.locator('h6').count() > 0:
                title = card_container.locator('h6').first.inner_text()
                availability = span.inner_text()
                
                # Check for expiration to update schedule AND fix visual time
                # Returns the corrected text if successful, or None
                corrected_text = self._check_expiration(span)
                
                if corrected_text:
                    availability = corrected_text
                
                games.append({
                    'title': title,
                    'availability': availability,
                    'card_element': card_container,
                    'index': i
                })
        
        return games

    def _find_card_container(self, span):
        # Strategy: span -> ... -> div[data-component="VaultOfferCard"] OR 'a' tag
        card = span.locator('xpath=ancestor::div[@data-component="VaultOfferCard"]')
        if card.count() == 0:
            card = span.locator('xpath=ancestor::a')
        if card.count() == 0:
            card = span.locator('xpath=../..') # Fallback
        return card

    def _check_expiration(self, span):
        try:
            time_element = span.locator('time').first
            if time_element.count() > 0:
                datetime_str = time_element.get_attribute('datetime')
                print(f"DEBUG - Datetime original do HTML: {datetime_str}")
                if datetime_str:
                    end_date = parser.isoparse(datetime_str)
                    
                    # --- FIX VISUAL TIME FOR SCREENSHOT ---
                    # Ensure end_date is UTC aware
                    if end_date.tzinfo is None:
                        end_date = end_date.replace(tzinfo=tz.tzutc())
                    
                    # Convert to Sao Paulo time
                    to_zone = tz.gettz('America/Sao_Paulo')
                    brt_date = end_date.astimezone(to_zone)
                    
                    months = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."]
                    day = brt_date.day
                    month = months[brt_date.month - 1]
                    hour = brt_date.strftime("%H:%M")
                    
                    # Construct the visual text dynamically based on the REAL converted time
                    new_text = f"{day} de {month} às {hour}"
                    
                    # Execute JS to update the DOM
                    # Update the PARENT span to ensure clean text replacement
                    full_text = f"Grátis - {new_text}"
                    
                    span.evaluate(f"el => el.innerText = '{full_text}'")
                    
                    print(f"Horário visual corrigido para: {full_text}")
                    # --------------------------------------

                    next_run = end_date + timedelta(minutes=10)
                    print(f"Data de expiração detectada: {end_date}")
                    WorkflowService.update_schedule(next_run)
                    
                    return full_text
        except Exception as e:
            print(f"Erro ao calcular próximo agendamento: {e}")
        
        return None

    def take_screenshot(self, card_element, index):
        filename = f"game_screenshot_{index}.png"
        try:
            # Scroll to element to trigger lazy loading
            card_element.scroll_into_view_if_needed()
            
            # Wait for image inside the card to load
            # Assuming there's an img tag. We wait for it to be visible and have a src.
            try:
                img = card_element.locator('img').first
                img.wait_for(state="visible", timeout=5000)
                # Small delay to ensure rendering is complete
                self.page.wait_for_timeout(2000)
            except:
                print("Aviso: Imagem do jogo não detectada ou demorou para carregar.")

            card_element.screenshot(path=filename)
            print(f"Screenshot salvo: {filename}")
            return filename
        except Exception as e:
            print(f"Erro ao tirar screenshot: {e}")
            return None
