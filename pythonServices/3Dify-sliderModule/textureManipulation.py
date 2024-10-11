import os
import json
import cv2
import numpy as np
import mediapipe as mp
import skimage
from skimage.transform import PiecewiseAffineTransform, warp
from backgroundremover.bg import remove
from io import BytesIO
from scipy.ndimage import uniform_filter
from skimage import color, filters
from PIL import Image, ImageDraw, ImageFilter
import base64

def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img

def calculate_center(points, offset=0):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    center = ((sum(x_coords) / len(points)) + offset, sum(y_coords) / len(points))
    return center


def create_fade_mask(size, center, max_radius, fade_strength):
    mask = Image.new("L", size, 0)
    for y in range(size[1]):
        for x in range(size[0]):
            distance = np.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
            # opacity = 255 - min(255, int((distance / max_radius) * fade_strength))
            opacity = max(0, int((distance / max_radius) * fade_strength))
            mask.putpixel((x, y), opacity)
    return mask

def remove_bg_preserve_alpha(src_img):
    img = src_img
    alpha_channel = img.split()[-1]

    data = BytesIO()
    src_img.save(data, format="PNG")
    data.seek(0)


    model_choices = ["u2net", "u2net_human_seg", "u2netp"]
    removed_bg = remove(
        data.read(),
        model_name=model_choices[0],
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_structure_size=10,
        alpha_matting_base_size=1000,
    )
    
    removed_bg_img = Image.open(BytesIO(removed_bg))
    
    new_alpha = Image.fromarray(np.array(removed_bg_img.split()[-1]))
    combined_alpha = Image.fromarray(np.minimum(np.array(alpha_channel), np.array(new_alpha)))
    
    final_img = Image.new("RGBA", img.size)
    final_img.paste(removed_bg_img.convert("RGB"), (0,0))
    final_img.putalpha(combined_alpha)
    
    return final_img
    
def make_white_transparent(input_image):
    img = input_image
    img = img.convert("RGBA")
    
    datas = img.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img
    
def split_alpha(image):
    if image.mode == "RGBA":
        rgb = image.convert("RGB")
        alpha = image.split()[3]
        return rgb, alpha
    else:
        return image, None
    
def merge_alpha(rgb, alpha):
    if alpha:
        return Image.merge("RGBA", (*rgb.split(), alpha))
    else:
        return rgb

def local_color_transfer(source, target, window_size=100, preserve_contrast=True, contrast_strength=5):
    source_lab = color.rgb2lab(np.array(source) / 255.0)
    target_lab = color.rgb2lab(np.array(target) / 255.0)

    def local_stats(img):
        mean = uniform_filter(img, size=window_size, mode="reflect")
        mean_sq = uniform_filter(img**2, size=window_size, mode="reflect")
        var = mean_sq - mean**2
        return mean, np.sqrt(np.maximum(var, 0))

    source_mean, source_std = local_stats(source_lab)
    target_mean, target_std = local_stats(target_lab)

    if preserve_contrast:
        # Create a mask for high-contrast areas
        gray_source = color.rgb2gray(np.array(source) / 255.0)
        edges = filters.sobel(gray_source)
        contrast_mask = filters.gaussian(edges, sigma=2)
        contrast_mask = np.tanh(contrast_strength * contrast_mask) / np.tanh(contrast_strength)
        contrast_mask = (contrast_mask - contrast_mask.min()) / (contrast_mask.max() - contrast_mask.min())
        
        # Adjust the transfer intensity based on the contrast mask
        transfer_intensity = 1 - contrast_mask
        transfer_intensity = np.dstack([transfer_intensity] * 3)  # Expand to 3 channels

        # Apply local color transfer with varying intensity
        result_lab = source_lab + transfer_intensity * (
            ((source_lab - source_mean) * (target_std / np.maximum(source_std, 1e-6)) + target_mean) - source_lab
        )
    else:
        # Original color transfer
        result_lab = (source_lab - source_mean) * (target_std / np.maximum(source_std, 1e-6)) + target_mean

    result_lab = np.clip(result_lab, 0, 100)
    result_rgb = color.lab2rgb(result_lab) * 255.0
    return Image.fromarray(np.uint8(result_rgb))

