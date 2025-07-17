from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)

# Rota exemplo para o frontend
@app.route('/')
def home():
    return render_template('index.html')  # HTML em templates/

if __name__ == '__main__':
    # Configura o livereload
    server = Server(app.wsgi_app)
    server.watch('templates/*.html')  # Monitora mudanças nos templates
    server.watch('static/css/*.css')  # Monitora arquivos CSS
    server.serve(port=5000, host='0.0.0.0')