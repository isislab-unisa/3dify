# import torch
# from torch import nn
# from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
# import base64
# from PIL import Image
# import matplotlib.pyplot as plt
# from io import BytesIO
# import cv2
# import numpy as np

# device = (
#     torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
# )

# def open_base64_image_to_PIL(base64_image):
#     image_data = base64.b64decode(base64_image)
#     image = Image.open(BytesIO(image_data))
#     return image

# def pil_to_cv2(pil_image):
#     cv2_image = np.array(pil_image)
#     cv2_image = cv2_image[:, :, ::-1].copy()
#     return cv2_image

# def inferFaceShapeSliders(imageBase64, gender):
#     #Convert Base64 to Image
#     image = open_base64_image_to_PIL(imageBase64)
#     #Load the model
#     image_processor = SegformerImageProcessor.from_pretrained("jonathandinu/face-parsing")
#     model = SegformerForSemanticSegmentation.from_pretrained("jonathandinu/face-parsing").to(device)
    
#     #Run inference on image
#     inputs = image_processor(images=image, return_tensors="pt").to(device)
#     outputs = model(**inputs)
#     logits = outputs.logits
    
#     #Resize output to match input image dimensions
#     upsampled_logits = nn.functional.interpolate(
#         logits,
#         size = image.size[::-1],
#         mode = "bilinear",
#         align_corners = False,
#     )
    
#     #get label mask
#     labels = upsampled_logits.argmax(dim=1)[0]
    
    
#     category_mask = labels.cpu().numpy()
    
#     cv2_image = pil_to_cv2(image)

#     desired_labels = [
#         1,  # skin
#         2,  # nose
#         3,  # eyeglasses
#         4,  # l_eye
#         5,  # r_eye
#         6,  # l_brow
#         7,  # r_brow
#         # 8,  # l_ear
#         # 9,  # r_ear
#         10,  # mouth
#         11,  # u_lip
#         12,  # l_lip
#         # 13,  # hair
#         # 17,  # neck
#     ]
    
#     mask = np.where(np.isin(category_mask, desired_labels), 255, 0).astype(np.uint8)
    
#     result_image = cv2.bitwise_and(cv2_image, cv2_image, mask=mask)
    
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     if contours:
#         largest_contour = max(contours, key=cv2.contourArea)
#         x, y, w, h = cv2.boundingRect(largest_contour)
        
#         #Upper Left Corner
#         corner_up_sx_x, corner_up_sx_y = x, y
#         #Upper Right Corner
#         corner_up_dx_x, corner_up_dx_y = x + w, y
#         #Lower Left Corner
#         corner_dw_sx_x, corner_dw_sx_y = x, y + h
#         #Lower Right Corner
#         corner_dw_dx_x, corner_dw_dx_y = x + w, y + h
        
        
#         for i in range(min(w, h)):
#             if np.any(result_image[corner_up_sx_y + i, corner_up_sx_x + i] != [0, 0, 0]):
#                 px_up_sx, py_up_sx = corner_up_sx_x + i, corner_up_sx_y + i
#                 break
#             else:
#                 px_up_sx, py_up_sx = corner_up_sx_x + min(w, h) - 1, corner_up_sx_y + min(w, h) - 1
            
#         distanceUpSx = np.sqrt((px_up_sx - corner_up_sx_x)**2 + (py_up_sx - corner_up_sx_y)**2)
        
#         for i in range(min(w, h)):
#             if np.any(result_image[corner_up_dx_y + i, corner_up_dx_x - i] != [0, 0, 0]):
#                 px_up_dx, py_up_dx = corner_up_dx_x - i, corner_up_dx_y + i
#                 break
#             else:
#                 px_up_dx, py_up_dx = corner_up_dx_x + min(w, h) - 1, corner_up_dx_y + min(w, h) - 1
            
#         distanceUpDx = np.sqrt((px_up_dx - corner_up_dx_x)**2 + (py_up_dx - corner_up_dx_y)**2)

#         for i in range(min(w, h)):
#             if np.any(result_image[corner_dw_dx_y - i, corner_dw_dx_x - i] != [0, 0, 0]):
#                 px_dw_dx, py_dw_dx = corner_dw_dx_x - i, corner_dw_dx_y - i
#                 break
#             else:
#                 px_dw_dx, py_dw_dx = corner_dw_dx_x + min(w, h) - 1, corner_dw_dx_y + min(w, h) - 1
            
#         distanceDwDx = np.sqrt((px_dw_dx - corner_dw_dx_x)**2 + (py_dw_dx - corner_dw_dx_y)**2)

#         for i in range(min(w, h)):
#             if np.any(result_image[corner_dw_sx_y - i, corner_dw_sx_x + i] != [0, 0, 0]):
#                 px_dw_sx, py_dw_sx = corner_dw_sx_x + i, corner_dw_sx_y - i
#                 break
#             else:
#                 px_dw_sx, py_dw_sx = corner_dw_sx_x + min(w, h) - 1, corner_dw_sx_y + min(w, h) - 1
            
#         distanceDwSx = np.sqrt((px_dw_sx - corner_dw_sx_x)**2 + (py_dw_sx - corner_dw_sx_y)**2)
        
#         center_x = x + w // 2
#         center_y = y + h // 2
        
#         #Distances
#         max_distance = np.sqrt((center_x - corner_up_sx_x)**2 + (center_y - corner_up_sx_y)**2)
#         distanceUpSx = distanceUpSx / max_distance
#         distanceUpDx = distanceUpDx / max_distance
#         distanceDwDx = distanceDwDx / max_distance
#         distanceDwSx = distanceDwSx / max_distance
        
#         diffWidthHeight = (w - h) / h
#         diffUpDown = (distanceUpSx + distanceUpDx) - (distanceDwSx + distanceDwDx)
#         sumUpDown = (distanceUpSx + distanceUpDx) + (distanceDwSx + distanceDwDx) 
        
#         #Normalized Features
#         roundSlider = (abs(diffWidthHeight) + 0.21)/ (0.33 - 0.21)
#         invTriangSlider = (diffUpDown - (-0.15)) / ((-0.08) - (-0.15))
#         triangSlider = (diffUpDown - (-0.08)) / ((0.22) - (-0.08))
#         diamondSlider = (sumUpDown - 0.98) / (1.22 - 0.98)
#         rectSlider = (sumUpDown - 0.76) / (0.98 - 0.76)
#         faceScaleVert = 2 * ((sumUpDown - 0.76) / (1.22 - 0.76)) - 1
        
#         sliders = {
#             "head/head-round": roundSlider if roundSlider > 0.0 and roundSlider < 1.0 else 0.0,
#             "head/head-invertedtriangular": invTriangSlider if invTriangSlider > 0.0 and invTriangSlider < 1.0 else 0.0,
#             "head/head-triangular": triangSlider if triangSlider > 0.0 and triangSlider < 1.0 else 0.0,
#             "head/head-diamond": diamondSlider if diamondSlider > 0.0 and diamondSlider < 1.0 else 0.0,
#             "head/head-rectangular": rectSlider if gender == "male" and rectSlider > 0.0 and rectSlider < 1.0 else 0.0,
#             "head/head-scale-vert-decr|incr" : faceScaleVert if gender == "female" and faceScaleVert > -1.0 and faceScaleVert < 1.0 else 0.0
#         }
        
#         return sliders

