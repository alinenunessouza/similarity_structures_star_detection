# Descritivo Funcional do Projeto: Identificação de Estrelas em Imagens Desfocadas

Este projeto tem como objetivo criar **dois modelos de similaridade** para a identificação de estrelas em imagens desfocadas. Ele foi pensado de forma modular para ser flexível, escalável e fácil de entender.

---

## Módulos do Projeto

### 1. **Módulo de Pré-Processamento**
#### Descrição:
Este módulo é responsável por preparar as imagens para análise, garantindo que elas tenham qualidade suficiente para que as estrelas possam ser identificadas.

#### Funcionalidades:
- Normalizar a intensidade das imagens.
- Reduzir ruído utilizando filtros como o filtro gaussiano ou mediano.
- Equalizar o histograma para melhorar o contraste das imagens.

---

### 2. **Módulo de Extração de Similaridade**
#### Descrição:
Este é o núcleo do sistema, onde os dois modelos de análise de similaridade são implementados para identificar padrões de estrelas.

#### Modelos:
1. **Modelo de Similaridade por cosseno:**
   - Baseado em padrões de brilho e intensidade.
   - Utiliza técnicas de similaridade por cosseno para encontrar regiões na imagem que correspondem a estrelas.

2. **Modelo de Correlação de Pearson:**
   - Baseado em padrões de brilho e intensidade.
   - Utiliza técnicas de correlação para encontrar regiões na imagem que correspondem a estrelas.

---
### 3. **Módulo de Pós-Processamento**
---

### 4. **Módulo de Validação**
#### Descrição:
Valida os resultados dos modelos para garantir que as estrelas identificadas sejam precisas.

#### Funcionalidades:
- Comparar as coordenadas das estrelas detectadas com as posições reais (quando disponíveis).
- Gerar métricas de desempenho como precisão, recall e F1-score.
- Avaliar a robustez dos modelos em diferentes condições de desfoque, ruído e brilho.

---

### 5. **Módulo de Documentação**
#### Descrição:
Fornece guias claros e detalhados para o uso dos modelos, incluindo explicações técnicas e práticas.

#### Funcionalidades:
- Documentar o fluxo de trabalho de cada módulo.
- Incluir exemplos de entrada e saída para facilitar o entendimento.
- Manter a documentação atualizada com as melhorias implementadas.

---

### 6. **Módulo de Configuração**
#### Descrição:
Permite ajustar os parâmetros dos modelos e das etapas de processamento.

#### Funcionalidades:
- Configurar os parâmetros dos filtros de pré-processamento (e.g., tamanho do kernel do filtro gaussiano).
- Ajustar os limiares dos modelos para melhorar a precisão ou recall.
- Definir métricas personalizadas para avaliação.

---

## Fluxo de Funcionamento

1. **Entrada de Imagem:**
   - Uma ou mais imagens desfocadas são carregadas no sistema.

2. **Pré-Processamento:**
   - As imagens passam pelo módulo de pré-processamento para limpeza e normalização.

3. **Análise de Similaridade:**
   - Os dois modelos analisam as imagens em busca de estrelas.
  
4. **Pós-Processamento:**


4. **Validação:**
   - Os resultados são validados e comparados com métricas de desempenho.

5. **Ajustes:**
   - Baseado nos resultados, o usuário pode ajustar os parâmetros no módulo de configuração.

---

## Resultados Esperados

1. **Precisão na detecção de estrelas:**
   - Identificar estrelas mesmo em condições adversas, como imagens com ruído, como desfoque.

2. **Flexibilidade dos modelos:**
   - Permitir ajustes para diferentes tipos de imagens astronômicas.

3. **Facilidade de uso:**
   - Oferecer ferramentas visuais e documentações claras para que o sistema seja acessível a diferentes tipos de usuários.

---

## Aplicações Práticas

- Identificação de estrelas em telescópios amadores ou profissionais.
- Detecção de padrões em imagens para análise científica.

