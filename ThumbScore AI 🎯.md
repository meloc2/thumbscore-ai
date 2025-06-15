# ThumbScore AI 🎯

**Otimize suas thumbnails com Inteligência Artificial**

O ThumbScore AI é um aplicativo inovador que utiliza machine learning para analisar e pontuar thumbnails de vídeos, ajudando criadores de conteúdo a aumentar suas taxas de clique (CTR) com insights baseados em dados reais de thumbnails virais.

![ThumbScore AI Interface](frontend/src/assets/screenshot.png)

## ✨ Características Principais

- **🤖 Análise com IA Avançada**: Modelos treinados com milhares de thumbnails virais
- **📊 Pontuação Detalhada**: Avaliação completa de impacto visual, contraste, composição e legibilidade
- **🎨 Interface Futurista**: Design moderno e responsivo para desktop e mobile
- **⚡ Processamento Rápido**: Análise em tempo real com feedback instantâneo
- **📈 Métricas Precisas**: Pontuação baseada em dados reais de performance
- **💡 Sugestões Inteligentes**: Recomendações personalizadas para melhorar suas thumbnails

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido para Python
- **TensorFlow**: Modelos de machine learning para análise de imagem
- **OpenCV**: Processamento avançado de imagem
- **Pillow**: Manipulação de imagens
- **Uvicorn**: Servidor ASGI de alta performance

### Frontend
- **React**: Biblioteca JavaScript para interfaces de usuário
- **Tailwind CSS**: Framework CSS utilitário
- **Shadcn/UI**: Componentes de interface modernos
- **Lucide Icons**: Ícones elegantes e consistentes
- **Vite**: Build tool rápido e moderno

### Machine Learning
- **Análise de Características Visuais**: Contraste, brilho, saturação, nitidez
- **Detecção de Composição**: Regra dos terços, distribuição de elementos
- **Processamento de Cores**: Harmonia cromática e impacto visual
- **Análise Contextual**: Avaliação de legibilidade e apelo emocional

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- pnpm ou npm

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/thumbscore-ai.git
cd thumbscore-ai
```

### 2. Configuração do Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (opcional)
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Iniciar o servidor
PYTHONPATH=/caminho/para/thumbscore-ai/backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Configuração do Frontend

```bash
cd frontend

# Instalar dependências
pnpm install

# Iniciar o servidor de desenvolvimento
pnpm run dev --host
```

### 4. Acessar a Aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 📖 Como Usar

### 1. Upload de Thumbnail
- Acesse a interface web
- Arraste e solte sua thumbnail na área de upload ou clique para selecionar
- Formatos suportados: JPG, PNG, WebP

### 2. Análise Automática
- Clique em "Analisar Thumbnail"
- Aguarde o processamento (geralmente 2-5 segundos)
- Visualize os resultados detalhados

### 3. Interpretação dos Resultados

#### Pontuação Geral (0-100)
- **85-100**: Excelente - Thumbnail otimizada para alto CTR
- **70-84**: Boa - Algumas melhorias podem aumentar a performance
- **0-69**: Precisa Melhorar - Requer ajustes significativos

#### Métricas Detalhadas
- **Impacto Visual**: Capacidade de chamar atenção
- **Clareza**: Nitidez e qualidade da imagem
- **Contraste**: Diferenciação entre elementos
- **Harmonia de Cores**: Equilíbrio cromático
- **Composição**: Distribuição e posicionamento dos elementos
- **Legibilidade do Texto**: Facilidade de leitura

### 4. Aplicar Sugestões
- Revise as sugestões personalizadas
- Implemente as melhorias recomendadas
- Teste novamente para comparar resultados

## 🔧 API Endpoints

### Análise de Thumbnail
```http
POST /analyze
Content-Type: multipart/form-data

{
  "file": "thumbnail.jpg"
}
```

**Resposta:**
```json
{
  "success": true,
  "filename": "thumbnail.jpg",
  "analysis": {
    "score": 87.3,
    "breakdown": {
      "visual_impact": 92,
      "clarity": 85,
      "contrast": 89,
      "color_harmony": 84,
      "composition": 88,
      "text_readability": 82
    },
    "suggestions": [
      "Excelente thumbnail! Pequenos ajustes podem torná-la ainda melhor",
      "Considere aumentar ligeiramente o contraste do texto"
    ]
  }
}
```

### Análise em Lote
```http
POST /batch-analyze
Content-Type: multipart/form-data

{
  "files": ["thumb1.jpg", "thumb2.jpg", ...]
}
```

### Verificação de Saúde
```http
GET /health
```

### Métricas da API
```http
GET /metrics
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   ML Engine     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (TensorFlow)  │
│                 │    │                 │    │                 │
│ • Interface UI  │    │ • API REST      │    │ • Análise CV    │
│ • Upload        │    │ • Validação     │    │ • Pontuação ML  │
│ • Resultados    │    │ • Orquestração  │    │ • Processamento │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧪 Testes

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
pnpm test
```

## 📦 Deploy

### Opção 1: Docker (Recomendado)
```bash
# Build das imagens
docker-compose build

# Iniciar os serviços
docker-compose up -d
```

### Opção 2: Deploy Manual

#### Backend (Heroku/Railway/DigitalOcean)
```bash
# Configurar variáveis de ambiente
export PYTHONPATH=/app
export PORT=8000

# Iniciar aplicação
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Frontend (Vercel/Netlify)
```bash
# Build de produção
pnpm build

# Deploy da pasta dist/
```

## 🔮 Roadmap Futuro

### Versão 2.0
- [ ] **Integração GPT-4 Vision**: Análise contextual avançada
- [ ] **Banco de Dados**: Histórico de análises e comparações
- [ ] **A/B Testing**: Comparação entre diferentes versões
- [ ] **API de Terceiros**: Integração com YouTube Analytics

### Versão 3.0
- [ ] **Geração Automática**: Criação de thumbnails otimizadas
- [ ] **Análise de Tendências**: Insights baseados em dados do mercado
- [ ] **Personalização por Nicho**: Modelos específicos por categoria
- [ ] **Dashboard Analytics**: Métricas de performance em tempo real

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: Manus AI
- **Especialista em ML**: Análise de Imagem e Computer Vision
- **Designer UI/UX**: Interface Moderna e Responsiva

## 📞 Suporte

- **Email**: suporte@thumbscore.ai
- **Discord**: [Comunidade ThumbScore](https://discord.gg/thumbscore)
- **Documentação**: [docs.thumbscore.ai](https://docs.thumbscore.ai)

## 🙏 Agradecimentos

- Comunidade de criadores de conteúdo que inspirou este projeto
- Datasets públicos de thumbnails para treinamento dos modelos
- Bibliotecas open-source que tornaram este projeto possível

---

**Desenvolvido com ❤️ para criadores de conteúdo que querem maximizar seu alcance**

*ThumbScore AI - Transforme suas thumbnails em ímãs de cliques!* 🎯✨

