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
            
            lines = content.splitlines()
            new_lines = []
            updated = False
            
            # Simple line-by-line replacement to avoid regex complexity issues
            for line in lines:
                if '# Dynamic' in line:
                    # If we haven't updated the schedule yet, add the new line
                    if not updated:
                        new_lines.append(f"    - cron: '{cron_exp}' # Dynamic")
                        updated = True
                    # If we already updated, we skip (delete) any subsequent dynamic lines to avoid duplication
                else:
                    new_lines.append(line)
            
            new_content = "\n".join(new_lines)
            # Preserve trailing newline if it existed
            if content.endswith('\n') and not new_content.endswith('\n'):
                new_content += '\n'
            
            if new_content != content:
                with open(workflow_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Agendamento dinâmico atualizado para: {cron_exp} (UTC)")
            else:
                print("O agendamento já está atualizado.")
                
        except Exception as e:
            print(f"Erro ao atualizar workflow: {e}")
