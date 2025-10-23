# 🧠 Segmentação de imagens
Mini-aplicativo de **visão computacional e IA** para **segmentação de imagens** utilizando **OpenCV** e **Python**.  
Permite segmentar cores (HSV) ou regiões (K-Means), salvando a **máscara binária** e a **imagem com overlay**.

---

## 🎯 Objetivo

O projeto realiza **segmentação de imagens** por dois métodos:
- **HSV (por cor):** segmenta regiões verdes ou azuis com base em faixas de cor configuráveis.
- **K-Means (agrupamento):** agrupa cores semelhantes e seleciona o cluster mais próximo da cor desejada.

---

## ⬇️ Instalação

### Clonar o repositório
```bash
git clone https://github.com/saffonso/image-segmentation-opencv.git
cd vision-ai-segmentation
```

### Instalar as dependências
```bash
pip install -r requirements.txt
```

## ⚙️ Execução

Para rodar o programa, basta informar o caminho da imagem e o método desejado. Por exemplo, para segmentar áreas verdes de uma imagem usando o método HSV, utiliza-se o comando:

```bash
python segment.py --input samples/planta1.jpg --method hsv --target green
```

Também é possível ajustar manualmente os limites de cor utilizando parâmetros adicionais, como `--hmin`, `--hmax`, `--smin`, **--smax**, **--vmin** e **--vmax**. Já para segmentar usando o método de agrupamento (K-Means), o comando seria:

```bash
python segment.py --input samples/cena.jpg --method kmeans --k 7 --target green
```
## 💡 Métodos

### Método Kmeans
Esse método faz a segmentação da imagem com base na cor.
Primeiro, a imagem é convertida do formato padrão BGR (usado pelo OpenCV) para o espaço de cor HSV, que separa a cor em três componentes:

- H (Hue) — tonalidade, define a cor (por exemplo, verde ≈ 60, azul ≈ 120);

- S (Saturation) — intensidade da cor;

- V (Value) — brilho da cor.

Depois da conversão, o algoritmo aplica um filtro que mantém apenas os pixels dentro de uma faixa de cor (range) configurável — por exemplo, tons de verde entre H=35–85.
O resultado é uma máscara binária, onde os pixels da cor desejada aparecem em branco (255) e o restante em preto (0).

Esse método é rápido e eficiente, mas depende bastante da iluminação e da saturação da imagem.