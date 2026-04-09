import requests
from bs4 import BeautifulSoup
import time
import re

# --- SUAS TAGS JÁ CONFIGURADAS ---
TAGS_AFILIADO = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

# Canal que o robô vai vigiar
CANAL_FONTE = "https://t.me/s/jgtechofertas"

def converter_link(link_original ):
    link_original = link_original.lower()
    if 'amazon.com.br' in link_original:
        conector = '&' if '?' in link_original else '?'
        return f"{link_original}{conector}tag={TAGS_AFILIADO['amazon']}"
    elif 'shopee.com.br' in link_original:
        conector = '&' if '?' in link_original else '?'
        return f"{link_original}{conector}smtt=0.0.{TAGS_AFILIADO['shopee']}"
    elif 'mercadolivre.com.br' in link_original:
        conector = '&' if '?' in link_original else '?'
        return f"{link_original}{conector}utm_source=afiliado&utm_campaign={TAGS_AFILIADO['mercadolivre']}"
    elif 'magazineluiza.com.br' in link_original:
        return f"https://www.magazinevoce.com.br/{TAGS_AFILIADO['magalu']}/"
    return link_original

def buscar_e_postar( ):
    print(f"[{time.strftime('%H:%M:%S')}] Verificando novas ofertas...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(CANAL_FONTE, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
        
        for msg in mensagens:
            texto_elem = msg.find('div', class_='tgme_widget_message_text')
            if not texto_elem: continue
            
            links = [a['href'] for a in texto_elem.find_all('a', href=True)]
            if links:
                link_convertido = converter_link(links[0])
                print(f"\n--- NOVA OFERTA ENCONTRADA ---")
                print(f"Link com sua comissão: {link_convertido}")
                # Aqui o robô enviaria para o seu WhatsApp
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("🚀 Robô de Ofertas Iniciado!")
    while True:
        buscar_e_postar()
        time.sleep(300) # Espera 5 minutos para a próxima busca
