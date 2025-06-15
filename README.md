# ThumbScore AI - Arquitetura do Sistema

## 1. Visão Geral

O ThumbScore AI será um aplicativo web que permitirá aos criadores de conteúdo fazer upload de miniaturas de vídeo, receber uma pontuação de desempenho visual e obter sugestões de melhoria. O sistema será composto por um backend robusto para processamento de IA e um frontend responsivo para interação do usuário.

## 2. Componentes Principais

- **Frontend:** Interface do usuário para upload de imagens, visualização de resultados e sugestões.
- **Backend (API):** Lógica de negócios, orquestração de chamadas de IA, gerenciamento de usuários e dados.
- **Módulo de Machine Learning (ML):** Contém os modelos de IA para análise e pontuação de miniaturas.
- **Banco de Dados:** Armazenamento de informações de usuários, histórico de análises e dados de treinamento (futuro).

## 3. Tecnologias Escolhidas

- **Backend:** FastAPI (Python) - Escolhido pela alta performance, facilidade de uso e documentação automática (Swagger/OpenAPI).
- **Frontend:** React (JavaScript) - Escolhido pela flexibilidade, ecossistema rico e capacidade de criar interfaces de usuário complexas e responsivas.
- **Machine Learning:**
    - **OpenCV:** Para pré-processamento de imagem (redimensionamento, normalização, detecção de características).
    - **TensorFlow/Keras:** Para o modelo de pontuação de performance visual (treinado com dados de miniaturas virais).
    - **GPT-4 Vision (via API):** Para interpretação contextual e geração de sugestões de melhoria baseadas em linguagem natural.
- **Banco de Dados:** SQLite (inicialmente para prototipagem), com possibilidade de migração para PostgreSQL ou MongoDB para escalabilidade.

## 4. Fluxo de Dados (Exemplo: Análise de Miniatura)

1. O usuário faz upload de uma miniatura através da interface do frontend.
2. O frontend envia a imagem para o endpoint `/analyze` do backend (FastAPI).
3. O backend recebe a imagem e a encaminha para o módulo de ML.
4. O módulo de ML:
    a. Utiliza OpenCV para pré-processar a imagem.
    b. Aplica o modelo TensorFlow para gerar a pontuação de performance visual.
    c. Envia a imagem e a pontuação para a API do GPT-4 Vision para obter sugestões contextuais.
5. O módulo de ML retorna a pontuação e as sugestões para o backend.
6. O backend envia os resultados de volta para o frontend.
7. O frontend exibe a pontuação e as sugestões ao usuário.

## 5. Estrutura de Pastas (Proposta Inicial)

```
thumbscore-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── ml/
│   │   ├── models/
│   │   ├── preprocessing/
│   │   └── __init__.py
│   ├── tests/
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── .gitignore
└── README.md
```


