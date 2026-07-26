import cv2                                   
import numpy as np                           
from paddleocr import PaddleOCR               

_ocr = None                                   


def get_ocr():
    global _ocr                              
    if _ocr is None:                          
        _ocr = PaddleOCR(
            lang='korean',                    
            enable_mkldnn=False,              
            use_doc_orientation_classify=False,  
            use_doc_unwarping=False,             
            use_textline_orientation=False,     
        )
    return _ocr                               


def preprocess(image_path):
    img = cv2.imread(image_path)              
    if img is None:                           
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

    h, w = gray.shape                              
    if w < 1000:                                   
        scale = 1000 / w                           
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)  


    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def extract_texts(image_path):
    img = preprocess(image_path)             
    if img is None:                          
        return []

    result = get_ocr().predict(img)           

    texts = []                              
    for res in result:                        
        texts.extend(res['rec_texts'])        
    return texts