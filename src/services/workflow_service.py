import os
import re
from src.config import Config

class WorkflowService:
    @staticmethod
    def update_schedule(next_run_dt):
        """
        Updates the cron schedule in the GitHub workflow file.
        """
        workflow_path = Config.WORKFLOW_FILE_PATH
        
        if not os.path.exists(workflow_path):
            print(f"Workflow file not found at {workflow_path}")
            return

        # Minute Hour Day Month *
        cron_exp = f"{next_run_dt.minute} {next_run_dt.hour} {next_run_dt.day} {next_run_dt.month} *"
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Regex to replace the dynamic cron line safely
            # Matches the entire line containing # Dynamic to ensure correct formatting
            # Expected format: - cron: 'M H D M *' # Dynamic
            new_content = re.sub(
                r"(\s*-\s*cron:\s*').*?(' # Dynamic)", 
                f"\\1{cron_exp}\\2", 
                content
            )
            
            if content != new_content:
                with open(workflow_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Agendamento dinâmico atualizado para: {cron_exp} (UTC)")
            else:
                print("O agendamento já está atualizado ou o marcador '# Dynamic' não foi encontrado.")
                
        except Exception as e:
            print(f"Erro ao atualizar workflow: {e}")
