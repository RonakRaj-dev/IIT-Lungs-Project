import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# --- CONFIGURATION ---
AUDITED_CORRECT_DIR = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\Datasets\datasets\bbox_audited\Correct'
BBOX_CSV = r'C:\Users\gamer\OneDrive\Desktop\IIT Project\utils\updated_annotations.csv'
TARGET_SIZE = (512, 512)
ORIG_RES = 1024
TARGET_CLASSES = ['Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltrate', 'Mass', 'Nodule', 'Pneumonia',
                  'Pneumothorax']


def prepare_audited_data():
    df = pd.read_csv(BBOX_CSV)

    # Get list of filenames you marked as 'Correct'
    correct_files = os.listdir(AUDITED_CORRECT_DIR)

    # Filter CSV to only include these images
    train_df = df[df['Image Index'].isin(correct_files)]

    images, labels, bboxes = [], [], []

    print(f"📦 Loading {len(correct_files)} audited images...")
    for idx, row in train_df.iterrows():
        img_path = os.path.join(AUDITED_CORRECT_DIR, row['Image Index'])

        # Image Processing
        img = load_img(img_path, target_size=TARGET_SIZE)
        img = img_to_array(img) / 255.0
        images.append(img)

        # Labels (Multi-label)
        labels.append(row[TARGET_CLASSES].values.astype('float32'))

        # Normalized BBoxes [x, y, w, h] scaled to [0, 1]
        bboxes.append([row['x'] / ORIG_RES, row['y'] / ORIG_RES, row['w'] / ORIG_RES, row['h'] / ORIG_RES])

    return np.array(images), np.array(labels), np.array(bboxes)



X, Y_class, Y_bbox = prepare_audited_data()

from tensorflow.keras import layers, models, applications

def build_heavy_teacher():
    # DenseNet-121 is superior for medical textures
    base_model = applications.DenseNet121(input_shape=(512, 512, 3),
                                          include_top=False,
                                          weights='imagenet')
    base_model.trainable = True # Unfreeze for fine-tuning since we have clean data

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)

    # Output 1: Disease Classification (Sigmoid for multi-label)
    class_out = layers.Dense(len(TARGET_CLASSES), activation='sigmoid', name='class_out')(x)

    # Output 2: Bounding Box Regression (Sigmoid for normalized 0-1 range)
    bbox_out = layers.Dense(4, activation='sigmoid', name='bbox_out')(x)

    model = models.Model(inputs=base_model.input, outputs=[class_out, bbox_out])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), # Low LR for fine-tuning
        loss={'class_out': 'binary_crossentropy', 'bbox_out': 'mse'},
        loss_weights={'class_out': 1.0, 'bbox_out': 5.0}, # Focus heavily on box precision
        metrics={'class_out': 'binary_accuracy', 'bbox_out': 'mae'}
    )
    return model

# Initialize and Train
model = build_heavy_teacher()

print("\n🚀 Training Heavy Teacher on Audited Dataset...")
history = model.fit(
    X,
    {'class_out': Y_class, 'bbox_out': Y_bbox},
    epochs=30,
    batch_size=4, # Keep small for 512px memory limits
    validation_split=0.1,
    verbose=1
)

# Save the final teacher
model.save('heavy_teacher_final.h5')