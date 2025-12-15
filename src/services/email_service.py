import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from src.config import Config

class EmailService:
    @staticmethod
    def send_notification(game_name, availability, screenshot_path=None):
        destinatario = Config.EMAIL_RECIPIENT
        assunto = f"{game_name} - Grátis na Epic Games"
        
        conteudo = f"""
Um novo jogo grátis foi detectado na Epic Games Store.

Jogo: {game_name}
Disponibilidade: {availability}

Link para resgate: {Config.EPIC_GAMES_URL}

Aproveite!
"""

        msg = MIMEMultipart('related')
        msg['Subject'] = assunto
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = destinatario

        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)

        msg_text = MIMEText(conteudo, 'plain')
        msg_alternative.attach(msg_text)

        html_content = f"""
        <html>
            <body>
                <p>{conteudo.replace(chr(10), '<br>')}</p>
                <br>
                <img src="cid:game_image" alt="Screenshot do Jogo" style="max-width: 100%;">
            </body>
        </html>
        """
        msg_html = MIMEText(html_content, 'html')
        msg_alternative.attach(msg_html)

        if screenshot_path:
            try:
                with open(screenshot_path, 'rb') as f:
                    img_data = f.read()
                
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<game_image>')
                img.add_header('Content-Disposition', 'inline', filename=os.path.basename(screenshot_path))
                msg.attach(img)
            except Exception as e:
                print(f"Erro ao anexar imagem: {e}")

        try:
            with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT) as smtp:
                smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                smtp.send_message(msg)
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
