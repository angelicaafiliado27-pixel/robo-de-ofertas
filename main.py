import requests
import time
import threading
import http.server
import socketserver
from bs4 import BeautifulSoup

# --- CONFIGURAÇÕES DO SEU ROBÔ ---
# Token do seu bot Maepraticabot
TOKEN_TELEGRAM = "8714375855:AAHULALUU7p9hcp1YUSBAl_bDn5vPbzvZdM"

# Como o seu grupo agora é PÚBLICO, usamos o @ do link que você criou
# Certifique-se de que o link do seu grupo seja t.me/ofertasmaepratica
CANAL_DESTINO = "@ofertasmaepratica" 

# Fonte das melhores ofertas (Canal Mestre )
CANAL_FONTE = "https://t.me/s/jgtechofertas" 

# Suas Tags de Afiliado (Já configuradas conforme sua estrutura )
TAGS = {
    'amazon': 'maepratica0b-20',
    'mercadolivre': 'aa20260106122411',
    'shopee': '18337860663',
    'magalu': 'magazinecasababylovers'
}

def enviar_telegram(mensagem):
    """Envia a mensagem para o seu grupo público do Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CANAL_DESTINO, 
        "text": mensagem, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload )
        print(f"Status Envio: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return False

def converter_link(link_original):
    """Aplica suas tags de afiliado automaticamente nos links encontrados"""
    link = link_original.lower()
    if 'amazon.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}tag={TAGS['amazon']}"
    elif 'shopee.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}smtt=0.0.{TAGS['shopee']}"
    elif 'mercadolivre.com.br' in link:
        conector = '&' if '?' in link else '?'
        return f"{link_original}{conector}utm_source=afiliado&utm_campaign={TAGS['mercadolivre']}"
    elif 'magazineluiza.com.br' in link:
        # Para Magalu, geralmente redirecionamos para sua loja magazinevoce
        return f"https://www.magazinevoce.com.br/{TAGS['magalu']}/"
    return link_original

def buscar_ofertas( ):
    """Monitora o canal fonte e envia novas ofertas a cada 1 hora"""
    print("🚀 Robô Maepratica: Monitoramento Iniciado!")
    ultima_oferta = ""
    
    while True:
        try:
            print("🔎 Verificando novas ofertas relâmpago...")
            # Acessa a versão web do canal fonte para fazer o scraping
            res = requests.get(CANAL_FONTE, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Encontra as bolhas de mensagem do Telegram
            mensagens = soup.find_all('div', class_='tgme_widget_message_bubble')
            
            if mensagens:
                msg = mensagens[-1] # Pega a oferta mais recente
                texto_elem = msg.find('div', class_='tgme_widget_message_text')
                
                if texto_elem:
                    # Extrai todos os links da mensagem
                    links = [a['href'] for a in texto_elem.find_all('a', href=True)]
                    
                    if links and links[0] != ultima_oferta:
                        link_original = links[0]
                        link_com_comissao = converter_link(link_original)
                        
                        # Monta a mensagem final para o seu grupo
                        msg_final = (
                            "🔥 *OFERTA RELÂMPAGO ENCONTRADA!*\n\n"
                            "🔗 *COMPRE AQUI COM DESCONTO:*\n"
                            f"{link_com_comissao}\n\n"
                            "⚠️ *Aproveite! Oferta por tempo limitado ou até durar o estoque.*"
                        )
                        
                        if enviar_telegram(msg_final):
                            ultima_oferta = link_original
                            print(f"✅ Oferta enviada com sucesso: {link_original}")
            
        except Exception as e:
            print(f"Erro durante o monitoramento: {e}")
            
        # Espera 1 hora (3600 segundos) para a próxima verificação
        # Conforme solicitado: monitoramento de hora em hora
        time.sleep(3600) 

if __name__ == "__main__":
    # Servidor HTTP simples para manter o Render 'Live' (Porta 8080)
    threading.Thread(target=lambda: socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler ).serve_forever(), daemon=True).start()
    
    # Mensagem de inicialização para confirmar que o robô está online no grupo público
    enviar_telegram("🤖 *Robô Maepratica ONLINE!* \n\nAgora seu grupo é público e estou monitorando ofertas a cada 1 hora. 🚀")
    
    # Inicia o loop principal de busca de ofertas
    buscar_ofertas()
