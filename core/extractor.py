from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import docx2txt
import fitz  # PyMuPDF
import os
import torch
import io

# Inicializa o modelo Donut uma vez (singleton)
processor = None
model = None


def init_donut():
    global processor, model
    if processor is None or model is None:
        processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
        model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")


def extract_text_from_pdf(file_path):
    """Extrai texto de arquivos PDF mantendo a estrutura"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_docx(file_path):
    """Extrai texto de arquivos DOCX"""
    return docx2txt.process(file_path)


def extract_text_from_txt(file_path):
    """Lê arquivos de texto simples"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_image(file_path_or_bytes):
    """Extrai texto de imagens usando Donut (OCR avançado)"""
    init_donut()

    try:
        # Aceita tanto caminho de arquivo quanto bytes
        if isinstance(file_path_or_bytes, (str, os.PathLike)):
            image = Image.open(file_path_or_bytes).convert("RGB")
        else:  # Assume que é um objeto bytes/BytesIO
            image = Image.open(io.BytesIO(file_path_or_bytes)).convert("RGB")

        # Pré-processamento para melhorar resultados
        image = image.resize((1280, 960))  # Redimensiona para tamanho ideal

        # Prepara a imagem para o modelo
        pixel_values = processor(image, return_tensors="pt").pixel_values

        # Gera o texto (com tratamento especial para documentos)
        task_prompt = "<s_cord-v2>"
        decoder_input_ids = processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt"
        ).input_ids

        # Executa a inferência
        outputs = model.generate(
            pixel_values.to(model.device),
            decoder_input_ids=decoder_input_ids.to(model.device),
            max_length=model.decoder.config.max_position_embeddings,
            early_stopping=True,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=3,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        # Pós-processamento do resultado
        sequence = processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(
            processor.tokenizer.pad_token, ""
        )
        sequence = sequence.replace("<s_cord-v2>", "").replace("</s>", "").strip()

        return sequence

    except Exception as e:
        print(f"Erro no Donut OCR: {str(e)}")
        return None


def extract_text(file_path_or_bytes, file_extension=None):
    """Função principal para extração de texto de qualquer formato"""
    if file_extension is None:
        if isinstance(file_path_or_bytes, (str, os.PathLike)):
            ext = os.path.splitext(file_path_or_bytes)[1].lower()
        else:
            raise ValueError("Para input em bytes, deve especificar a extensão")
    else:
        ext = file_extension.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path_or_bytes)
    elif ext == ".docx":
        return extract_text_from_docx(file_path_or_bytes)
    elif ext == ".txt":
        return extract_text_from_txt(file_path_or_bytes)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path_or_bytes)
    else:
        raise ValueError(f"Formato não suportado: {ext}")

