import feedparser
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from transformers import pipeline
from datetime import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor

from deep_translator import GoogleTranslator

# List of RSS feed URLs
rss_feeds = [
    "https://www.omgubuntu.co.uk/feed"
]

# Load AI classification and summarization models
try:
    clasificador_ia = pipeline("text-classification", model="mrm8488/bert-mini-finetuned-age_news-classification")
    resumen_ia = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print(f"⚠️ Error loading AI models: {e}")
    clasificador_ia = None
    resumen_ia = None

# Helper function to download a feed
def fetch_feed(url):
    return feedparser.parse(url).entries

# Function to download and parse articles with concurrency (download only)
def descargar_articulos():
    entradas = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_feed, rss_feeds)
        for r in results:
            entradas.extend(r)
    return entradas

# Process a single article (sequentially)
def procesar_entrada(entry):
    try:
        response = requests.get(entry.link, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        contenido = ' '.join([para.get_text() for para in paragraphs])
    except:
        return None

    if not contenido.strip():
        return None

    if "subscriber of LWN.net" in contenido.lower() or len(contenido) < 300:
        return None

    print(f"Viewing: {entry.title}")
    print(f"URL: {entry.link}")
    print("Extracted content:")
    print(contenido[:500])

    try:
        idioma_original = detect(contenido)
    except:
        idioma_original = 'en'

    texto_para_clasificar = contenido.strip().replace("\n", " ")[:1000]

    try:
        if clasificador_ia:
            resultado = clasificador_ia(texto_para_clasificar)[0]
            print(f"🤖 AI Classification: {resultado['label']} (score: {resultado['score']:.2f})")
            if resultado['label'].lower() not in ['tech', 'sci/tech']:
                return None
        else:
            print("⚠️ Classifier not available. Including by default.")
    except Exception as e:
        print(f"⚠️ Error classifying content: {e}")
        return None

    if idioma_original != 'es':
        try:
            contenido = GoogleTranslator(source='auto', target='es').translate(text=contenido)
        except:
            return None

    texto_para_resumen = contenido.strip().replace("\n", " ")[:2000]

    print(f"✏️ Summarizing article: {entry.title}")
    try:
        if resumen_ia:
            resumen = resumen_ia(texto_para_resumen, max_length=350, min_length=200, do_sample=False)[0]['summary_text']
        else:
            resumen = texto_para_resumen[:700] + "..."
    except Exception as e:
        print(f"⚠️ Error summarizing with AI: {e}")
        resumen = texto_para_resumen[:700] + "..."

    return {
        'titulo': entry.title,
        'link': entry.link,
        'resumen': resumen
    }

# Function to get and process articles sequentially
def obtener_articulos():
    articulos_relevantes = []
    entradas = descargar_articulos()

    inicio = time.time()
    for entrada in entradas:
        resultado = procesar_entrada(entrada)
        if resultado:
            articulos_relevantes.append(resultado)
    fin = time.time()
    print(f"⏱️ Total processing time: {fin - inicio:.2f} seconds")

    return articulos_relevantes

# Save summary in Markdown
def guardar_markdown(articulos):
    fecha = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("output", exist_ok=True)
    filename = os.path.join("output", f"resumen_{fecha}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# \U0001F4F0 Daily Summary - {fecha}\n\n")
        for articulo in articulos:
            f.write(f"## [{articulo['titulo']}]({articulo['link']})\n")
            f.write(f"{articulo['resumen']}\n\n")

    print(f"\u2705 Summary saved as Markdown in: {filename}")

# Save summary in HTML
def guardar_html(articulos):
    fecha = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("output", exist_ok=True)
    filename = os.path.join("output", f"resumen_{fecha}.html")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<html><head><meta charset='utf-8'><title>Daily Summary {fecha}</title></head><body>")
        f.write(f"<h1>\U0001F4F0 Daily Summary - {fecha}</h1>")
        for articulo in articulos:
            f.write(f"<h2><a href='{articulo['link']}'>{articulo['titulo']}</a></h2>")
            f.write(f"<p>{articulo['resumen']}</p>")
        f.write("</body></html>")

    print(f"\u2705 Summary saved as HTML in: {filename}")

# Run the script
if __name__ == '__main__':
    articulos = obtener_articulos()
    if articulos:
        guardar_markdown(articulos)
        guardar_html(articulos)
    else:
        print('No relevant articles found.')