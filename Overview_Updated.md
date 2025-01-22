# Multimodal Sentiment Analysis from Images and Audio with Noise Information from Audio

## Learning Objectives
With this material, reader will:
1. Understand the availability of multimodal data (images and audio) taken from the environment.
2. Explore how  multimodal data can be handled and possiblity of feature extraction techniques.
3. Explore how the relationship between various features (from image and audio) with sentiments can be shown.

## Introduction to the Problem

### Why is it important?
Urban environments generate vast amounts of multimodal data through cameras and microphones. Understanding the relationship between these sensory inputs and human sentiment can provide valuable insights for urban planning, public safety, and quality of life assessment. This project explores how visual and acoustic features correlate with reported sentiment in urban spaces. Furthermore, the insights gained from this project can be relevant for:
1. **Urban Planning**: Designing human-centered spaces.
2. **Public Safety**: Identifying potentially stressful environments.
3. **Quality of Life Assessment**: Measuring factors that impact well-being.

## Key Concepts
### Features in Multimodal Data
Features are the characteristics that can be extracted from the data. A simple example of feature from an image data can be the average pixel value. And for an audio, level of noise can be a feature.

We have 3 types of features:
1. **Image Features**: We have 3 image data from each user on each of the 5 places. And we compute features from them.
2. **Audio Features**: We have environmental noise recording of few seconds from each user on each of the 5 places. We compute noise level as dB feature. 
3. **Sentiment Features**: We have this feature in source file which was uploaded by users. 

#### Image Features
In order to generate image features, we will be using OpenCV. 

1. **Brightness and RGB Values**: Measure ambient lighting. 
    - **Explains**: How light or colorful an area is.
    - **Package Uses**: OpenCV
2. **Greenness**: Quantify vegetation to assess greenery levels. 
    - **Explains**: How much vegetation is visible (like trees or grass).
    - **Package Uses**: OpenCV
3. **Object Counts**: Using State of the Art method to detect people and vehicles.
    - **Explains**: How crowded or busy an area feels.
    - **Package Uses**: This data will be provided because calculation of this feature takes high resources and compution time. This data is created using YOLO.

#### Audio Features
1. **Noise Levels**: Capture environmental sound intensity using Root Mean Square (RMS) amplitude, a method in the Librosa library.
    - **Explains** : How loud or quiet a place is—like the difference between honking cars and birds chirping.
    - **Package Uses**: Librosa

#### Sentiment Features
1. **Bipolar Scales**: This features are uploaded by users on the time of data collection which has been combined to make ease to use.
    - **Explains**: How a person felt at a place: ranging from Calm-Chaotic
    - **Package Uses**: None.

### Analysis of Features
#### 1. Density Analysis
Based on the features extracted above, we can look into the density:
1. Density of people and vehicles on the places. Which is the most/least crowed places?
2. Greeness level on the places. Which is the most/least green place?
3. Noise level on places. Which is the most/least noisy place?

#### 2. Correlation Analysis
Based on the features extracted above, we can compute the correlatio and answer the questions:
1. Does people count and vehicles count have any correlation with Sentiment Tags?
2. Does the noise level have any relationship with people and vehicles counts and with tags?
3. Does the correlation varies throughout the palces or remains same?
4. Can the correlation vary based on the time of visit?
5. Can the correlation vary based on an individual person (user)?

## Practical Implementation
### 1. Installation of Packages
We will be working with packages:
1. `pandas`: To read and work with dataframes.
2. `numpy`: To work with numerical operations like finding mean and subtracion on arrays.
3. `librosa`: To work with audio.
4. `cv2`: To work with images.
5. `matplotlib`: To generate plots.
6. `seaborn`: To make `matplotlib` better.
7. `plotly`: To generate interactive plots.
8. `tqdm`: To visualize progressbar.
9. `scikit-learn`: To work with KMeans Clustering. (It is more than this though.)

The above mentioned packages could be installed with PIP: `pip install scikit-learn pandas plotly seaborn opencv-python librosa tqdm`

### 2. Preparing Data
1. **Main source data**: This data is given to us via Studon. It is available on session **28. Nov 2024, 14:00 - 16:00: Session 7: Intro multi-modal data sample**
2. **Suppliment data**: This data is given by us and contains the information of person and vehicle counts for each image.

