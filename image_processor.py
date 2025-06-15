import cv2
import numpy as np
from PIL import Image
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Classe para pré-processamento de imagens"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
        
    def preprocess(self, image: Image.Image) -> np.ndarray:
        """
        Pré-processar imagem para análise
        
        Args:
            image: Imagem PIL
            
        Returns:
            Array numpy da imagem processada
        """
        try:
            # Converter para RGB se necessário
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Redimensionar mantendo proporção
            image = self._resize_with_padding(image)
            
            # Converter para array numpy
            img_array = np.array(image)
            
            # Normalizar valores para 0-1
            img_array = img_array.astype(np.float32) / 255.0
            
            return img_array
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento da imagem: {str(e)}")
            raise
    
    def _resize_with_padding(self, image: Image.Image) -> Image.Image:
        """Redimensionar imagem mantendo proporção com padding"""
        
        # Calcular novo tamanho mantendo proporção
        width, height = image.size
        target_width, target_height = self.target_size
        
        # Calcular escala
        scale = min(target_width / width, target_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Redimensionar
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Criar nova imagem com padding
        new_image = Image.new('RGB', self.target_size, (0, 0, 0))
        
        # Calcular posição para centralizar
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        
        # Colar imagem redimensionada
        new_image.paste(image, (x, y))
        
        return new_image
    
    def extract_features(self, image: np.ndarray) -> dict:
        """
        Extrair características específicas da imagem
        
        Args:
            image: Array numpy da imagem
            
        Returns:
            Dicionário com características extraídas
        """
        try:
            # Converter para uint8 se necessário
            if image.dtype == np.float32:
                img_uint8 = (image * 255).astype(np.uint8)
            else:
                img_uint8 = image
            
            # Converter para diferentes espaços de cor
            hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)
            lab = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2LAB)
            gray = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2GRAY)
            
            features = {}
            
            # Características de cor
            features['mean_hue'] = np.mean(hsv[:, :, 0])
            features['mean_saturation'] = np.mean(hsv[:, :, 1])
            features['mean_value'] = np.mean(hsv[:, :, 2])
            features['mean_lightness'] = np.mean(lab[:, :, 0])
            
            # Características de textura
            features['contrast'] = np.std(gray)
            features['brightness'] = np.mean(gray)
            
            # Características de nitidez
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            features['sharpness'] = np.var(laplacian)
            
            # Características de bordas
            edges = cv2.Canny(gray, 50, 150)
            features['edge_density'] = np.sum(edges > 0) / edges.size
            
            # Características de distribuição de cores
            hist_r = cv2.calcHist([img_uint8], [0], None, [256], [0, 256])
            hist_g = cv2.calcHist([img_uint8], [1], None, [256], [0, 256])
            hist_b = cv2.calcHist([img_uint8], [2], None, [256], [0, 256])
            
            features['color_variance_r'] = np.var(hist_r)
            features['color_variance_g'] = np.var(hist_g)
            features['color_variance_b'] = np.var(hist_b)
            
            return features
            
        except Exception as e:
            logger.error(f"Erro na extração de características: {str(e)}")
            return {}
    
    def detect_faces(self, image: np.ndarray) -> list:
        """
        Detectar rostos na imagem
        
        Args:
            image: Array numpy da imagem
            
        Returns:
            Lista de coordenadas dos rostos detectados
        """
        try:
            # Converter para uint8 se necessário
            if image.dtype == np.float32:
                img_uint8 = (image * 255).astype(np.uint8)
            else:
                img_uint8 = image
            
            gray = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2GRAY)
            
            # Carregar classificador de rostos
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detectar rostos
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            return faces.tolist()
            
        except Exception as e:
            logger.error(f"Erro na detecção de rostos: {str(e)}")
            return []
    
    def analyze_composition(self, image: np.ndarray) -> dict:
        """
        Analisar composição da imagem (regra dos terços, etc.)
        
        Args:
            image: Array numpy da imagem
            
        Returns:
            Dicionário com análise de composição
        """
        try:
            height, width = image.shape[:2]
            
            # Converter para escala de cinza
            if len(image.shape) == 3:
                if image.dtype == np.float32:
                    gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
                else:
                    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Dividir em grade 3x3 para regra dos terços
            third_h = height // 3
            third_w = width // 3
            
            # Calcular interesse em cada seção
            sections = []
            for i in range(3):
                for j in range(3):
                    y1, y2 = i * third_h, (i + 1) * third_h
                    x1, x2 = j * third_w, (j + 1) * third_w
                    section = gray[y1:y2, x1:x2]
                    
                    # Calcular variância como medida de interesse
                    interest = np.var(section)
                    sections.append(interest)
            
            # Pontos de interesse da regra dos terços (interseções)
            rule_of_thirds_points = [
                (third_w, third_h), (2 * third_w, third_h),
                (third_w, 2 * third_h), (2 * third_w, 2 * third_h)
            ]
            
            # Calcular pontuação de composição
            center_interest = sections[4]  # Centro
            corners_interest = (sections[0] + sections[2] + sections[6] + sections[8]) / 4
            thirds_interest = (sections[1] + sections[3] + sections[5] + sections[7]) / 4
            
            composition_score = thirds_interest / (center_interest + 1e-6)
            
            return {
                'composition_score': min(composition_score, 2.0),
                'center_interest': center_interest,
                'rule_of_thirds_adherence': thirds_interest / max(sections),
                'sections_variance': sections
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de composição: {str(e)}")
            return {'composition_score': 1.0, 'center_interest': 0.0, 'rule_of_thirds_adherence': 0.5}

