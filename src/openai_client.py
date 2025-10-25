import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

def get_openai_client() -> OpenAI:
    """
    Carrega a chave da API OpenAI do arquivo .env e retorna um cliente OpenAI autenticado.

    Returns:
        Um objeto de cliente OpenAI pronto para uso.

    Raises:
        ValueError: Se a chave da API não for encontrada no ambiente.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo .env.")
    return OpenAI(api_key=api_key)

def transcribe_images(client: OpenAI, images: list[bytes]) -> str:
    """
    Envia uma lista de imagens para o modelo gpt-4o e solicita a transcrição.

    Args:
        client: O cliente OpenAI autenticado.
        images: Uma lista de imagens em formato de bytes.

    Returns:
        A transcrição do texto contido nas imagens.
    """
    base64_images = [base64.b64encode(img).decode('utf-8') for img in images]

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Transcreva o texto manuscrito contido nesta imagem. "
                        "Não faça nenhuma correção gramatical ou de qualquer outro tipo. "
                        "Transcreva exatamente o que está escrito. "
                        "Se você não conseguir ler uma palavra, substitua-a pela palavra 'INELEGÍVEL' em letras maiúsculas."
                    )
                },
                *[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    } for img_b64 in base64_images
                ]
            ]
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        raise
