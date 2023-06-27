def get_parameter_names(template_type):
    if template_type == 'ecommerce':
        return [
            {'name': 'numero di prodotti', 'input_type': 'text', 'multiple': False},
            {'name': 'categorie', 'input_type': 'text', 'multiple': True},
            {'name': 'sotto-categorie di prodotti', 'input_type': 'text', 'multiple': True},
            {'name': 'icona', 'input_type': 'file', 'multiple': False}
        ]
    elif template_type == 'news':
        return [
            {'name': 'articoli in prima pagina', 'input_type': 'text', 'multiple': False},
            {'name': 'lunghezza della pagina', 'input_type': 'text', 'multiple': False},
            {'name': 'categorie', 'input_type': 'text', 'multiple': True},
            {'name': 'icona', 'input_type': 'file', 'multiple': False}
        ]
    else:
        return [
            {'name': 'descrizione', 'input_type': 'text', 'multiple': False},
            {'name': 'servizi offerti', 'input_type': 'text', 'multiple': True},
            {'name': 'organigramma', 'input_type': 'text', 'multiple': True, 'key_value': True},
            {'name': 'contatti', 'input_type': 'text', 'multiple': True, 'key_value': True},
            {'name': 'icona', 'input_type': 'file', 'multiple': False}
        ]