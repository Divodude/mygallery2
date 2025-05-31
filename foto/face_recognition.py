from keras_facenet import FaceNet
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob
import pickle
import gc
import sys
import time
import schedule
# Reconfigure stdout encoding for compatibility
sys.stdout.reconfigure(encoding='utf-8')

# Initialize FaceNet model
facenet = FaceNet()

# Function to extract embeddings for all faces in an image
def face_extractor_fnet(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (300, 300))  # Resize for faster processing
    faces = facenet.extract(img, threshold=0.95)
    if faces:
        return [face['embedding'] for face in faces]  # Return embeddings for all faces
    return None

# Function to get image paths from a directory
def image_from_dir(dir_path):
    image_extensions = ['jpg', 'jpeg', 'png']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(dir_path, f'**/*.{ext}'), recursive=True))
    return image_files

# Function to get embeddings for all images in a directory
def get_embeddings_from_dir(dir_path=None, embd_save_path=None, batch_size=5, image_paths=None):
    if image_paths is not None:
        image_paths = image_paths

    # Load existing embeddings if available
    existing_embeddings, existing_paths = load_embeddings(embd_save_path)
    if existing_embeddings is None:
        existing_embeddings, existing_paths = [], []

    existing_paths_set = set(existing_paths)

    # Process images in batches
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        batch_embeddings = []
        batch_valid_paths = []

        for img_path in batch_paths:
            if img_path in existing_paths_set:
                print(f"Skipping existing file: {img_path}")
                continue

            embeddings = face_extractor_fnet(img_path)
            if embeddings is not None:
                for embedding in embeddings:
                    print(f"Processing: {img_path}")
                    batch_embeddings.append(embedding)
                    batch_valid_paths.append(img_path)

        existing_embeddings.extend(batch_embeddings)
        existing_paths.extend(batch_valid_paths)

        save_embeddings(existing_embeddings, existing_paths, embd_save_path)

        # Clean up memory
        del batch_embeddings, batch_valid_paths
        gc.collect()  
        print(f"Processed batch {i // batch_size + 1}/{(len(image_paths) // batch_size + 1)}")

def load_embeddings(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            embeddings, image_paths = pickle.load(f)
        return embeddings, image_paths
    return None, None

def save_embeddings(embeddings, image_paths, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump((embeddings, image_paths), f)

def find_matching_images(target_dir, main_dir, threshold=0.8):
    target_embeddings, _ = load_embeddings(target_dir)
    main_embeddings, main_image_paths = load_embeddings(main_dir)

    matching_images = []

    for i, main_embedding in enumerate(main_embeddings):
        for target_embedding in target_embeddings:
            similarity = cosine_similarity([target_embedding], [main_embedding])[0][0]
            if similarity >= threshold:
                matching_images.append(main_image_paths[i])
                break 

    return matching_images

def display_matching_images(matching_images):
    if len(matching_images) == 0:
        print("No matching images found.")
        return

    fig, axs = plt.subplots(1, len(matching_images), figsize=(20, 10))
    if len(matching_images) == 1:
        matching_images = [matching_images]

    for i, image_path in enumerate(matching_images):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        axs[i].imshow(img)
        axs[i].axis('off')
        axs[i].set_title(os.path.basename(image_path))
    plt.show()

def run_midnight_embedding_extraction():
    dir_path = r"static\userimages\images"  
    embd_save_path = "main.pkl" 
    image_paths = image_from_dir(dir_path)
    get_embeddings_from_dir(dir_path, embd_save_path, image_paths=image_paths)


