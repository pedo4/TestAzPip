from jinja2 import Environment, FileSystemLoader

# Carica il template HTML dal file
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('temEcom.html')

# Definisci i valori mockati dei parametri
parametri = {
    'categorie': ['cucina', 'elettronica', 'igiene'],
    'numero_di_prodotti': 'Oltre 1000 prodotti disponibili',
    'descrizione': 'Benvenuti nel nostro negozio online',
    'prodotti': ['Prodotto 1', 'Prodotto 2', 'Prodotto 3']
}

# Renderizza la pagina HTML con i valori mockati
output = template.render(**parametri)

# Salva il risultato in un file
with open('output.html', 'w') as file:
    file.write(output)