def cut_top_bottom(image, top_cut, bottom_cut):
    width, height = image.size
    
    new_height = height - top_cut - bottom_cut
    
    cropped_image = image.crop((0, top_cut, width, height - bottom_cut))
    
    return cropped_image

def create_border_fade_mask(image, border_size=50):
    h, w, _ = np.array(image).shape
    mask = np.ones((h, w), dtype=np.float32)

    # Create gradients for the borders
    for i in range(border_size):
        fade_value = i / border_size
        mask[i, :] *= fade_value  # Top border
        mask[h - i - 1, :] *= fade_value  # Bottom border
        mask[:, i] *= fade_value  # Left border
        mask[:, w - i - 1] *= fade_value  # Right border

    return mask

def blend_face_texture_alpha(body, faceUp, faceDown, face_up_position, face_down_position):
    def blend_face(body, face, position):
        face = face.resize(
            (position[2] - position[0], position[3] - position[1])
        )
        
        if face.mode != "RGBA":
            face = face.convert("RGBA")
            
        mask = face.split()[3]
        
        mask = mask.filter(ImageFilter.GaussianBlur(radius=10))
        
        body.paste(face, position, mask)
    
    blend_face(body, faceUp, face_up_position)
    blend_face(body, faceDown, face_down_position)
    
    return body

def cv2_image_to_base64(image):
    _, buffer = cv2.imencode(".png", image)
    png_as_text = base64.b64encode(buffer)
    return png_as_text.decode("utf-8")

def create_fade_mask_from_start_points(image, start_points, fade_width):
    h, w = image.shape[:2]
    mask = np.ones((h, w), dtype=np.float32)

    for x, y in start_points:
        for i in range(fade_width):
            fade_value = (fade_width - i) / fade_width
            if x - i >= 0:
                mask[:, x - i] *= fade_value

    return mask

def apply_fade_out_from_points(image, fade_width=50):    
    # Assicurati che l'immagine abbia un canale alfa (per la trasparenza)
    if image.shape[2] != 4:
        raise ValueError("The image does not have an alpha channel.")
    
    # Trova i punti di partenza per la dissolvenza (i punti rossi)
    start_points = []
    for y in range(image.shape[0]):
        row_pixel = 0
        for x in range(image.shape[1]):
            r, g, b, a = image[y, x]
            if a != 0:
                row_pixel +=1
                if row_pixel == 5:# Punto rosso
                    start_points.append((x, y))
                    break  # Passa alla prossima riga

    # Crea la maschera di dissolvenza
    fade_mask = create_fade_mask_from_start_points(image, start_points, fade_width)

    # Separa i canali colore e alfa
    b, g, r, a = cv2.split(image)

    # Normalizza la maschera di dissolvenza nell'intervallo [0, 255]
    fade_mask = (fade_mask * 255).astype(np.uint8)

    # Assicurati che il canale alfa e la maschera di dissolvenza siano entrambi di tipo float32
    a = a.astype(np.float32)
    fade_mask = fade_mask.astype(np.float32)

    # Combina il canale alfa con la maschera di dissolvenza
    new_alpha = cv2.multiply(a, fade_mask / 255.0).astype(np.uint8)

    # Unisci i canali di nuovo
    faded_image = cv2.merge((b, g, r, new_alpha))
    
    return faded_image


