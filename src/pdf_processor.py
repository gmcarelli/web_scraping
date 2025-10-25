import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path: str) -> list[bytes]:
    """
    Extrai cada página de um arquivo PDF como uma imagem de alta qualidade.

    Args:
        pdf_path: O caminho para o arquivo PDF.

    Returns:
        Uma lista de objetos bytes, onde cada objeto é uma imagem PNG de uma página.

    Raises:
        Exception: Se o arquivo PDF não puder ser aberto ou processado.
    """
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Erro ao abrir o arquivo PDF '{pdf_path}': {e}")
        raise

    images = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # Renderiza a página como uma imagem com 300 DPI
        zoom = 300 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Converte o pixmap para um objeto de imagem do Pillow
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Salva a imagem em um buffer de bytes em formato PNG
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        images.append(img_byte_arr.getvalue())

    pdf_document.close()
    return images
