import os
import argparse
from src.pdf_processor import extract_images_from_pdf
from src.openai_client import get_openai_client, transcribe_images

def main():
    """
    Ponto de entrada principal do script.
    Processa os arquivos PDF de um diretório e gera as transcrições.
    """
    parser = argparse.ArgumentParser(
        description="Transcreve o conteúdo de arquivos PDF manuscritos usando a API da OpenAI."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="O caminho para o diretório contendo os arquivos .pdf."
    )
    args = parser.parse_args()

    input_dir = args.directory
    output_dir = "temp"

    # Cria o diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Inicializa o cliente OpenAI
    try:
        openai_client = get_openai_client()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return

    # Processa cada arquivo no diretório de entrada
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            base_filename = os.path.splitext(filename)[0]
            output_filepath = os.path.join(output_dir, f"{base_filename}.txt")

            print(f"Processando arquivo: {filename}...")

            try:
                # 1. Extrair imagens do PDF
                images = extract_images_from_pdf(pdf_path)
                if not images:
                    print(f"  -> Nenhuma imagem encontrada em '{filename}'. Pulando.")
                    continue

                # 2. Transcrever imagens com a API
                transcription = transcribe_images(openai_client, images)

                # 3. Salvar o resultado
                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write(transcription)

                print(f"  -> Transcrição salva em: {output_filepath}")

            except Exception as e:
                print(f"  -> Ocorreu um erro ao processar o arquivo '{filename}': {e}")
                print("     Pulando para o próximo arquivo.")
                continue

    print("\nProcessamento concluído.")

if __name__ == "__main__":
    main()
