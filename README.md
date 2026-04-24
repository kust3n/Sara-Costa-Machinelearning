# Sara-Costa-Machine-learning

---

## Labb 1 - Movie Recommendation System

A content-based movie recommendation system built on the
[MovieLens](https://grouplens.org/datasets/movielens/) dataset.

### Method
Movies are represented as binary genre vectors using one-hot encoding.
A K-Nearest Neighbours model with cosine similarity finds the five most
genre-similar movies for any given input film.

### Dataset
MovieLens Latest - 86 537 movies, 33 million+ ratings.
Movies without genre information (~7 060) are excluded from the system.

### Files
- `recommendation_system.py` - data loading, feature engineering and KNN model
    Can be imported as a module or run directly from the command line (Quick instructions at beginning of code)
- `app.py` - interactive Dash web app with a searchable dropdown
- `EDA.ipynb` - exploratory data analysis with visualisations
- `report.md` - full written report

### Requirements

pandas
scikit-learn
dash

---

## Labb 2 - CNN Interpretability with TorchCAM

Course assignment exploring interpretability in convolutional neural networks
using Class Activation Maps (CAM).

### Model
ResNet18 with default ImageNet pretrained weights. Default CAM layer: `layer4`.

### Method
LayerCAM from the [torchcam](https://github.com/frgfm/torch-cam) library.
For each of the three chosen classes, one positive example (image containing
the class) and one negative example (image not containing the class) are analysed.

### Classes
- Doberman (class 236)
- Toucan (class 96)
- Siamese cat (class 284)

### Files
- `assignment2.ipynb` - main notebook with code and analysis
- `imagenet_class_index.json` - ImageNet class labels
- `doberman.jpg`, `toucan.jpg`, `siamese.jpg` - images from [Unsplash](https://unsplash.com)

### Requirements

torch
torchvision
torchcam
matplotlib
