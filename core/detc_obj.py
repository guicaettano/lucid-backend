import easyocr
from PIL import Image
import io

# Inicializa o leitor com suporte ao português
reader = easyocr.Reader(["pt"], gpu=False)


def extract_text_easyocr(image_path_or_bytes):
    if isinstance(image_path_or_bytes, bytes):
        image = Image.open(io.BytesIO(image_path_or_bytes))
        image.save("temp_image.jpg")  # EasyOCR precisa de caminho de arquivo
        image_path = "temp_image.jpg"
    else:
        image_path = image_path_or_bytes

    results = reader.readtext(image_path, detail=0)  # detail=0 retorna só o texto
    return "\n".join(results)
