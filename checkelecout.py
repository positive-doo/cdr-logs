from bs4 import BeautifulSoup
from datetime import date, timedelta
from os import getenv
import requests
import os
os.environ["PRAVNIK_PASS"] = "Leofort1s"

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
def send_email(subject, message, from_addr, to_addr, smtp_server, smtp_port, username, password):
    """
    Sends an email using SMTP protocol.

    Args:
    subject (str): Subject line of the email.
    message (str): Body of the email.
    from_addr (str): Sender's email address.
    to_addr (str): Recipient's email address.
    smtp_server (str): Address of the SMTP server to connect to.
    smtp_port (int): Port number for the SMTP server.
    username (str): Username for the SMTP server authentication.
    password (str): Password for the SMTP server authentication.

    This function creates an email message using the specified subject and
    message, sets up a connection to the specified SMTP server, logs in with
    provided credentials, and sends the email. The connection is securely 
    established using TLS (Transport Layer Security).
    """
    
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

x = ""
def check_term_in_file(url, term):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return term.lower() in soup.text.lower()
    except Exception as e:
        x += f"Error fetching {url}: {e}\n"
        return False


term0 = "Данила Киша"
urls = [
    "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_0_Iskljucenja.htm",
    "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_1_Iskljucenja.htm",
    "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_2_Iskljucenja.htm",
    "https://elektrodistribucija.rs/planirana-iskljucenja-srbija/NoviSad_Dan_3_Iskljucenja.htm"
]

danas = date.today()
sutra = (danas + timedelta(days=1)).strftime("%d.%m.%Y")
prekosutra = (danas + timedelta(days=2)).strftime("%d.%m.%Y")
nakosutra = (danas + timedelta(days=3)).strftime("%d.%m.%Y")
danas = danas.strftime("%d.%m.%Y")

day_mapping = {0: f"DANAS {danas}", 1: f"SUTRA {sutra}", 2: f"PREKOSUTRA {prekosutra}", 3: f"NAKOSUTRA {nakosutra}"}

results = []
for i, url in enumerate(urls):
    if check_term_in_file(url, term0):
        results.append((day_mapping[i], url))

y = False
output = ""
if results:
    y = True
    for result in results:
        output += f"Termin '{term0}' je pronađen za '{result[0]}', pogledajte:\n{result[1]}\n\n"
else:
    output += f"Termin'{term0}' nije pronađen u narednim danima.\n\n"

if y:
    send_email(
        subject=f"Isključenja struje u Danila Kiša!",
        message=output,
        from_addr="nemanja.perun98@gmail.com",
        to_addr="nemanja.perunicic@positive.rs",
        smtp_server="smtp.office365.com",
        smtp_port=587,
        username="nemanja.perun98@gmail.com",
        password=getenv("PRAVNIK_PASS")
    )
    send_email(
        subject=f"Isključenja struje u Danila Kiša!",
        message=output,
        from_addr="nemanja.perun98@gmail.com",
        to_addr="nemanja.perunicic@positive.rs",
        smtp_server="smtp.office365.com",
        smtp_port=587,
        username="nemanja.perun98@gmail.com",
        password=getenv("PRAVNIK_PASS")
    )
else:
    send_email(
        subject=f"Isključenja struje u Danila Kiša!",
        message=output,
        from_addr="azure.test@positive.rs",
        to_addr="nemanja.perunicic@positive.rs",
        smtp_server="smtp.office365.com",
        smtp_port=587,
        username="nemanja.perunicic@positive.rs",
        password=getenv("PRAVNIK_PASS")
    )

if x.strip() != "":
    send_email(
        subject=f"Isključenja struje - Error occurred!",
        message=output,
        from_addr="azure.test@positive.rs",
        to_addr="nemanja.perunicic@positive.rs",
        smtp_server="smtp.office365.com",
        smtp_port=587,
        username="azure.test@positive.rs",
        password=getenv("PRAVNIK_PASS")
    )
