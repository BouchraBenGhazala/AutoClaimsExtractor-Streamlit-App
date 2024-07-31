import streamlit as st
from openai import OpenAI
import base64
import json
import cv2
import io
from PIL import Image
import numpy as np

import google.generativeai as genai

# API Key OPENAI
client = OpenAI(organization="org-UBgxxZXUHWRbudONatpTkaAJ", api_key=st.secrets["OPENAI_API_KEY_ORG"])

#API Key Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Model OpenAI
MODEL = "gpt-4o"

#Model Gemini
vision_model = genai.GenerativeModel('gemini-pro-vision')


# Functions
# Encadrer l'image
def returnPartOfImg(image, top, bottom, left, right):
    h, w, c = image.shape
    top = int(h * top)
    bottom = int(h * bottom)
    left = int(w * left)
    right = int(w * right)
    croppedImg = image[top:bottom, left:right]
    return croppedImg

# Encodage de l'image
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")

# Open the image file and encode it as a base64 string
def encode_image2(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Extraire des infos de l'image
def get_image_info_openai(base64_image, prompt):
    content = [{"type": "text", "text": prompt}]
    content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that specializes in extracting informations. Please help in extracting information from those images!"},
                {"role": "user", "content": content}
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)

def get_image_info_gemini(image, request):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convertir en objet PIL
    response = vision_model.generate_content([request, pil_image])
    return response.text

# Extraire des infos de l'audio

prompt_audio = open('prompts/prompt_audio.txt', 'r', encoding="utf-8").read()


def get_transcription_gemini(audio_path, type):
    audio = genai.upload_file(audio_path, mime_type=type)
    response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt_audio, audio])
    text = response.candidates[0].content.parts[0].text.strip()
    return text, audio

prompt_translation = open('prompts/prompt_audio_translation.txt', 'r', encoding="utf-8").read()

def get_translation_gemini(darija_text):
    response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt_translation, darija_text])
    text = response.text.strip()
    return text

prompt_summary = open('prompts/prompt_audio_summary.txt', 'r', encoding="utf-8").read()

def get_summary_gemini(darija_text):
    response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt_summary, darija_text])
    text = response.text.strip()
    return text

# Convertir str en json
def str_to_json(str):
    json_obj = json.loads(str)
    return json_obj

# Load the prompts
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def resize_image(image, size=(320, 320)):
    return image.resize(size, Image.LANCZOS)

def gpt_resp_to_dict(text):
    text = text.replace("json", "")
    text = text.replace("```", "")
    return eval(text)


def process_constat(constat_image):
        #prompts
        prompt_infos = load_prompt('prompts/prompt_infos.txt')
        prompt_vA = load_prompt('prompts/prompt_vehicule.txt')
        prompt_vueA = load_prompt('prompts/prompt_vue.txt')
        prompt_vB = load_prompt('prompts/prompt_vehicule.txt')
        prompt_vueB = load_prompt('prompts/prompt_vue.txt')
        prompt_casA = load_prompt('prompts/prompt_cases.txt')
        prompt_casB = load_prompt('prompts/prompt_cases.txt')

        image = np.array(constat_image)
        cropped_image = returnPartOfImg(image, 0, 0.17, 0, 0.6)  # infos constat
        base64_image = encode_image(cropped_image)
        infos = get_image_info_openai(base64_image, prompt_infos)
        # infos=get_image_info_gemini(cropped_image,prompt_infos)

        VoitureA = returnPartOfImg(image, 0.17, 0.6, 0, 0.32)
        base64_image_2 = encode_image(VoitureA)
        info_voiture_A = get_image_info_openai(base64_image_2, prompt_vA)
        # info_voiture_A = get_image_info_gemini(VoitureA,prompt_vA)

        VueA = returnPartOfImg(image, 0.62, 0.73, 0, 0.32)  # vue vehicule A
        base64_image_2_2 = encode_image(VueA)
        info_vue_A = get_image_info_openai(base64_image_2_2, prompt_vueA)
        # info_vue_A=get_image_info_gemini(VueA,prompt_vueA)

        VoitureB = returnPartOfImg(image, 0.17, 0.6, 0.7, 1)
        base64_image_3 = encode_image(VoitureB)
        info_voiture_B = get_image_info_openai(base64_image_3, prompt_vB)
        # info_voiture_B = get_image_info_gemini(VoitureB, prompt_vB)


        VueB = returnPartOfImg(image, 0.62, 0.72, 0.7, 1)  # vue vehicule B
        base64_image_3_2 = encode_image(VueB)
        info_vue_B = get_image_info_openai(base64_image_3_2, prompt_vueB)
        # info_vue_B = get_image_info_gemini(VueB, prompt_vueB)

        casA = returnPartOfImg(image, 0.17, 0.68, 0.3, 0.36)
        base64_image_4 = encode_image(casA)
        info_casA = get_image_info_openai(base64_image_4, prompt_casA)
        # info_casA = get_image_info_gemini(casA, prompt_casA)

        casB = returnPartOfImg(image, 0.17, 0.68, 0.64, 0.7)
        base64_image_5 = encode_image(casB)
        info_casB = get_image_info_openai(base64_image_5, prompt_casB)
        # info_casB = get_image_info_gemini(casB, prompt_casB)
        return {
            "infos_constat": infos,
            "infos_voiture_A": info_voiture_A,
            "infos_vue_A": info_vue_A,
            "infos_casA": info_casA,
            "infos_voiture_B": info_voiture_B,
            "infos_vue_B": info_vue_B,
            "infos_casB": info_casB
    }

def group_files(images_bytes, file_names):
    #prompts
    grouping_prompt = load_prompt('prompts/grouping_prompt.txt')
    car_prompt = load_prompt('prompts/car_grouping_prompt.txt')
    images_with_index = {}
    i = 0
    content = []
    for image_bytes, file_name in zip(images_bytes, file_names):
        image = base64.b64encode(image_bytes).decode("utf-8")
        images_with_index[i+1] = file_name
        content.append({"type": "text", "text": str(i+1) + ": "})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
        i += 1

    content.append({"type": "text", "text": grouping_prompt})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": content
        }],
        max_tokens=300,
        temperature=0.2
    )
    model_res = gpt_resp_to_dict(response.choices[0].message.content.strip())
    
    for key, value in model_res.items():
        model_res[key] = [images_with_index[number] for number in value]
    
    car_images = model_res["images voitures"]
    content2 = []
    images_with_index = {}
    i = 0
    for car_image in car_images:
        # get index of the image from the file_names list
        index = file_names.index(car_image)
        image_bytes = images_bytes[index]
        image = base64.b64encode(image_bytes).decode("utf-8")
        images_with_index[i+1] = file_names[index]
        content2.append({"type": "text", "text": str(i+1) + ": "})
        content2.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
        i += 1
        
    content2.append({"type": "text", "text": car_prompt})
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": content2
        }],
        max_tokens=300,
        temperature=0.2
    )
    model_res["images voitures"] = gpt_resp_to_dict(response2.choices[0].message.content.strip())
    for key, value in model_res["images voitures"].items():
        model_res["images voitures"][key] = [images_with_index[number] for number in value]

    return model_res


def get_image_by_name(images, name, file_names):
    for image, file_name in zip(images, file_names):
        if file_name == name:
            return image