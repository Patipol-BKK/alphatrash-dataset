# alphatrash-dataset
 
This dataset is a part of the [AlphaTrash project](https://github.com/Patipol-BKK/alphatrash) which has been published in the paper: Automatic Trash Classification using Convolutional Neural Network Machine Learning.

## Contents

The folder [trash_dataset](trash_dataset) contains trash image files that has been collected in this project. All of the trash here are from Thailand and the images has been taken using a Raspberry Pi Camera Module 2 within the trash disposal compartment of the AlphaTrash system. Here, the dataset has been structured as `train/`, `val/`, and `test/` for training, validation, and testing data which currently has a 70%, 15%, 15% split. 

The images within each splits are organized in labeled folders as follows:

- `general/`: Miscellaneous trash that couldn't be categorized in the following categories - 1190 images
- `metal/`: Metal waste (Current dataset only contains soda cans)                                  - 1065 images
- `organic/`: Organic waste such as food scraps, vegetable or fruit peels.                         - 819  images
- `paper/`: Paper and cardboard waste                                                              - 895  images
- `plasic/`: Plastic waste                                                                         - 1722 images

## Adding New Images to the Dataset

To add new images to the current dataset, organize the image files by grouping them into folders that are named after their labels. Then group these in to a new single folder named e.g. `new_dataset/` that is located in the main directory and run the [formatter.py](formatter.py) script to auto format them.

The format for the command is as follow:
```
python formatter.py path/to/new_dataset_folder/ path/to/destination_folder/ train_ratio val_ratio test_ratio
```

This command imports the new images from `new_dataset/` into the current trash_dataset and split them into 60% `train/`, 20% `val/`, and 20% `test/`:
```
python formatter.py new_dataset trash_dataset 0.6 0.2 0.2
```

This command creates a new dataset named `trash_dataset_2/` from `new_dataset/` with 70% `train/`, 0% `val/`, and 30% `test/` split:
```
python formatter.py new_dataset trash_dataset_2 0.7 0 0.3
```

## Re-Splitting or Re-Shuffling of Current Dataset

To re-split or re-shuffle the current dataset, run the [formatter.py](formatter.py) script to auto format.

The format for the command is as follow:
```
python formatter.py path/to/dataset_folder/ train_ratio val_ratio test_ratio
```

This command redistribute images within the current trash_dataset into 80% `train/`, 10% `val/`, and 10% `test/` splits:
```
python formatter.py trash_dataset_2 0.8 0.1 0.1
```

## Future Contribution and Contact Information
If you are interested in contributing to this dataset or have any inquiries, please feel free to contact me at [patipol.ti@gmail.com](patipol.ti@gmail.com).
