import os
from src.config import Config

class StateService:
    @staticmethod
    def get_last_processed_games():
        """
        Reads the last processed games from file or environment variable.
        Returns a set of game titles.
        """
        last_checked = set()
        
        # Try to read from file first
        if os.path.exists('last_game.txt'):
            try:
                with open('last_game.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        # Assuming games are separated by " | "
                        last_checked.update(content.split(" | "))
                print(f"Jogos verificados anteriormente (arquivo): {last_checked}")
            except Exception as e:
                print(f"Erro ao ler last_game.txt: {e}")
        
        # Fallback to env var if file is empty/missing
        if not last_checked:
            env_last = os.getenv('LAST_CHECKED_GAME', '')
            if env_last:
                last_checked.add(env_last)
                print(f"Jogos verificados anteriormente (env): {last_checked}")
                
        return last_checked

    @staticmethod
    def save_current_games(games_list):
        """
        Saves the current list of games to file.
        games_list: list of game titles
        """
        try:
            content = " | ".join(games_list)
            with open('last_game.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Output for GitHub Actions
            if os.getenv('GITHUB_OUTPUT'):
                with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                    f.write(f"current_game={content}\n")
        except Exception as e:
            print(f"Erro ao salvar estado dos jogos: {e}")