def createCustomSkin(skinColor, gender, age, image=None):
    uv_path = r"3Dify-sliderModule/mediapipe_models/uv_map.json"
    uv_map_dict = json.load(open(uv_path))
    uv_map = np.array([ (uv_map_dict["u"][str(i)],uv_map_dict["v"][str(i)]) for i in range(468)])

    img_ori = image.copy()
    img_ori = convert(img_ori, 0, 255, np.uint8)

    img = img_ori
    H,W,_ = img.shape
    #run facial landmark detection
    with mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(img)
        
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)


    assert len(results.multi_face_landmarks)==1

    face_landmarks = results.multi_face_landmarks[0]
    keypoints = np.array([(W*point.x,H*point.y) for point in face_landmarks.landmark[0:468]])

    # H_new, W_new = 512,512
    H_new,W_new = 1024,1024
    keypoints_uv = np.array([(W_new*x, H_new*y) for x,y in uv_map])

    tform = PiecewiseAffineTransform()
    tform.estimate(keypoints_uv,keypoints)
    texture = warp(img_ori, tform, output_shape=(H_new,W_new))
    
    #Sharpening filter
    # sharpening_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # texture = cv2.filter2D(texture, -1, sharpening_kernel)
    
    texture = (255*texture).astype(np.uint8)

    #Create a Fading Mask for the eyes
    left_eye_points = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382, 362]
    right_eye_points = [133, 173, 157, 158, 159, 160, 161, 246, 33, 7, 163, 144, 145, 153, 154, 155]

    left_eye_landmarks = [
        (
            (keypoints_uv[idx][0]),
            keypoints_uv[idx][1],
        )
        for idx in left_eye_points
    ]

    right_eye_landmarks = [
        (
            keypoints_uv[idx][0],
            keypoints_uv[idx][1],
        )
        for idx in right_eye_points
    ]

    left_eye_center = calculate_center(left_eye_landmarks)
    right_eye_center = calculate_center(right_eye_landmarks)

    #Fade Mask Parameters
    max_radius = 25
    fade_strength = 100

    left_eye_fade_mask = create_fade_mask(
        (W_new, H_new), left_eye_center, max_radius, fade_strength
    )
    right_eye_fade_mask = create_fade_mask(
        (W_new, H_new), right_eye_center, max_radius, fade_strength
    )

    left_eye_fade_mask_np = np.array(left_eye_fade_mask)
    right_eye_fade_mask_np = np.array(right_eye_fade_mask)
    combined_fade_mask_np = np.bitwise_and(left_eye_fade_mask_np, right_eye_fade_mask_np)

    #Apply the fade mask to the texture of the face
    img_rgba = cv2.cvtColor(texture, cv2.COLOR_RGB2RGBA)
    img_rgba[:, :, 3] = combined_fade_mask_np

    uvMapPIL = Image.fromarray(img_rgba)

    #Remove Background from texture while preserving alpha channel
    faceNoBG = remove_bg_preserve_alpha(uvMapPIL)

    #Delete noisy pixels from the sides of the texture
    image = faceNoBG
    image = image.convert("RGBA")

    mask = Image.new("L", image.size, 0)

    draw = ImageDraw.Draw(mask)

    border_width = 70

    draw.rectangle([0,0, border_width, image.height], fill=255)
    draw.rectangle([image.width - border_width, 0, image.width, image.height], fill=255)
        
    mask = mask.convert('1')

    image.paste(mask , mask=mask)

    faceNoBGTransparentSide = image
        
    faceNoBGTransparent = make_white_transparent(faceNoBGTransparentSide)

    #Transfer the color from the makehuman skin to the face texture
    source = faceNoBGTransparent
    source = source.rotate(90)
    source = source.resize((512, 512), Image.LANCZOS)
    source_rgb, source_alpha = split_alpha(source)
    face_position = (1518, 798, 1518 + source.width, 798 + source.height)
    skins = {
        "light": {
            "male": {
                "old": r"3Dify-sliderModule/original_skins/old_lightskinned_male_diffuse.png",
                "middleAge": r"3Dify-sliderModule/original_skins/middleage_lightskinned_male_diffuse.png",
            },
            "female": {
                "old": r"3Dify-sliderModule/original_skins/old_lightskinned_female_diffuse.png",
                "middleAge": r"3Dify-sliderModule/original_skins/middleage_lightskinned_female_diffuse.png",
            },
        },
        "dark": {
            "male": {
                "old": r"3Dify-sliderModule/original_skins/old_darkskinned_male_diffuse.png",
                "middleAge": r"3Dify-sliderModule/original_skins/middleage_darkskinned_male_diffuse.png",
            },
            "female": {
                "old": r"3Dify-sliderModule/original_skins/old_darkskinned_female_diffuse.png",
                "middleAge": r"3Dify-sliderModule/original_skins/middleage_darkskinned_female_diffuse.png",
            },

        }
    }
    gender = "male"
    age = 35.0

    base_skin = skins["dark" if skinColor == 1 else "light"][gender]["middleAge" if age < 60 else "old"]
    target = Image.open(base_skin).crop(face_position)
    result = local_color_transfer(source_rgb, target)
    result = merge_alpha(result, source_alpha)
    color_matched_face = result
    source = color_matched_face
    cut_image = cut_top_bottom(source, 85, 85)


    #Cut the face texture in half to better position it on the base skin
    img = cut_image

    width, height = img.size
    width_part = width // 1.75

    left_part = img.crop((0, 0, width_part, height))

    right_part = img.crop((width_part, 0, width, height))

    #Create a light fade mask around the border of the two pieces of texture
    image = left_part
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)

    if np.array(image).shape[2] != 4:
        raise ValueError("The image does not have an alpha channel.")

    border_fade_mask = create_border_fade_mask(image, border_size=65)
    b, g, r, a = cv2.split(image)
    border_fade_mask = (border_fade_mask * 255).astype(np.uint8)
    new_alpha = cv2.bitwise_and(a, border_fade_mask)
    faded_image = cv2.merge((b, g, r, new_alpha))
    left_part_faded = faded_image
    left_part_faded = apply_fade_out_from_points(left_part_faded, fade_width=50)

    image = right_part
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)
    border_fade_mask = create_border_fade_mask(image, border_size=35)
    b, g, r, a = cv2.split(image)
    border_fade_mask = (border_fade_mask * 255).astype(np.uint8)
    new_alpha = cv2.bitwise_and(a, border_fade_mask)
    faded_image = cv2.merge((b, g, r, new_alpha))
    right_part_faded = faded_image

    #Stretch the left face texture to fit the base skin
    left_part_faded = cv2.resize(left_part_faded, (214, 344), interpolation=cv2.INTER_LINEAR)
    
    #Compression up-down
    compression_factor = 0.8
    new_height_left = int(left_part_faded.shape[0] * compression_factor)
    new_height_right = int(right_part_faded.shape[0] * compression_factor)
    
    left_part_faded = cv2.resize(left_part_faded, (left_part_faded.shape[1], new_height_left), interpolation=cv2.INTER_LINEAR)
    right_part_faded = cv2.resize(right_part_faded, (right_part_faded.shape[1], new_height_right), interpolation=cv2.INTER_LINEAR)
    
    #Blend the face texture on the base skin selected
    body_texture = Image.open(base_skin)
    face_up_texture = left_part_faded
    face_up_texture = Image.fromarray(cv2.cvtColor(face_up_texture, cv2.COLOR_BGRA2RGBA))
    face_down_texture = right_part_faded
    face_down_texture = Image.fromarray(cv2.cvtColor(face_down_texture, cv2.COLOR_BGRA2RGBA))
    # face_up_position = (1572, 888, 1572 + face_up_texture.width, 888 + face_up_texture.height)
    # face_down_position = (1795, 885, 1795 + face_down_texture.width, 885 + face_down_texture.height)
    
    face_up_position = (1574, 920, 1574 + face_up_texture.width, 920 + face_up_texture.height)
    face_down_position = (1802, 921, 1802 + face_down_texture.width, 921 + face_down_texture.height)



    result = blend_face_texture_alpha(body_texture, face_up_texture, face_down_texture, face_up_position, face_down_position)
    result = cv2.cvtColor(np.array(result), cv2.COLOR_RGBA2BGRA)
    base64_result = cv2_image_to_base64(np.array(result))
    return base64_result