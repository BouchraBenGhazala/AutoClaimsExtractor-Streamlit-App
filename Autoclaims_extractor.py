import streamlit as st
from functions import *

st.set_page_config(layout="wide", page_title="AutoClaims Extractor", page_icon="sygma_favicon.png")

st.markdown("<h1 style='color:#077d81;'>AutoClaims Extractor</h1>", unsafe_allow_html=True)



with st.sidebar:
    # st.image("sygma_logo.png")
    st.markdown("# AutoClaims Extractor")
    st.markdown("This app uses AI to **automate the process of accident claims** by **grouping images** and **extracting information** from them.")
    # st.markdown("[Sygma.AI](https://sygma.ai/)")
    st.markdown("Made by **Bouchra BENGHAZALA** 💖")

# Load the prompt
with open('prompts/prompt_permis.txt', 'r') as file:
    prompt_permis = file.read()
with open('prompts/prompt_carte_grise.txt', 'r') as file: 
    prompt_carte_grise = file.read()
with open('prompts/car_information.txt', 'r') as file: 
    prompt_car_infos = file.read()

images = st.file_uploader("Upload image files to automate the process of accident claims...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

images_bytes= []

if images:
    with st.spinner("Processing..."):
        file_names = []
        for image in images:
            images_bytes.append(image.read())
            file_names.append(image.name)
        res = group_files(images_bytes, file_names)

    st.markdown("## Grouped images:")
    with st.expander("Car's images", expanded=False):
        col_a, col_b = st.columns(2)
        nb_images_a = len(res["images voitures"]["A"])
        nb_images_b = len(res["images voitures"]["B"])
        is_cars = nb_images_a > 0 or nb_images_b > 0 

        if nb_images_a > 0:
            tabs_a = col_a.tabs([f"Image {i+1}" for i in range(nb_images_a)])
            for i in range(nb_images_a):
                with tabs_a[i]:
                    image=get_image_by_name(images, res["images voitures"]["A"][i], file_names=file_names)
                    resized_image=resize_image(Image.open(image))
                    base64_image = encode_image2(resized_image)
                    st.markdown(f'<img src="data:image/png;base64,{base64_image}" class="uploaded-image">', unsafe_allow_html=True)
                    # st.write(get_image_info_openai(base64_image, prompt_car_infos))
                    st.write(get_image_info_gemini2(base64_image, prompt_car_infos))
                    
        else:
            col_a.warning("No image found for the first car!")

        if nb_images_b > 0:
            tabs_b = col_b.tabs([f"Image {i+1}" for i in range(nb_images_b)])
            for i in range(nb_images_b):
                with tabs_b[i]:
                    image=get_image_by_name(images, res["images voitures"]["B"][i], file_names=file_names)
                    resized_image=resize_image(Image.open(image))
                    base64_image = encode_image2(resized_image)
                    st.markdown(f'<img src="data:image/png;base64,{base64_image}" class="uploaded-image">', unsafe_allow_html=True)
                    # st.write(get_image_info_openai(base64_image, prompt_car_infos))
                    st.write(get_image_info_gemini(base64_image, prompt_car_infos))
        else:
            col_b.warning("No image found for the second car!")
    
    with st.expander("Accident report", expanded=False):
        nb_constat= len(res["constat"])
        if nb_constat==1:
            constat_image = get_image_by_name(images, res["constat"][0], file_names=file_names)
            st.image(constat_image)
            st.markdown("<h4 style='color:#077d81;'>Extracted information</h4>", unsafe_allow_html=True)
            # Convert the image to a format suitable for processing
            image_pil = Image.open(constat_image)
            image_np = np.array(image_pil)
            # Process the accident report
            resp = process_constat(image_np)

            st.markdown("<h6 style='color:#077d81;'>Accident report information</h6>", unsafe_allow_html=True)
            st.write(resp['infos_constat'])
            col1, col2 = st.columns(2)
            col1.markdown("<h6 style='color:#077d81;'>Car A information</h6>", unsafe_allow_html=True)
            col1.write(resp['infos_voiture_A'])
            col1.markdown("<h6 style='color:#077d81;'>Car B information</h6>", unsafe_allow_html=True)
            col1.write(resp['infos_vue_A'])
            col1.markdown("<h6 style='color:#077d81;'>Check boxes for car A</h6>", unsafe_allow_html=True)
            col1.write(resp['infos_casA'])
            col2.markdown("<h6 style='color:#077d81;'>Check boxes for car A</h6>", unsafe_allow_html=True)
            col2.write(resp['infos_voiture_B'])
            col2.markdown("<h6 style='color:#077d81;'>View information for car A</h6>", unsafe_allow_html=True)
            col2.write(resp['infos_vue_B'])
            col2.markdown("<h6 style='color:#077d81;'>View information for car A</h6>", unsafe_allow_html=True)
            col2.write(resp['infos_casB'])
        elif nb_constat>1:
            st.warning("Please provide just one accident report image!")
        else:
            st.markdown(":red[No accident report image found!]")
    
    with st.expander("Driving license", expanded=False):
        nb_permis= len(res["permis"])
        if nb_permis==2:
            permis_1=get_image_by_name(images, res["permis"][0], file_names=file_names)
            permis_2=get_image_by_name(images, res["permis"][1], file_names=file_names)
            image1=Image.open(permis_1)
            image2=Image.open(permis_2)
            resized_image1 = resize_image(image1)
            resized_image2 = resize_image(image2)
            base64_image1 = encode_image2(resized_image1)
            base64_image2 = encode_image2(resized_image2)
            col1, col2 = st.columns(2)
            cv_image_1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
            cv_image_2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
            col1.markdown(f'<img src="data:image/png;base64,{base64_image1}" class="uploaded-image">', unsafe_allow_html=True)
            col2.markdown(f'<img src="data:image/png;base64,{base64_image2}" class="uploaded-image">', unsafe_allow_html=True)
            # col1.write(get_image_info_openai(base64_image1, prompt_permis))
            # col2.write(get_image_info_openai(base64_image2, prompt_permis))
            col1.write(get_image_info_gemini(base64_image1, prompt_permis))
            col2.write(get_image_info_gemini(base64_image2, prompt_permis))



        elif nb_permis==1 or nb_permis>2:
            st.warning("Please provide two driving license images (Front and Back)!")
        else:
            st.markdown(":red[No driving license images found!]")
    
    with st.expander("Car registration", expanded=False):
        nb_carte_grise= len(res["carte grise"])
        if nb_carte_grise==2:
            carte_grise_1=get_image_by_name(images, res["carte grise"][0], file_names=file_names)
            carte_grise_2=get_image_by_name(images, res["carte grise"][1], file_names=file_names)
            image1=Image.open(carte_grise_1)
            image2=Image.open(carte_grise_2)
            resized_image1 = resize_image(image1)
            resized_image2 = resize_image(image2)
            base64_image1 = encode_image2(resized_image1)
            base64_image2 = encode_image2(resized_image2)
            col1, col2 = st.columns(2)
            cv_image_1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
            cv_image_2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
            col1.markdown(f'<img src="data:image/png;base64,{base64_image1}" class="uploaded-image">', unsafe_allow_html=True)
            col2.markdown(f'<img src="data:image/png;base64,{base64_image2}" class="uploaded-image">', unsafe_allow_html=True)
            # col1.write(get_image_info_openai(base64_image1, prompt_carte_grise))
            # col2.write(get_image_info_openai(base64_image2, prompt_carte_grise))
            col1.write(get_image_info_gemini(base64_image1, prompt_carte_grise))
            col2.write(get_image_info_gemini(base64_image2, prompt_carte_grise))

        elif nb_carte_grise==1 or nb_carte_grise>2:
            st.warning("Please provide two car registration images (Front and Back)!")
        else:
            st.markdown(":red[No car registration images found!]")
        
    with st.expander("Other images", expanded=False):
        nb_images_autres = len(res["autres"])
        if nb_images_autres > 0:
            tabs_autres = st.tabs([f"Image {i+1}" for i in range(nb_images_autres)])
            for i in range(nb_images_autres):
                with tabs_autres[i]:
                    st.image(get_image_by_name(images, res["autres"][i], file_names=file_names))
        else:
            st.markdown(":gray[No other type of images found!]")