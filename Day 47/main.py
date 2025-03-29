import requests
from bs4 import BeautifulSoup
import smtplib
import dotenv
import os
from email.mime.text import MIMEText
from email.header import Header

dotenv.load_dotenv()

#URL="https://appbrewery.github.io/instant_pot/"
URL="https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
MAIL= os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
RECIPIENT = os.environ.get("EMAIL_RECIPIENT")

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

amazon = requests.get(url=URL, headers=header).text

soup = BeautifulSoup(amazon, "html.parser")

price = soup.select_one(".aok-offscreen").getText().strip()
print(price)

price_without_currency = price.split("$")[1]

price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.select_one("#productTitle").getText().strip()
print(title)

if price_as_float < 100:
    subject = "Amazon Price Alert!"
    body = f"{title} is now {price}\n{URL}"
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = MAIL
    msg["To"] = RECIPIENT

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MAIL, password=PASSWORD)
        connection.sendmail(from_addr=MAIL, to_addrs=RECIPIENT, msg=msg.as_string())