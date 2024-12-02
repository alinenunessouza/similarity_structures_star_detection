# Descritivo Funcional do Projeto: Identificação de Estrelas em Imagens Desfocadas
obs.: esta documentação faz parte do trabalho de conclusão 'Análise de Estruturas de Similaridade para Identificação de Estrelas em Imagens Desfocadas'

Este projeto tem como objetivo criar **dois modelos de similaridade** para a identificação de estrelas em imagens desfocadas. Ele foi pensado de forma modular para ser flexível, escalável e fácil de entender.

![Diagrama de fluxo do projeto](https://github.com/alinenunessouza/similarity_structures_star_detection/blob/main/docs/Fluxogragrama_metodologia.png)

---

## Módulos do Projeto

### 1. **Módulo de Pré-Processamento**
#### Descrição:
Este módulo é responsável por preparar as imagens para análise, garantindo que elas tenham qualidade suficiente para que as estrelas possam ser identificadas.

#### Funcionalidades:
- Converter a imagem  para escala de preto e branco;
- Normalizar os pixels da imagem, para intervalo entre 0 e 1;
- Reduzir ruído utilizando um filtro de intensidade.

---

### 2. **Módulo de Extração de características**
#### Descrição:
Este é o núcleo do sistema, onde os dois modelos de análise de similaridade são implementados para identificar padrões de estrelas. A base do projeto é dada pela hipótese que a distribuição de energia de uma imagem de estrela real coincide estatisticamente com uma distruibuição gaussiana na maioria dos casos.

#### Modelos:
1. **Modelo de Similaridade por cosseno:**
   - Estabelecer uma comparação baseada na diferença entre ângulos de um vetor de espaço N. No caso, é o produto escalar da região de interesse da imagem com estrela e o kernel gaussiano gerado, dividido pelo comprimento da região da imagem e do kernel. Como a similaridade trabalha com vetor de dimensão 1xN, foi necessário transformar a imagem em um vetor unidimensional.
   ![Fluxograma do modelo de similaridade por cosseno](https://github.com/alinenunessouza/similarity_structures_star_detection/blob/main/docs/Fluxograma_SimilaridadeCos.png)

2. **Modelo de Correlação de Pearson:**
   - Abodagem através do índice de correlação de Person. A correlação é responsável por avaliar a força e a direção de uma relação linear entre a intensidade de brilho do segmento da imagem e o kernel gaussiano;
   - Mapa de correlação: destaca objetos estelares que se assemelham em tamanho e dispersão ao kernel utilizado;
   - Projetor Gama: de maneira a agregar diferentes kernels, a utilização de um projetor gama é definida como a função acumulativa das correlações inferidas.
   ![Fluxograma do modelo de correlação](https://github.com/alinenunessouza/similarity_structures_star_detection/blob/main/docs/Fluxograma_Correlacao.png)
---
### 3. **Módulo de Pós-Processamento**
- Detecção dos picos de luminosidade a partir dos mapas de similaridade gerados;
- Indicação de coordenadas com pontos candidados a estrela na imagem original.
---

### 4. **Etapa de Validação**
#### Descrição:
Validar os resultados dos modelos para garantir que as estrelas identificadas sejam precisas.

#### O que será feito:
- Comparar as coordenadas das estrelas detectadas com as posições reais (quando disponíveis).
- Avaliar o comportamento do modelo com base de dados homogênea e não homogênea (disparidade maior quanto a tamanho de estrelas, disparidade luminosa entre objetos, etc).
- Gerar métricas de classificação como acurácia, precisão, recall, falsos positivos, falsos negativos, verdadeiro positivo e verdadeiro negativo.
- Gerar métricas de regressão como RMSE (erro quadrático médio).

---

### 5. **Módulo de Configuração**
#### Descrição:
Pipeline que permite ajustar os parâmetros dos modelos e das etapas de processamento.

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
   - Indicação dos candidatos a estrela.

5. **Validação:**
   - Os resultados são validados e comparados com métricas de classificação e regressão.

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

- Identificação de estrelas em telescópios amadores ou profissionais;
- Detecção de padrões em imagens para análise científica;
- Aplicação em equipamentos com pouco espaço de armazenamento, sem necessidade de carregar catalogos estelares.

