"""
Integração com OpenRouter API para geração de conteúdo jornalístico.
"""

import os
import json
import re
import traceback
from openai import OpenAI


SYSTEM_PROMPT = """Você é um gerador especializado em conteúdo jornalístico.
Sua tarefa é transformar temas, acontecimentos ou press releases em conteúdo jornalístico profissional e estruturado.

INSTRUÇÃO CRÍTICA: Retorne EXCLUSIVAMENTE um JSON válido, sem markdown, sem blocos de código, sem texto extra, sem explicações.

Estrutura obrigatória do JSON:
{
  "manchete": "Título jornalístico impactante e envolvente (máx. 80 caracteres)",
  "pauta": "Resumo editorial com ângulo da matéria (3-5 linhas)",
  "noticia": "Corpo completo da notícia em formato jornalístico usando pirâmide invertida (3-4 parágrafos)",
  "social": "Post otimizado para redes sociais (máx. 280 caracteres) com hashtags relevantes",
  "roteiro_video": "Roteiro narrado para vídeo curto (reels/shorts) com indicações de cena",
  "entrevista": "3 perguntas sugeridas para entrevista com especialistas no tema, uma por linha"
}

Regras:
- Responda APENAS com o JSON puro
- Certifique-se que o JSON é válido
- Conteúdo deve ser profissional, imparcial e factual"""


def generate_journalistic_content(theme_or_release: str) -> tuple[dict | None, str | None]:
    """
    Chama a OpenRouter API para gerar conteúdo jornalístico estruturado.
    """
    try:
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return None, "Chave API do OpenRouter não configurada. Configure OPENROUTER_API_KEY em .env"

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        response = client.chat.completions.create(
            model="deepseek/deepseek-v3.2",  # modelo gratuito
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Gere conteúdo jornalístico para: {theme_or_release}"}
            ],
            max_tokens=2048,
            temperature=0.7,
        )

        resposta_texto = response.choices[0].message.content

        if not resposta_texto:
            return None, "OpenRouter retornou resposta vazia. Tente novamente."

        result_json = _parse_json_response(resposta_texto)

        if result_json is None:
            return None, "Não consegui processar a resposta da IA. Tente novamente com outro tema."

        if not _validate_json_structure(result_json):
            return None, "Resposta da IA está incompleta. Campos obrigatórios faltando."

        return result_json, None

    except Exception as e:
        traceback.print_exc()
        error_msg = str(e).lower()

        if "401" in error_msg or "unauthorized" in error_msg:
            return None, "Chave API inválida. Verifique sua OPENROUTER_API_KEY."
        elif "429" in error_msg or "rate limit" in error_msg:
            return None, "Limite de requisições atingido. Aguarde alguns minutos."
        elif "connection" in error_msg or "timeout" in error_msg:
            return None, "Erro de conexão. Verifique sua internet."
        else:
            return None, f"Erro inesperado: {str(e)}"


def _parse_json_response(text: str) -> dict | None:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    text_cleaned = re.sub(r'```json\s*', '', text)
    text_cleaned = re.sub(r'```', '', text_cleaned)
    text_cleaned = text_cleaned.strip()

    try:
        return json.loads(text_cleaned)
    except json.JSONDecodeError:
        pass

    json_match = re.search(r'\{.*\}', text_cleaned, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return None


def _validate_json_structure(data: dict) -> bool:
    required_keys = {"manchete", "pauta", "noticia", "social", "roteiro_video", "entrevista"}
    return required_keys.issubset(set(data.keys()))