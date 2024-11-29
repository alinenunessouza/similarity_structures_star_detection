import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


def _open_img(path: str, filter_ths: float = 0.1, debug: bool = False) -> np.ndarray:
    img = cv2.imread(path, 0)
    threshold_value = filter_ths * img.max()
    _, mask = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
    img = cv2.bitwise_and(img, img, mask=mask.astype(np.uint8))
    img = np.where(mask > 0, img, 0)
    if debug:
        plt.imshow(img, cmap="gray")
        plt.title("Base Img")
        plt.show()
    return img


def _generate_kernel(
    kernel_size: int = 3, sigma: float = 0.5, debug: bool = False
) -> np.ndarray:
    gaussian_kernel = cv2.getGaussianKernel(kernel_size, sigma)
    gaussian_kernel = np.array(gaussian_kernel * gaussian_kernel.T)
    gaussian_kernel = gaussian_kernel - np.mean(gaussian_kernel)
    gaussian_kernel = gaussian_kernel / np.linalg.norm(gaussian_kernel)
    if debug:
        plt.imshow(gaussian_kernel)
        plt.title("Kernel")
        plt.show()
    return gaussian_kernel


def cosine_similarity(img_region, kernel):
    img_region_flat = img_region.flatten()
    kernel_flat = kernel.flatten()

    dot_product = np.dot(img_region_flat, kernel_flat)
    norm_img_region = np.linalg.norm(img_region_flat)
    norm_kernel = np.linalg.norm(kernel_flat)

    # Similaridade de cosseno entre 0 e 1
    return max(dot_product / (norm_img_region * norm_kernel), 0)


def new_get_convolution(
    path: str,
    filter_ths: float = 0.1,
    kernel_size: int = 3,
    sigma: float = 0.5,
    debug: bool = False,
):
    img = _open_img(path, filter_ths, True)
    gaussian_kernel = _generate_kernel(kernel_size, sigma, True)
    similarity_map = np.zeros_like(img, dtype=np.float32)

    ## Gerar mapa com similaridade de cosseno entre Kernel e imagem

    for i in range(0, img.shape[0] - kernel_size + 1):
        for j in range(0, img.shape[1] - kernel_size + 1):
            img_region = img[i : i + kernel_size, j : j + kernel_size]
            if np.any(img_region != 0):
                similarity_map[i, j] = cosine_similarity(img_region, gaussian_kernel)
            else:
                continue

    if debug and np.any(similarity_map != 0):
        plt.imshow(similarity_map, cmap="gray")
        plt.title("convolved map")
        plt.show()
    return similarity_map
