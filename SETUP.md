# Setup Voz da Comunidade

## 1. Ativar Virtualenv

```bash
source venv/bin/activate
```

## 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 3. Obter Chave API do Gemini

1. Acesse: https://aistudio.google.com/app/apikey
2. Clique em "Create API Key"
3. Selecione "Create API key in new project" (ou projeto existente)
4. Copie a chave gerada

## 4. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
# Edite .env e adicione sua GEMINI_API_KEY
nano .env
```

Seu `.env` deve ficar assim:
```
GEMINI_API_KEY=sua_chave_aqui
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## 5. Executar o Servidor

```bash
python app.py
```

O servidor estará disponível em: **http://localhost:5000**

## Estrutura de Arquivos

```
voz-da-comunidade/
├── app.py              ← Rotas Flask (GET / e POST /api/generate)
├── services.py         ← Integração com Gemini + parsing JSON robusto
├── requirements.txt    ← Dependências Python (Flask, google-generativeai, python-dotenv)
├── .env.example        ← Modelo de variáveis
├── .env                ← Variáveis locais (não sobe pro git)
├── .gitignore          ← Configuração Git
├── SETUP.md            ← Este arquivo
└── templates/
    └── index.html      ← Frontend completo com CSS/JS
```

## Teste Rápido

Com o servidor rodando, abra seu navegador e acesse:
- GET http://localhost:5000/ → Renderiza o formulário
- POST http://localhost:5000/api/generate → Gera conteúdo

### Teste via cURL

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Comunidade de Vila Olímpia iniciou um projeto inovador de educação e inclusão digital para jovens da periferia. Mais de 500 alunos já participam das aulas gratuitas."
  }' | python3 -m json.tool
```

## Troubleshooting

**"Chave API não configurada"**
- Verifique que `.env` existe e contém `GEMINI_API_KEY`
- Tente recarregar a página ou reiniciar o servidor

**"Chave API inválida"**
- Gere uma nova chave em https://aistudio.google.com/app/apikey
- Verifique que não há espaços extras

**"Limite de requisições atingido"**
- O Gemini (versão free) tem rate limiting
- Aguarde alguns minutos e tente novamente
- Considere usar uma chave de projeto pago para aumentar limites

