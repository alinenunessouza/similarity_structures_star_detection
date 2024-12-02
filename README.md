# Analysis of Similarity Structures for Star Identification in Blurred Images

_Keywords: astronomy, star detection algorithm, blurred images, computer vision, similarity metrics._

# Directory Structure

```plaintext
.
├── data/                          # Images for model testing
├── docs/                          # Project documentation files
├── examples/                      # Demonstrative examples and notebooks
├── utils/                         # Utility functions and helper scripts
├── .gitignore                     
├── CorrelationPipeline.py         # Pipeline for the model based on Pearson Correlation
├── CosSimilarityPipeline.py       # Pipeline for the model based on Cosine Similarity
├── Interface.py                   # Interface defining the pipeline contracts
├── filter_toolbox.py              # Functions for use in the models
```

# Executing the Pipelines

``` python
# Define input parameters
input_data = mi.PipelineInput(
    img_path = img_path, # Path to the image to be tested
    filter_intensity=0.2, # Minimum intensity factor for the preprocessing step
    kernel_param= [mi.KernelParam(size=17, sigma=3)], # Gaussian kernel parameters: size and standard deviation
    agg_type=np.mean # Aggregation function for similarity maps (e.g., np.mean, np.max)
)
# Initialize the model pipeline
model = model_pipeline(is_debug=False) # Set is_debug=True for detailed process logs

# Run the pipeline with the input data
agg=model.run(input_data=input_data)
```

# Tech
- [Python] -
- [cv2] -
- [scipy] -
- [matplotlib]
