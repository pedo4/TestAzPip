# Utilizza un'immagine di base con il server web desiderato
FROM nginx:latest

# Copia il file specificato tramite il parametro "filename" nella directory di default del server web
ARG filename
COPY $filename /usr/share/nginx/html/output.html

# Copia il file di configurazione personalizzato
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Espone la porta 80 per consentire l'accesso al server web
EXPOSE 80

# Avvia il server web
CMD ["nginx", "-g", "daemon off;"]

