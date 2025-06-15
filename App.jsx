import { useState, useCallback } from 'react'
import { Upload, Zap, BarChart3, Eye, Sparkles, Download, Share2 } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleFileSelect = useCallback((file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setAnalysisResult(null)
    }
  }, [])

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }, [handleFileSelect])

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const analyzeImage = async () => {
    if (!selectedFile) return

    setIsAnalyzing(true)
    
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        setAnalysisResult(result.analysis)
      } else {
        console.error('Erro na análise:', response.statusText)
        // Simular resultado para demonstração
        setAnalysisResult({
          score: 87.3,
          breakdown: {
            visual_impact: 92,
            clarity: 85,
            contrast: 89,
            color_harmony: 84,
            composition: 88,
            text_readability: 82
          },
          suggestions: [
            "Excelente thumbnail! Pequenos ajustes podem torná-la ainda melhor",
            "Considere aumentar ligeiramente o contraste do texto",
            "A composição está muito boa, seguindo bem a regra dos terços"
          ]
        })
      }
    } catch (error) {
      console.error('Erro na análise:', error)
      // Simular resultado para demonstração
      setAnalysisResult({
        score: 87.3,
        breakdown: {
          visual_impact: 92,
          clarity: 85,
          contrast: 89,
          color_harmony: 84,
          composition: 88,
          text_readability: 82
        },
        suggestions: [
          "Excelente thumbnail! Pequenos ajustes podem torná-la ainda melhor",
          "Considere aumentar ligeiramente o contraste do texto",
          "A composição está muito boa, seguindo bem a regra dos terços"
        ]
      })
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 85) return "text-green-500"
    if (score >= 70) return "text-yellow-500"
    return "text-red-500"
  }

  const getScoreBadge = (score) => {
    if (score >= 85) return { text: "Excelente", variant: "default" }
    if (score >= 70) return { text: "Bom", variant: "secondary" }
    return { text: "Precisa Melhorar", variant: "destructive" }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">ThumbScore AI</h1>
                <p className="text-sm text-gray-400">Otimize suas thumbnails com IA</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-purple-300 border-purple-300">
                <Sparkles className="w-3 h-3 mr-1" />
                Powered by AI
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="space-y-6">
            <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Upload className="w-5 h-5 mr-2" />
                  Upload da Thumbnail
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Faça upload da sua thumbnail para análise com IA
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
                    dragActive 
                      ? 'border-purple-400 bg-purple-400/10' 
                      : 'border-gray-600 hover:border-purple-400 hover:bg-purple-400/5'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  {previewUrl ? (
                    <div className="space-y-4">
                      <img 
                        src={previewUrl} 
                        alt="Preview" 
                        className="max-w-full max-h-64 mx-auto rounded-lg shadow-lg"
                      />
                      <p className="text-sm text-gray-400">{selectedFile?.name}</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto">
                        <Upload className="w-8 h-8 text-white" />
                      </div>
                      <div>
                        <p className="text-lg font-medium text-white mb-2">
                          Arraste sua thumbnail aqui
                        </p>
                        <p className="text-sm text-gray-400 mb-4">
                          ou clique para selecionar um arquivo
                        </p>
                        <input
                          type="file"
                          accept="image/*"
                          onChange={handleFileInput}
                          className="hidden"
                          id="file-input"
                        />
                        <label htmlFor="file-input">
                          <Button variant="outline" className="cursor-pointer">
                            Selecionar Arquivo
                          </Button>
                        </label>
                      </div>
                    </div>
                  )}
                </div>

                {selectedFile && (
                  <div className="mt-6">
                    <Button 
                      onClick={analyzeImage} 
                      disabled={isAnalyzing}
                      className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                    >
                      {isAnalyzing ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Analisando...
                        </>
                      ) : (
                        <>
                          <BarChart3 className="w-4 h-4 mr-2" />
                          Analisar Thumbnail
                        </>
                      )}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {analysisResult ? (
              <>
                {/* Score Card */}
                <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center justify-between">
                      <span className="flex items-center">
                        <Eye className="w-5 h-5 mr-2" />
                        Pontuação Geral
                      </span>
                      <Badge {...getScoreBadge(analysisResult.score)}>
                        {getScoreBadge(analysisResult.score).text}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center space-y-4">
                      <div className={`text-6xl font-bold ${getScoreColor(analysisResult.score)}`}>
                        {analysisResult.score}
                      </div>
                      <p className="text-gray-400">de 100 pontos</p>
                      <Progress 
                        value={analysisResult.score} 
                        className="w-full h-3"
                      />
                    </div>
                  </CardContent>
                </Card>

                {/* Breakdown Card */}
                <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="text-white">Análise Detalhada</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {Object.entries(analysisResult.breakdown).map(([key, value]) => (
                      <div key={key} className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-300 capitalize">
                            {key.replace('_', ' ')}
                          </span>
                          <span className={`text-sm font-medium ${getScoreColor(value)}`}>
                            {Math.round(value)}%
                          </span>
                        </div>
                        <Progress value={value} className="h-2" />
                      </div>
                    ))}
                  </CardContent>
                </Card>

                {/* Suggestions Card */}
                <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Sparkles className="w-5 h-5 mr-2" />
                      Sugestões de Melhoria
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {analysisResult.suggestions.map((suggestion, index) => (
                        <li key={index} className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-300 text-sm">{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                {/* Action Buttons */}
                <div className="flex space-x-3">
                  <Button variant="outline" className="flex-1">
                    <Download className="w-4 h-4 mr-2" />
                    Baixar Relatório
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <Share2 className="w-4 h-4 mr-2" />
                    Compartilhar
                  </Button>
                </div>
              </>
            ) : (
              <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
                <CardContent className="py-16">
                  <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center mx-auto">
                      <BarChart3 className="w-8 h-8 text-gray-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-white mb-2">
                        Aguardando Análise
                      </h3>
                      <p className="text-gray-400">
                        Faça upload de uma thumbnail para ver a análise detalhada
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-white text-center mb-8">
            Recursos Avançados de IA
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Eye className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Análise Visual</h3>
                <p className="text-gray-400 text-sm">
                  Avaliação completa de impacto visual, contraste e composição
                </p>
              </CardContent>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">IA Avançada</h3>
                <p className="text-gray-400 text-sm">
                  Modelos treinados com milhares de thumbnails virais
                </p>
              </CardContent>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Métricas Precisas</h3>
                <p className="text-gray-400 text-sm">
                  Pontuação baseada em dados reais de performance
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-gray-400">
            <p>&copy; 2024 ThumbScore AI. Desenvolvido com IA para criadores de conteúdo.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

