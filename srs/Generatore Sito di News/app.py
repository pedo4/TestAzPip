from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from jinja2 import Template
import re
from newspaper import Article
import nltk
import os
import openai
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    # Route per la pagina principale del form news website
    return render_template('form_NW.html')

# Route per i file statici
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/genera_news_website', methods=['POST'])
def genera_news_website():
    # Route per la generazione del sito di news

    #recupero dei dati inseriti dall'utente
    article_count = request.form.get('num_articoli')
    length_count = request.form.get('lunghezza_articoli')

    # Download dei dati necessari per la tokenizzazione delle frasi
    nltk.download('punkt')

    # Inizializzazione dell'oggetto NewsApiClient con la chiave API
    newsapi = NewsApiClient(api_key='c240c14564e148d1a0371d4f37355153')

    # Esempio di chiamata per ottenere notizie basate su una parola chiave
    keyword = 'breaking news'
    news_by_keyword = newsapi.get_everything(q=keyword, page_size=int(article_count))

    # Caricamento del template HTML utilizzando Jinja2
    template = Template('''
        <div class="news">
            <h2>{{ article.title }}</h2>
            <p>{{ article.description }}</p>
            <p>Author: {{ article.author }}</p>
            <p>{% for line in article.content_lines %}{{ line }}<br>{% endfor %}</p>
        </div>
    ''')

    # Genera il codice HTML per le notizie
    html_text = ''
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
        n_sentences = int(length_count)  # Imposta il numero desiderato di frasi
        article['content_lines'] = sentences[:n_sentences]

        # Genera il codice HTML per l'articolo utilizzando il template
        html_text += template.render(article=article)

    # Lettura del contenuto del file template_news.html
    with open("template_news.html", "r") as file:
        html_content = file.read()

    # Composizione del prompt con la descrizione dell'utente e il contenuto del file HTML
    prompt = f"Alterare il codice HTML {html_content} che ti invio, utilizzando il contenuto di {html_text} per rappresentare i diversi articoli. Traduci tutto in italiano. Inoltre, utilizza lo stesso stile e la stessa struttura del file di template."

    # Impostazione della chiave API
    openai.api_key = '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'

    # Chiamata all'API di completamento di OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=2500,
        temperature=1
    )

    html_text = response.choices[0].text
    api_usage = response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    
    templates_dir = os.path.join(app.root_path, 'static')
    # Salva l'HTML generato su file
    file_path = os.path.join(templates_dir, 'NewsWebsite.html')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(html_text)

    return send_from_directory('static', 'NewsWebsite.html')


if __name__ == '__main__':
    app.run()
