import sys
import os
import datetime
import shutil
import warnings
from tqdm import tqdm
import math
import random

FOLDER_SPLITS = ['train', 'val', 'test']
TMP_FOLDER = 'tmp'

INPUT_MODE = False

# Get command-line arguments
args = sys.argv[1:] # Skip the first argument, which is the script name

# Parse arguments
try:
    tmp = float(args[1])
    formatted_imgs_path = args[0]
except ValueError:
    unformatted_imgs_path = args[0]
    formatted_imgs_path = args[1]
    INPUT_MODE = True

splits = {}
split_sum = 0
for i, split in enumerate(FOLDER_SPLITS):
    if INPUT_MODE:
        splits[split] = float(args[2 + i])
    else:
        splits[split] = float(args[1 + i])
    split_sum += splits[FOLDER_SPLITS[i]]

# Calculate ratios for the splits
split_ratios = {}
for i, split in enumerate(FOLDER_SPLITS):
    split_ratios[split] = splits[split] / split_sum

if not os.path.exists(formatted_imgs_path):
    os.makedirs(formatted_imgs_path)

    # Make temporary folder for moving all trash images into prior to splitting them
    tmp_dir_path = os.path.join(formatted_imgs_path, 'tmp')
    try:
        os.makedirs(tmp_dir_path)
    except FileExistsError:
        raise RuntimeError(f'FileExistsError: \"{TMP_FOLDER}\" folder exists within existing dataset path. Please delete this folder before running the script.')

    existing_labels = set()

else:    
    if INPUT_MODE:
        # Check if destination dataset folder already exist or not
        while True:
            response = input('Dataset folder already exists! Include new trash data into this dataset? (y/n): ')
            if response.lower() == 'y':
                print('Continuing with existing dataset folder: ', os.path.basename(formatted_imgs_path))
                break
            elif response.lower() == 'n':
                sys.exit()
            else:
                print('Invalid response, please try again.')

    # Make temporary folder for moving all trash images into prior to splitting them
    tmp_dir_path = os.path.join(formatted_imgs_path, 'tmp')
    try:
        os.makedirs(tmp_dir_path)
    except FileExistsError:
        raise RuntimeError(f'FileExistsError: \"{TMP_FOLDER}\" folder exists within existing dataset path. Please delete this folder before running the script.')

    # Import existing labels
    existing_labels = set()
    for folder_name in FOLDER_SPLITS:
        try:
            existing_labels |= set(os.listdir(os.path.join(formatted_imgs_path, folder_name)))
        except FileNotFoundError:
            warnings.warn(f'Warning: \"{folder_name}\" folder not found within existing dataset.', UserWarning)

    # Make folders from existing labels
    for label in existing_labels:
        os.makedirs(os.path.join(tmp_dir_path, label))

# Import new dataset labels
if INPUT_MODE:
    new_labels = set(os.listdir(unformatted_imgs_path))

    # Check for mismatching labels between new and old dataset
    mismatched_labels = new_labels.difference(existing_labels)

    if len(mismatched_labels) > 0:
        while True:
            if len(existing_labels) > 0:
                response = input('Found new labels within new dataset. Include new labels to the existing dataset? (y/n): ')
            else:
                response = 'y'

            if response.lower() == 'y':
                for mismatched_label in mismatched_labels:
                    if len(os.listdir(os.path.join(unformatted_imgs_path, mismatched_label))) == 0:
                        shutil.rmtree(tmp_dir_path)
                        raise RuntimeError(f'Folder \"{mismatched_label}\" within new dataset cannot be empty')
                    os.makedirs(os.path.join(tmp_dir_path, mismatched_label))
                break
            elif response.lower() == 'n':
                break
            else:
                print('Invalid response, please try again.')


labels_to_import = os.listdir(tmp_dir_path)

