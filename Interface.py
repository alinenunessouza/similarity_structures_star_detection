from pydantic import BaseModel, Field,  ConfigDict
from typing import Annotated, Callable, List, Any
import numpy as np


class KernelParam(BaseModel):
    size: int
    sigma: float


class PipelineInput(BaseModel):
    img_path: str
    filter_intensity: Annotated[float, Field(strict=True, gt=0, le=1)]
    kernel_param: List[KernelParam]
    agg_type: Callable


class FilterOutput(BaseModel):
    filtered_image: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Kernel(BaseModel):
    parameter: KernelParam
    values: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FilterInput(BaseModel):
    filter_intensity: Annotated[float, Field(strict=True, gt=0, le=1)]
    input_image: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)


class SimilarityMapOutput(BaseModel):
    map: np.ndarray
    params: KernelParam
    model_config = ConfigDict(arbitrary_types_allowed=True)

class SimilarityMapInput(BaseModel):
    image:np.ndarray
    kernel:Kernel
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AggregatedMap(BaseModel):
    map: np.ndarray
    aggregation_type: Callable
    base_maps: List[SimilarityMapOutput]
    model_config = ConfigDict(arbitrary_types_allowed=True)