After downloading the data, we will be reading them using pandas.

### 3. Filtering and Merging Both data
Based on the availability of columns, we need to merge above two data and make a single data for easier use.

### 4. Location Clustering
1. Based on the lattitude and longitude data available, we apply KMeans Clustering.
2. We visualize the person and vehicle counts on map and location cluster to find the cluster name.
4. We map cluster id to place name.

### 5. Greeness and Brightness Extraction
Here we read each image file and calculate Brightness value and Greeness value. 

#### Greeness calculation
Using the function below, we calculate the greeness value.

```python

def calculate_greeness(data: np.ndarray) -> float:
    """
    Calculate the greenness of an image using RGB channel differences.

    The formula identifies vegetation presence through two conditions:
    1. G-R > 0 (Diff_1)
    2. G-B > 0 (Diff_2)
    Vegetation is present when both conditions are true and their product is positive.

    Args:
        data (np.ndarray): Input image array in RGB format with shape (H, W, 3)

    Returns:
        float: Proportion of pixels identified as green vegetation (0 to 1)
    """
    data = data.astype(np.float64)

    # Extract RGB channels
    blue_channel, green_channel, red_channel = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # Calculate differences
    Diff_1 = green_channel - red_channel
    Diff_2 = green_channel - blue_channel
    Diff = Diff_1 * Diff_2
    
    # Identify green vegetation pixels
    greens = np.logical_and(Diff > 0, Diff_1 > 0)

    # Calculate proportion of green pixels
    portion_green = np.sum(greens) / (data.shape[0] * data.shape[1])

    return portion_green
```

#### Brightness calculation
Using the function below, we calculate brightness values.

```python
def calculate_brightness(image: np.ndarray) -> dict:
    """
    Calculate average brightness metrics for an image.

    Args:
        image (np.ndarray): Input image array in BGR format

    Returns:
        dict: Dictionary containing:
            - 'brightness': Overall average brightness (0-255)
            - 'b': Average blue channel intensity
            - 'g': Average green channel intensity
            - 'r': Average red channel intensity
    """
    # Split channels
    b, g, r = cv2.split(image)

    # Calculate channel averages
    avg_b = np.mean(b)
    avg_g = np.mean(g)
    avg_r = np.mean(r)

    # Calculate overall brightness

    # Calculate overall brightness
    avg_int = (avg_b + avg_g + avg_r) / 3

    return {
        'brightness': int(avg_int),
        'b': avg_b,
        'g': avg_g,
        'r': avg_r
    }
```

### Audio Feature Extraction
Using the function below, we calculate noise level.

```python
def calculate_noise_level(audio_file: Path) -> float:
    """
    Calculate the noise level of an audio file in decibels (dB).

    Uses the formula: LdB = 10 * log10(1/N * Σ(x[n]²))
    where:
    - x[n] is the amplitude at time step n
    - N is total number of samples (duration * sample_rate)

    Args:
        audio_file (Path): Path to the audio file

    Returns:
        float: Noise level in decibels (dB)
    """
    # Load audio file with original sampling rate
    signal, sr = librosa.load(audio_file, sr=None)

    signal_square = np.square(signal)
    signal_square_mean = np.mean(signal_square)
    rms = np.sqrt(signal_square_mean)

    # Convert RMS to dB
    # 20 is here just as a scaling factor
    noise_level_db = 20 * np.log10(rms)

    return noise_level_db
```

Here, we read each environmental noise audio file and compute noise level for it.
1. Using librosa, compute the noise level.
2. Merging the noise level data with main data.
3. Plotting the density on map. 


## Analysis To Perform
### Distribution Analysis
We plot the distribution plot of the calculated features. It allows us to answer the questions:
1. What is the distribution of vehicle/people count observed on images?
2. What is the distribution of noise level?
3. What is the distribution of greeness level?

### Density Analysis
We plot the map plot and view the density of the data. We can answer the questions:
1. Which are the places with most greenery value?
2. Which places are most noisy?
4. What are the most/least crowded places?

### Correlation Analysis
We select columns representing sentiment tags and features from image and noise then find correlation. It is as easy as `df.corr()`.

1. What are the strong correlations found in of sentiment tags with features?
2. Does the correlation vary on various place?
3. Are there any other ways to group the data and find the correlation? 