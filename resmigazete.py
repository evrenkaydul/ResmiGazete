import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime
import sys

def fetch_content_with_clickable_links_spaced_and_two_at_end():
    url = "https://www.resmigazete.gov.tr/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        news_items = soup.find_all('div', class_='fihrist-item mb-1')

        contents = ['<table style="width:100%; border-collapse: collapse;">']

        for item in news_items:
            title = item.find('a').text.strip()
            link = item.find('a')['href']
            link = link if "http" in link else url + link

            row = f'''
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: left;">
                    <b><a href="{link}" style="color: #44546A; text-decoration: none;">{title}</a></b>
                </td>
            </tr>
            '''
            contents.append(row)

        contents.append('</table>')

        styled_content = f'''
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #E8EBF0; /* Açık gri arka plan */
                        color: #333;
                        line-height: 1.6;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        padding: 20px;
                        background: #E8EBF0; /* Beyaz arka plan */
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #44546A; /* Koyu mavi-gri başlık rengi */
                        text-align: center;
                        margin-bottom: 30px;
                        font-size: 23px;
                    }}
                    a {{
                        color: #44546A; /* Koyu mavi-gri link rengi */
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    td {{
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Resmi Gazete Günlüğü</h1>
                    {''.join(contents)}
                    <div class="footer">
                    <p><b>Bu e-posta içeriği Python {python_version} kullanılarak otomatik olarak oluşturulmuştur.</b></p>
                </div>
                </div>
            </body>
        </html>
        '''
        return styled_content
    except requests.RequestException as e:
        print(f"Resmi Gazete'den içerik çekerken bir hata oluştu: {e}")
        return None

python_version = sys.version.split()[0]  # Python versiyonunu al

def send_email_with_html(content, to_email):
    from_email = "Email_Adresi"
    password = "Şifre"
    
    # Mevcut tarihi al ve formatla
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    email_subject = f"{current_date} Tarihli Resmi Gazete İçeriği"
    
    try:
        msg = MIMEText(content, 'html', _charset='utf-8')  # HTML içerik türü ile e-posta oluşturuyoruz
        msg['Subject'] = email_subject  # Konuyu güncel tarih ile ayarla
        msg['From'] = from_email
        msg['To'] = to_email
        
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()  # SMTP sunucusuyla selamlaşma
        server.starttls()  # STARTTLS ile güvenli bağlantı başlat
        server.ehlo()  # STARTTLS sonrası tekrar selamlaşma
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"E-posta gönderilirken bir hata oluştu: {e}")

if __name__ == "__main__":
    content = fetch_content_with_clickable_links_spaced_and_two_at_end()
    if content:
        send_email_with_html(content, "Email_Adresi")
    else:
        print("İçerik çekilemedi, e-posta gönderilmedi.")
