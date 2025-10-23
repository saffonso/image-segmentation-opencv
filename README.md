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
cd image-segmentation-opencv
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

Também é possível ajustar manualmente os limites de cor utilizando parâmetros adicionais, como `--hmin`, `--hmax`, `--smin`, `--smax`, `--vmin` e `--vmax`. Já para segmentar usando o método de agrupamento (K-Means), o comando seria:

```bash
python segment.py --input samples/cena.jpg --method kmeans --k 7 --target green
```
## 💡 Métodos

### Método HSV
Esse método faz a segmentação da imagem com base na cor.
Primeiro, a imagem é convertida do formato padrão BGR (usado pelo OpenCV) para o espaço de cor HSV, que separa a cor em três componentes:

- H (Hue) — tonalidade, define a cor (por exemplo, verde ≈ 60, azul ≈ 120);

- S (Saturation) — intensidade da cor;

- V (Value) — brilho da cor.

Depois da conversão, o algoritmo aplica um filtro que mantém apenas os pixels dentro de uma faixa de cor (range) configurável — por exemplo, tons de verde entre H=35–85.
O resultado é uma máscara binária, onde os pixels da cor desejada aparecem em branco (255) e o restante em preto (0).

Esse método é rápido e eficiente, mas depende bastante da iluminação e da saturação da imagem.

### Método Kmeans
O método K-Means realiza a segmentação agrupando os pixels com cores semelhantes.
Cada pixel é tratado como um ponto em um espaço tridimensional (B, G, R), e o algoritmo os divide em K grupos (clusters) — onde K é definido pelo usuário.

Após o agrupamento, o programa identifica qual grupo (cluster) possui cor mais próxima da cor alvo (verde ou azul) e cria uma máscara com os pixels pertencentes a esse grupo.

Esse método é útil quando as cores não estão bem definidas ou há variações de iluminação, pois ele não depende de um range fixo de cor. No entanto, ele é um pouco mais lento e pode confundir tons semelhantes se o valor de K não for adequado.

---

## 🔎 Observações
Sobre o range do método HSV, como o alvo eram cores azuis ou verdes escolhi um range de `35 - 85` para verde e `90 - 130` para azul, obtendo assim uma boa precisão para esse tipo de algoritmo. Além disso os valores de S e V normalmente variam de 50 a 255, para capturar tons intensos sem incluir áreas muito escuras ou cinzentas.

## ❗ Limitações
Os métodos de segmentação utilizados são sensíveis a variações nas condições de iluminação e cor. Mudanças de luz, sombras ou reflexos podem alterar os valores de brilho `V` e comprometer a detecção das cores.

Imagens com baixa saturação como tons apagados, esbranquiçados ou acinzentados também dificultam a segmentação por HSV, pois o `S` se torna muito baixo.

Além disso, o método K-Means pode confundir cores semelhantes quando há muitos tons próximos, e seu desempenho depende da escolha adequada do número de clusters (k), o que eu observei nos testes individuais que fiz, para uma escolha de poucos clusters a máscara refletia uma sensibilidade muito alta de cores, mas com o número de `K` mais alto era possível uma precisão maior.