# Move images within existing dataset into tmp folder
for folder_name in FOLDER_SPLITS:
    formatted_folder_path = os.path.join(formatted_imgs_path, folder_name)
    for label in labels_to_import:
        tmp_dir_label_path = os.path.join(tmp_dir_path, label)
        formatted_label_path = os.path.join(formatted_folder_path, label)
        try:
            imgs_list = os.listdir(formatted_label_path)
            for img_name in tqdm(imgs_list, desc=f'Importing images from {formatted_label_path}'):
                img_path = os.path.join(formatted_label_path, img_name)

                if os.path.exists(os.path.join(tmp_dir_label_path, img_name)):
                    now = datetime.datetime.now()
                    now_str = now.strftime("%Y%m%d%H%M%S%f")

                    new_img_name = f'{img_name}_{now_str}'
                    new_img_path = os.path.join(tmp_dir_label_path, new_img_name)
                    warnings.warn(f'Warning: Found duplicate file name when moving \"{img_name}\". Renaming file to \"{new_img_name}\"', UserWarning)
                else:
                    new_img_path = os.path.join(tmp_dir_label_path, img_name)

                shutil.move(img_path, new_img_path)
        except FileNotFoundError:
            pass

# Move images from new dataset to tmp folder
if INPUT_MODE:
    for label in labels_to_import:
        tmp_dir_label_path = os.path.join(tmp_dir_path, label)
        unformatted_label_path = os.path.join(unformatted_imgs_path, label)
        try:
            imgs_list = os.listdir(unformatted_label_path)
            for img_name in tqdm(imgs_list, desc=f'Importing images from {unformatted_label_path}'):
                img_path = os.path.join(unformatted_label_path, img_name)

                if os.path.exists(os.path.join(tmp_dir_label_path, img_name)):
                    now = datetime.datetime.now()
                    now_str = now.strftime("%Y%m%d%H%M%S%f")

                    new_img_name = f'{os.path.splitext(img_name)[0]}_{now_str}{os.path.splitext(img_name)[1]}'
                    new_img_path = os.path.join(tmp_dir_label_path, new_img_name)
                    warnings.warn(f'Warning: Found duplicate file name when copying \"{img_name}\". Renaming file to \"{new_img_name}\"', UserWarning)
                else:
                    new_img_path = os.path.join(tmp_dir_label_path, img_name)

                shutil.copy(img_path, new_img_path)
        except FileNotFoundError:
            pass

# Calculate number of files in each split
split_imgs_count = {}
for split in FOLDER_SPLITS:
    imgs_counts = {}
    for label in labels_to_import:
        tmp_dir_label_path = os.path.join(tmp_dir_path, label)
        imgs_list = os.listdir(tmp_dir_label_path)
        imgs_count = len(imgs_list)

        imgs_counts[label] = math.ceil(imgs_count * split_ratios[split])
    split_imgs_count[split] = imgs_counts

# Copy images from tmp to destination folders
for split in FOLDER_SPLITS:
    formatted_split_path = os.path.join(formatted_imgs_path, split)
    try:
        os.makedirs(formatted_split_path)
    except FileExistsError:
        pass

    for label in tqdm(labels_to_import, desc=f'Splitting Dataset to {formatted_split_path}'):
        formatted_label_path = os.path.join(formatted_split_path, label)

        try:
            os.makedirs(formatted_label_path)
        except FileExistsError:
            pass

        tmp_dir_label_path = os.path.join(tmp_dir_path, label)
        imgs_list = os.listdir(tmp_dir_label_path)
        imgs_count = len(imgs_list)

        shuffled_list = random.sample(imgs_list, len(imgs_list))
        split_list = shuffled_list[:split_imgs_count[split][label]]
        
        for img_name in split_list:
            img_path = os.path.join(tmp_dir_label_path, img_name)
            new_img_path = os.path.join(formatted_label_path, img_name)
            shutil.move(img_path, new_img_path)

# Remove tmp folder and empty splits
for split in os.listdir(formatted_imgs_path):
    formatted_split_path = os.path.join(formatted_imgs_path, split)
    is_empty = False
    for label in tqdm(os.listdir(formatted_split_path), desc=f'Pruning empty split for {formatted_split_path}'):
        if len(os.listdir(os.path.join(formatted_split_path, label))) == 0:
            is_empty = True
    if is_empty:
        shutil.rmtree(formatted_split_path)
