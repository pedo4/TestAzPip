from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from jinja2 import Template
import webbrowser
import re
from newspaper import Article
import nltk

# Download dei dati necessari per la tokenizzazione delle frasi
nltk.download('punkt')

# Inizializza l'oggetto NewsApiClient con la tua chiave API
newsapi = NewsApiClient(api_key='c240c14564e148d1a0371d4f37355153')

# Esempio di chiamata per ottenere notizie basate su una parola chiave
keyword = 'bed'
news_by_keyword = newsapi.get_everything(q=keyword, page_size=3)

# Carica il template HTML utilizzando Jinja2
template = Template('''
    <div class="news">
        <h2>{{ article.title }}</h2>
        <p>{{ article.description }}</p>
        <p>Author: {{ article.author }}</p>
        <p>{% for line in article.content_lines %}{{ line }}<br>{% endfor %}</p>
        <a href="{{ article.url }}"> Read More </a>
    </div>
''')

# Genera il codice HTML per le notizie
html_content = ''
for article in news_by_keyword['articles']:
    if article.get('content'):
        # Recupera il contenuto completo dell'articolo togliendo contenuti superflui dell'URL (link, video, immagini...)
        article_url = article['url']
        news_article = Article(article_url)
        news_article.download()
        news_article.parse()
        article_text = news_article.text
        # Aggiorna l'oggetto dell'articolo con il contenuto completo
        article['content'] = article_text

        # Rimuovi [+X chars] dal contenuto dell'articolo
        article['content'] = re.sub(r'\[\+\d+ chars\]', '', article['content'])

        # Utilizza BeautifulSoup per filtrare i contenuti indesiderati
        soup = BeautifulSoup(article['content'], 'html.parser')
        # Rimuovi tutti i tag <a> e i loro contenuti
        for a in soup.find_all('a'):
            a.decompose()
        # Rimuovi tutti i tag <img> e i loro contenuti
        for img in soup.find_all('img'):
            img.decompose()
        # Ottieni solo il testo rimanente
        cleaned_text = soup.get_text()

        # Tokenizzazione delle frasi
        sentences = nltk.sent_tokenize(cleaned_text)

        # Limita il numero di frasi dell'articolo
        max_sentences = 3  # Imposta il numero desiderato di frasi
        article['content_lines'] = sentences[:max_sentences]

        # Genera il codice HTML per l'articolo utilizzando il template
        html_content += template.render(article=article)

# Salva il codice HTML in un file
with open('notizie.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Apri il file HTML con il browser predefinito
webbrowser.open('notizie.html')


