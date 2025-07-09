#!/usr/bin/env python3
"""
Sistema Completo di Automazione Report Economico
Invia automaticamente report economici alle 6:00 ogni mattina
"""

import smtplib
import requests
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from bs4 import BeautifulSoup
import yfinance as yf
import os
from typing import Dict, List, Tuple

class EconomicReportGenerator:
    def __init__(self, config_file='config.json'):
        """Inizializza il generatore di report con configurazione"""
        self.config = self.load_config(config_file)
        self.template_path = 'report_template.html'
        
    def load_config(self, config_file: str) -> Dict:
        """Carica configurazione da file JSON"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Configurazione di default
            return {
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender_email": "your_email@gmail.com",
                    "sender_password": "your_app_password",
                    "recipient_email": "recipient@gmail.com"
                },
                "apis": {
                    "alpha_vantage_key": "YOUR_API_KEY",
                    "news_api_key": "YOUR_NEWS_API_KEY"
                },
                "markets": {
                    "indices": ["^FTMIB", "^STOXX50E", "^GDAXI", "^DJI"],
                    "names": ["FTSE MIB", "Euro Stoxx 50", "DAX", "Dow Jones"]
                }
            }
    
    def get_market_data(self) -> List[Dict]:
        """Ottieni dati di mercato real-time"""
        market_data = []
        
        for symbol, name in zip(self.config["markets"]["indices"], 
                               self.config["markets"]["names"]):
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    
                    market_data.append({
                        "name": name,
                        "open": f"{hist['Open'].iloc[-1]:.0f}",
                        "close": f"{current:.0f}",
                        "change": f"{change:+.2f}%",
                        "trend": "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    })
                    
            except Exception as e:
                print(f"Errore nel recupero dati per {name}: {e}")
                # Dati di fallback
                market_data.append({
                    "name": name,
                    "open": "N/A",
                    "close": "N/A",
                    "change": "N/A",
                    "trend": "➡️"
                })
                
        return market_data
    
    def get_economic_indicators(self) -> Dict:
        """Ottieni indicatori economici"""
        try:
            # Simulazione - in produzione useresti API reali
            return {
                "cpi_usa": "+0.2%",
                "unemployment_usa": "4.1%",
                "pmi_manufacturing": "49",
                "fed_rate": "5.25-5.50%",
                "ecb_deposit": "2.00%",
                "ecb_refinancing": "2.15%"
            }
        except Exception as e:
            print(f"Errore nel recupero indicatori: {e}")
            return {
                "cpi_usa": "N/A",
                "unemployment_usa": "N/A",
                "pmi_manufacturing": "N/A",
                "fed_rate": "N/A",
                "ecb_deposit": "N/A",
                "ecb_refinancing": "N/A"
            }
    
    def get_financial_news(self) -> Dict:
        """Ottieni notizie finanziarie categorizzate"""
        news_data = {
            "monetary_policy": [
                {
                    "title": "BCE conferma i tassi: depositi 2,00%, rifinanziamento 2,15%",
                    "link": "https://www.ecb.europa.eu/"
                },
                {
                    "title": "Powell (FED): Decisioni sui tassi dipenderanno dall'inflazione",
                    "link": "https://www.federalreserve.gov/"
                },
                {
                    "title": "Lagarde: Cautela necessaria sul percorso anti-inflazione",
                    "link": "https://www.ecb.europa.eu/"
                }
            ],
            "corporate": [
                {
                    "title": "Stagione trimestrali: focus su settore bancario e automotive",
                    "link": "https://www.borse.it/"
                },
                {
                    "title": "Fusioni e acquisizioni: attività in crescita nel Q3",
                    "link": "https://www.ilsole24ore.com/"
                },
                {
                    "title": "Settore tech: investimenti in AI e sostenibilità",
                    "link": "https://www.repubblica.it/"
                }
            ],
            "geopolitics": [
                {
                    "title": "Tensioni commerciali USA-Cina: nuove tariffe in discussione",
                    "link": "https://www.reuters.com/"
                },
                {
                    "title": "UE-USA: negoziazioni per accordo commerciale",
                    "link": "https://www.europarl.europa.eu/"
                },
                {
                    "title": "Commodity: prezzi petrolio influenzati da tensioni geopolitiche",
                    "link": "https://www.bloomberg.com/"
                }
            ]
        }
        
        return news_data
    
    def get_weekly_events(self) -> List[Dict]:
        """Ottieni eventi economici settimanali"""
        today = datetime.now()
        events = []
        
        for i in range(7):
            date = today + timedelta(days=i)
            day_name = date.strftime("%A")
            day_date = date.strftime("%d/%m")
            
            # Eventi simulati - in produzione useresti API calendario economico
            if day_name == "Tuesday":
                events.append({
                    "day": f"🗓️ Martedì {day_date}",
                    "events": [
                        "Prezzi consumo YoY: Atteso 2.1% - Ore 11:00",
                        "Verbali FOMC: Politica monetaria USA - Ore 20:00"
                    ]
                })
            elif day_name == "Wednesday":
                events.append({
                    "day": f"🗓️ Mercoledì {day_date}",
                    "events": [
                        "Produzione industriale: Atteso +1.0% - Ore 10:00",
                        "Asta BOT 12 mesi: 7.5 miliardi € - Ore 11:00"
                    ]
                })
            elif day_name == "Thursday":
                events.append({
                    "day": f"🗓️ Giovedì {day_date}",
                    "events": [
                        "Inflazione UK: Atteso +0.7% - Ore 08:00",
                        "Produzione industriale Eurozona - Ore 11:00"
                    ]
                })
            elif day_name == "Friday":
                events.append({
                    "day": f"🗓️ Venerdì {day_date}",
                    "events": [
                        "Vendite al dettaglio USA: Atteso +0.3% - Ore 14:30",
                        "Sentiment consumatori Michigan - Ore 16:00"
                    ]
                })
        
        return events[:4]  # Ritorna solo 4 giorni
    
    def generate_html_report(self) -> str:
        """Genera report HTML completo"""
        # Carica template base
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Ottieni dati
        market_data = self.get_market_data()
        indicators = self.get_economic_indicators()
        news = self.get_financial_news()
        weekly_events = self.get_weekly_events()
        
        # Aggiorna data
        current_date = datetime.now().strftime("%d %B %Y")
        template = template.replace("09 Luglio 2025", current_date)
        
        # Aggiorna dati di mercato
        market_rows = ""
        for market in market_data:
            color_class = "positive" if "+" in market["change"] else "negative" if "-" in market["change"] else "neutral"
            market_rows += f"""
            <tr>
                <td><strong>{market['name']}</strong></td>
                <td>{market['open']}</td>
                <td>{market['close']}</td>
                <td class="{color_class}">{market['change']}</td>
                <td>{market['trend']}</td>
            </tr>
            """
        
        # Aggiorna indicatori
        template = template.replace("5.25-5.50%", indicators["fed_rate"])
        template = template.replace("2,00%", indicators["ecb_deposit"])
        template = template.replace("2,15%", indicators["ecb_refinancing"])
        
        # Aggiorna notizie
        for category, articles in news.items():
            for i, article in enumerate(articles):
                placeholder = f"{category}_{i}_title"
                if placeholder in template:
                    template = template.replace(placeholder, article["title"])
        
        # Aggiorna eventi settimanali
        events_html = ""
        for event in weekly_events:
            events_html += f"""
            <div class="day-events">
                <h4>{event['day']}</h4>
                <ul>
            """
            for event_item in event['events']:
                events_html += f"<li>{event_item}</li>"
            events_html += "</ul></div>"
        
        return template
    
    def send_email_report(self, html_content: str) -> bool:
        """Invia report via email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Report Economico - {datetime.now().strftime('%d/%m/%Y')}"
            msg['From'] = self.config["email"]["sender_email"]
            msg['To'] = self.config["email"]["recipient_email"]
            
            # Crea parte HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Invia email
            server = smtplib.SMTP(self.config["email"]["smtp_server"], 
                                 self.config["email"]["smtp_port"])
            server.starttls()
            server.login(self.config["email"]["sender_email"], 
                        self.config["email"]["sender_password"])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Report inviato con successo alle {datetime.now().strftime('%H:%M')}")
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'invio email: {e}")
            return False
    
    def generate_and_send_report(self):
        """Funzione principale: genera e invia report"""
        print(f"🔄 Generazione report iniziata alle {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            html_content = self.generate_html_report()
            success = self.send_email_report(html_content)
            
            if success:
                print("✅ Report completato con successo!")
            else:
                print("❌ Errore nella generazione del report")
                
        except Exception as e:
            print(f"❌ Errore generale: {e}")

def create_config_file():
    """Crea file di configurazione di esempio"""
    config = {
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your_email@gmail.com",
            "sender_password": "your_app_password",
            "recipient_email": "recipient@gmail.com"
        },
        "apis": {
            "alpha_vantage_key": "YOUR_ALPHA_VANTAGE_KEY",
            "news_api_key": "YOUR_NEWS_API_KEY"
        },
        "markets": {
            "indices": ["^FTMIB", "^STOXX50E", "^GDAXI", "^DJI"],
            "names": ["FTSE MIB", "Euro Stoxx 50", "DAX", "Dow Jones"]
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("📝 File config.json creato! Personalizza con i tuoi dati.")

def main():
    """Funzione principale con scheduler"""
    # Crea configurazione se non esiste
    if not os.path.exists('config.json'):
        create_config_file()
        print("⚠️  Configura il file config.json prima di procedere!")
        return
    
    # Inizializza generatore
    generator = EconomicReportGenerator()
    
    # Programma invio giornaliero alle 6:00
    schedule.every().day.at("06:00").do(generator.generate_and_send_report)
    
    # Per test immediato (rimuovi in produzione)
    # generator.generate_and_send_report()
    
    print("🚀 Sistema di automazione avviato!")
    print("📧 Report programmato per le 6:00 ogni mattina")
    print("⏰ Premi Ctrl+C per terminare")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Controlla ogni minuto
    except KeyboardInterrupt:
        print("\n👋 Sistema terminato dall'utente")

if __name__ == "__main__":
    main()
