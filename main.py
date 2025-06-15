from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar serviços
from app.services.thumbnail_analyzer import ThumbnailAnalyzer
from app.core.config import settings

# Criar instância do FastAPI
app = FastAPI(
    title="ThumbScore AI API",
    description="API para análise e pontuação de thumbnails de vídeos usando IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar o analisador de thumbnails
thumbnail_analyzer = ThumbnailAnalyzer()

@app.get("/")
async def root():
    """Endpoint raiz para verificar se a API está funcionando"""
    return {"message": "ThumbScore AI API está funcionando!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da API"""
    return {"status": "healthy", "service": "ThumbScore AI"}

@app.post("/analyze")
async def analyze_thumbnail(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analisar uma thumbnail e retornar pontuação e sugestões
    """
    try:
        # Verificar se o arquivo é uma imagem
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")
        
        # Ler o conteúdo do arquivo
        contents = await file.read()
        
        # Analisar a thumbnail
        result = await thumbnail_analyzer.analyze(contents, file.filename)
        
        return {
            "success": True,
            "filename": file.filename,
            "analysis": result
        }
        
    except Exception as e:
        logger.error(f"Erro ao analisar thumbnail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/batch-analyze")
async def batch_analyze_thumbnails(files: list[UploadFile] = File(...)) -> Dict[str, Any]:
    """
    Analisar múltiplas thumbnails em lote
    """
    try:
        results = []
        
        for file in files:
            if not file.content_type.startswith('image/'):
                continue
                
            contents = await file.read()
            result = await thumbnail_analyzer.analyze(contents, file.filename)
            
            results.append({
                "filename": file.filename,
                "analysis": result
            })
        
        return {
            "success": True,
            "total_analyzed": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Erro ao analisar thumbnails em lote: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """
    Obter métricas de uso da API
    """
    return {
        "total_analyses": thumbnail_analyzer.get_total_analyses(),
        "average_score": thumbnail_analyzer.get_average_score(),
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

