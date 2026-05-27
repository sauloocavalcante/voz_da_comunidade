"""
Flask application para Voz da Comunidade.
Plataforma de transformação de temas/releases em conteúdo jornalístico via IA.
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from services import generate_journalistic_content

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')


@app.route('/', methods=['GET'])
def index():
    """Renderiza página inicial com formulário."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Endpoint que recebe tema/release e retorna conteúdo jornalístico.
    """
    data = request.get_json()
    user_input = data.get('input', '').strip() if data else ''
    
    # Validação mínima
    if not user_input or len(user_input) < 10:
        return jsonify({
            'error': 'Texto deve ter no mínimo 10 caracteres'
        }), 400
    
    # Chama geração de conteúdo
    result, error = generate_journalistic_content(user_input)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify(result), 200


@app.errorhandler(404)
def not_found(error):
    """Trata rotas não encontradas."""
    return jsonify({'error': 'Rota não encontrada'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Trata erros internos do servidor."""
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
