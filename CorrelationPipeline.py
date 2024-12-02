import cv2
import numpy as np
import matplotlib.pyplot as plt
import Interface as mi
from typing import List, Callable
from scipy.signal import correlate2d

THRESHOLD_FACTOR = 0.6 # Fator para cálculo do limiar
MASK_MAX_VALUE = 255  # Valor máximo da máscara binária

class CorrelationPipeline:
    def __init__(self, is_debug) -> None:
        self.debug_flag = is_debug

    def _filter_by_intensity(self, input_data: mi.FilterInput) -> mi.FilterOutput:
        """
        Filters the image based on the light intensity and applies a binary mask to filter noise.

        Parameters:
        - input_data: FilterByIntensityInput object containing the intensity factor and image.

        Returns:
        - FilterByIntensityOutput object containing the resulting image after applying the binary mask.
        """
        filter_intensity = input_data.filter_intensity
        image = input_data.input_image
        ths = filter_intensity * image.max()
        _, mask = cv2.threshold(image, ths, MASK_MAX_VALUE, cv2.THRESH_BINARY)
        img = cv2.bitwise_and(image, image, mask=mask.astype(np.uint8))
        filtered_image = np.where(mask > 0, img, 0)

        return mi.FilterOutput(filtered_image=filtered_image)

    def _generate_kernel(self, param: mi.KernelParam) -> mi.Kernel:
        """
        Gera um kernel gaussiano com base nos parâmetros fornecidos e o normaliza.

        O método cria um kernel gaussiano bidimensional usando a função `cv2.getGaussianKernel`,
        multiplicando-o por sua transposta para obter uma matriz bidimensional. Em seguida, o kernel
        é centrado subtraindo a média e normalizado pela norma Euclidiana.

        Se o sinalizador de depuração (`debug_flag`) estiver ativado, a função exibirá o kernel
        usando `matplotlib`.

        Parâmetros:
        -----------
        param : mi.KernelParam
            Um objeto contendo os parâmetros para a geração do kernel. Inclui:
            - `size`: O tamanho do kernel (número de linhas e colunas).
            - `sigma`: O desvio padrão da distribuição gaussiana para o kernel.

        Retorna:
        --------
        mi.Kernel
            Retorna um objeto `mi.Kernel` que contém:
            - `parameter`: Os parâmetros usados para gerar o kernel.
            - `values`: O kernel gaussiano gerado e normalizado como uma matriz numpy.


        Exemplo de uso:
        ---------------
            kernel_param = mi.KernelParam(size=5, sigma=1.0)
            generated_kernel = self._generate_kernel(kernel_param)
            O método pode exibir o kernel se `self.debug_flag` estiver ativado.
        """
        gaussian_kernel = cv2.getGaussianKernel(param.size, param.sigma)
        gaussian_kernel = np.array(gaussian_kernel * gaussian_kernel.T) # gera 2D
        gaussian_kernel = gaussian_kernel - np.mean(gaussian_kernel)
        gaussian_kernel = gaussian_kernel / np.linalg.norm(gaussian_kernel)

        if self.debug_flag:
            plt.imshow(gaussian_kernel)
            plt.title(f"Kernel (ks: {param.size} sigma: {param.sigma})")
            plt.show()
        return mi.Kernel(parameter=param, values=gaussian_kernel)

    def correlation        (
        self, img_region: np.ndarray, kernel: np.ndarray
    ) -> np.ndarray:
        img_region_flat = img_region.flatten() # faz o array ficar array unidimensional (plano)
        kernel_flat = kernel.flatten()
        return np.correlate(img_region_flat, kernel_flat)

    def get_similarity_map(self, input: mi.SimilarityMapInput) -> mi.SimilarityMapOutput:
        filtered_image = input.image
        gaussian_kernel = input.kernel
        kernel_parameter = gaussian_kernel.parameter
        kernel_size = kernel_parameter.size
        
        similarity_map = np.zeros_like(filtered_image, dtype=np.float32) # inicializa a matriz de similaridade com o tamanho da imagem preenchida com zeros
        half_kernel_size = kernel_size // 2  # Calcula a metade do tamanho do kernel

        for i in range(0, filtered_image.shape[0] - kernel_size + 1): # percorre a imagem verticalmente
            for j in range(0, filtered_image.shape[1] - kernel_size + 1): # percorre a imagem horizontalmente
                img_region = filtered_image[i : i + kernel_size, j : j + kernel_size] # extrai uma região da imagem do tamanho do kernel
                if np.any(img_region != 0): # filtra para não calcular similaridade em áreas vazias
                    # if self.debug_flag:
                    #     self.plot_map(img_region, "Região extraída da imagem no tamanho do kernel")
                    similarity_value = self.correlation(img_region, gaussian_kernel.values)
                    
                    # Ajustar a posição para o centro da região em vez do canto superior esquerdo
                    center_i = i + half_kernel_size
                    center_j = j + half_kernel_size
                    
                    similarity_map[center_i, center_j] = similarity_value

        threshold_value = THRESHOLD_FACTOR * similarity_map.max() # valor usado para criar uma máscara binária que destaca áreas de maior similaridade
        _, mask = cv2.threshold(similarity_map, threshold_value, MASK_MAX_VALUE, cv2.THRESH_BINARY) # pixels no mapa de similaridade que têm valores acima do threshold_value são definidos como 255 (branco), e os outros são 0 (preto)
        
        similarity_map = cv2.bitwise_and(similarity_map, similarity_map, mask=mask.astype(np.uint8)) # preserva apenas os pixels do mapa de similaridade que estão dentro das áreas de alta similaridade (onde a máscara tem valor 255)
        #similarity_map = np.where(mask > 0, similarity_map, 0) # pixels fora das regiões com alta similaridade serão zerados
        
        return mi.SimilarityMapOutput(map=similarity_map, params=kernel_parameter)

    def map_aggregation(self,
        maps: List[mi.SimilarityMapOutput], agg_function: Callable[[np.ndarray], np.ndarray]
    ) -> mi.SimilarityMapOutput:
        """
        Agrega uma lista de mapas de similaridade usando uma função de agregação fornecida.

        Parâmetros:
        -----------
        maps : List[mi.SimilarityMap]
            Lista de mapas de similaridade a serem agregados. Cada mapa é um objeto `mi.SimilarityMap`,
            contendo o mapa de similaridade (`map`) e os parâmetros usados para gerar o kernel (`params`).

        agg_function : Callable[[np.ndarray], np.ndarray]
            Função de agregação a ser aplicada ao conjunto de mapas. Exemplo de funções podem ser `np.mean`,
            `np.median`, `np.sum`, ou qualquer outra função que agregue um array de mapas de similaridade.

        Retorna:
        --------
        mi.SimilarityMap
            Um novo objeto `mi.SimilarityMap` contendo o mapa agregado e os parâmetros do kernel
            (assumimos que todos os mapas de entrada compartilham os mesmos parâmetros).

        Exceções:
        ---------
        ValueError: Lança um erro se a lista de mapas for vazia ou se os mapas não tiverem o mesmo tamanho.

        Exemplo de uso:
        ---------------
        aggregated_map = map_aggregation(list_of_similarity_maps, np.mean)
        """
        if not maps:
            raise ValueError(
                "A lista de mapas está vazia. Não é possível realizar a agregação."
            )

        # Verifica se todos os mapas têm o mesmo tamanho
        map_shape = maps[0].map.shape
        if any(m.map.shape != map_shape for m in maps):
            raise ValueError(
                "Todos os mapas devem ter o mesmo tamanho para serem agregados."
            )

        # Converte os mapas para um array 3D: (num_maps, height, width)
        map_stack = np.array([m.map for m in maps])

        # Aplica a função de agregação ao longo do eixo 0 (agregando os mapas)
        aggregated_map = agg_function(map_stack, axis=0)

        return mi.AggregatedMap(
            map=aggregated_map, aggregation_type=agg_function, base_maps=maps
        )
    

    def plot_map(self, map, title):
        plt.imshow(map, cmap='gray')
        plt.title(title)
        plt.show()

    def run(self, input_data: mi.PipelineInput, flag_kernel:bool=True) -> mi.AggregatedMap:
        """
        Executa o pipeline de similaridade para múltiplas imagens, gera os mapas de similaridade e realiza a agregação.

        Parâmetros:
        -----------
        inputs : List[mi.PipelineInput]
            Lista de objetos `mi.PipelineInput` contendo as informações necessárias para gerar os mapas de similaridade.

        Retorna:
        --------
        mi.AggregatedMap
            O mapa agregado resultante da agregação dos mapas de similaridade gerados.
        """

        input_image = cv2.imread(input_data.img_path, 0) # carrega a imagem em escala de cinza

        if self.debug_flag:
            self.plot_map(input_image, "Imagem em escala de cinza")
            print(input_image)

        input_image = input_image / 255.0 #normalized image

        if self.debug_flag:
            self.plot_map(input_image, "Imagem normalizada")
            print(input_image)

        img = self._filter_by_intensity(
            mi.FilterInput(
                filter_intensity=input_data.filter_intensity,
                input_image= input_image 
            )
        )

        filtered_image = img.filtered_image

        if self.debug_flag:
            self.plot_map(filtered_image, "Filtered image")

        #pad_width = 35  # 1 pixel de padding em todas as direções, for kernel_param -> maior kernel size

        # Adicionando padding
        #filtered_image = np.pad(filtered_image, pad_width, mode='constant', constant_values=0)

        similarity_maps = []
        for kernel_param in input_data.kernel_param:
            gaussian_kernel = self._generate_kernel(kernel_param)
            similarity_map = self.get_similarity_map(
                mi.SimilarityMapInput(image=filtered_image, kernel=gaussian_kernel)
            )
            if self.debug_flag:
                self.plot_map(similarity_map.map, "Similarity_map")
            """similarity_map = self.get_similarity_map(
                mi.SimilarityMapInput(image=similarity_map.map, kernel=gaussian_kernel)
            )"""
            # self.plot_map(similarity_map.map, f"Kernel (ks: {similarity_map.params.size} sigma: {similarity_map.params.sigma})")
            similarity_maps.append(similarity_map)

        aggregated_map = self.map_aggregation(similarity_maps, input_data.agg_type)
        self.plot_map(aggregated_map.map,title='aggregated_map')
        return aggregated_map
