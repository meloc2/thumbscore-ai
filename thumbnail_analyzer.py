import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, Tuple
import asyncio
from datetime import datetime

# Importar módulos de ML
from ml.preprocessing.image_processor import ImageProcessor
from ml.models.score_predictor import ScorePredictor
from ..core.config import settings

logger = logging.getLogger(__name__)

class ThumbnailAnalyzer:
    """Serviço principal para análise de thumbnails"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.score_predictor = ScorePredictor()
        self.total_analyses = 0
        self.scores_history = []
        
    async def analyze(self, image_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Analisar uma thumbnail e retornar pontuação completa
        """
        try:
            # Converter bytes para imagem PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # Pré-processar a imagem
            processed_image = self.image_processor.preprocess(image)
            
            # Análise básica da imagem
            basic_analysis = self._analyze_basic_features(processed_image)
            
            # Gerar pontuação usando ML
            ml_score = await self.score_predictor.predict_score(processed_image)
            
            # Análise contextual (simulada por enquanto)
            contextual_analysis = await self._analyze_contextual_features(image)
            
            # Combinar todas as análises
            final_score = self._calculate_final_score(basic_analysis, ml_score, contextual_analysis)
            
            # Gerar sugestões
            suggestions = self._generate_suggestions(basic_analysis, contextual_analysis, final_score)
            
            # Atualizar estatísticas
            self.total_analyses += 1
            self.scores_history.append(final_score)
            
            return {
                "score": final_score,
                "breakdown": {
                    "visual_impact": basic_analysis["visual_impact"],
                    "clarity": basic_analysis["clarity"],
                    "contrast": basic_analysis["contrast"],
                    "color_harmony": basic_analysis["color_harmony"],
                    "composition": contextual_analysis["composition"],
                    "text_readability": contextual_analysis["text_readability"]
                },
                "suggestions": suggestions,
                "analysis_timestamp": datetime.now().isoformat(),
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"Erro na análise da thumbnail {filename}: {str(e)}")
            raise
    
    def _analyze_basic_features(self, image: np.ndarray) -> Dict[str, float]:
        """Análise de características básicas da imagem"""
        
        # Converter para diferentes espaços de cor
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        
        # Calcular contraste
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        contrast = np.std(gray) / 255.0
        
        # Calcular saturação média
        saturation = np.mean(hsv[:, :, 1]) / 255.0
        
        # Calcular brilho
        brightness = np.mean(lab[:, :, 0]) / 255.0
        
        # Calcular nitidez (usando Laplacian)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        clarity = np.var(laplacian) / 10000.0  # Normalizar
        
        # Análise de cores dominantes
        color_harmony = self._calculate_color_harmony(image)
        
        # Impacto visual (combinação de fatores)
        visual_impact = (contrast * 0.3 + saturation * 0.3 + clarity * 0.4)
        
        return {
            "visual_impact": min(visual_impact * 100, 100),
            "clarity": min(clarity * 100, 100),
            "contrast": min(contrast * 100, 100),
            "color_harmony": color_harmony,
            "brightness": brightness * 100,
            "saturation": saturation * 100
        }
    
    def _calculate_color_harmony(self, image: np.ndarray) -> float:
        """Calcular harmonia de cores"""
        # Reduzir para cores dominantes
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        # K-means para encontrar cores dominantes
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(data, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Calcular distribuição de cores
        unique, counts = np.unique(labels, return_counts=True)
        color_distribution = counts / len(labels)
        
        # Harmonia baseada na distribuição (mais equilibrada = melhor)
        harmony = 1 - np.std(color_distribution)
        
        return harmony * 100
    
    async def _analyze_contextual_features(self, image: Image.Image) -> Dict[str, float]:
        """Análise contextual usando características avançadas"""
        
        # Simular análise de composição
        composition_score = np.random.uniform(60, 95)  # Placeholder
        
        # Simular análise de legibilidade de texto
        text_readability = np.random.uniform(70, 90)  # Placeholder
        
        # Em uma implementação real, aqui seria usado GPT-4 Vision
        # para análise contextual mais sofisticada
        
        return {
            "composition": composition_score,
            "text_readability": text_readability,
            "emotional_appeal": np.random.uniform(65, 85),
            "brand_consistency": np.random.uniform(70, 90)
        }
    
    def _calculate_final_score(self, basic: Dict, ml_score: float, contextual: Dict) -> float:
        """Calcular pontuação final combinando todas as análises"""
        
        # Pesos para diferentes componentes
        weights = {
            "basic": 0.4,
            "ml": 0.35,
            "contextual": 0.25
        }
        
        # Média ponderada das características básicas
        basic_avg = (
            basic["visual_impact"] * 0.3 +
            basic["clarity"] * 0.25 +
            basic["contrast"] * 0.25 +
            basic["color_harmony"] * 0.2
        )
        
        # Média das características contextuais
        contextual_avg = (
            contextual["composition"] * 0.4 +
            contextual["text_readability"] * 0.3 +
            contextual["emotional_appeal"] * 0.3
        )
        
        # Pontuação final
        final_score = (
            basic_avg * weights["basic"] +
            ml_score * weights["ml"] +
            contextual_avg * weights["contextual"]
        )
        
        return round(min(final_score, 100), 1)
    
    def _generate_suggestions(self, basic: Dict, contextual: Dict, final_score: float) -> list:
        """Gerar sugestões de melhoria baseadas na análise"""
        suggestions = []
        
        if basic["contrast"] < 60:
            suggestions.append("Aumente o contraste para melhorar a legibilidade")
        
        if basic["clarity"] < 50:
            suggestions.append("Use uma imagem mais nítida para melhor impacto visual")
        
        if basic["color_harmony"] < 70:
            suggestions.append("Considere usar uma paleta de cores mais harmoniosa")
        
        if contextual["composition"] < 70:
            suggestions.append("Melhore a composição seguindo a regra dos terços")
        
        if contextual["text_readability"] < 75:
            suggestions.append("Torne o texto mais legível com melhor contraste ou tamanho")
        
        if final_score > 85:
            suggestions.append("Excelente thumbnail! Pequenos ajustes podem torná-la ainda melhor")
        elif final_score > 70:
            suggestions.append("Boa thumbnail! Algumas melhorias podem aumentar o CTR")
        else:
            suggestions.append("Esta thumbnail precisa de melhorias significativas para melhor performance")
        
        return suggestions
    
    def get_total_analyses(self) -> int:
        """Retornar total de análises realizadas"""
        return self.total_analyses
    
    def get_average_score(self) -> float:
        """Retornar pontuação média de todas as análises"""
        if not self.scores_history:
            return 0.0
        return round(sum(self.scores_history) / len(self.scores_history), 1)

