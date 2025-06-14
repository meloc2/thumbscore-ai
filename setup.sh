#!/bin/bash

# ThumbScore AI - Script de Instalação Automática
# Este script configura automaticamente o ambiente de desenvolvimento

echo "🎯 ThumbScore AI - Configuração Automática"
echo "=========================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 20+"
    exit 1
fi

echo "✅ Pré-requisitos verificados"

# Configurar Backend
echo "🔧 Configurando Backend..."
cd backend

# Criar ambiente virtual (opcional)
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate 2>/dev/null || echo "⚠️  Ambiente virtual não ativado (opcional)"

# Instalar dependências do backend
echo "📥 Instalando dependências do backend..."
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "⚙️  Criando arquivo de configuração..."
    cp .env.example .env
fi

cd ..

# Configurar Frontend
echo "🎨 Configurando Frontend..."
cd frontend

# Verificar se pnpm está disponível, senão usar npm
if command -v pnpm &> /dev/null; then
    echo "📥 Instalando dependências com pnpm..."
    pnpm install
    PACKAGE_MANAGER="pnpm"
else
    echo "📥 Instalando dependências com npm..."
    npm install
    PACKAGE_MANAGER="npm"
fi

cd ..

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo "=================================="
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Iniciar o Backend:"
echo "   cd backend"
echo "   PYTHONPATH=\$(pwd) uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "2. Iniciar o Frontend (em outro terminal):"
echo "   cd frontend"
if [ "$PACKAGE_MANAGER" = "pnpm" ]; then
    echo "   pnpm run dev --host"
else
    echo "   npm run dev -- --host"
fi
echo ""
echo "3. Acessar a aplicação:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🚀 Divirta-se otimizando suas thumbnails!"

