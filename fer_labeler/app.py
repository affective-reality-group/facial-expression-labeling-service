import csv
import random
from pathlib import Path
from typing import Tuple, Optional

from flask import Flask, render_template, request, jsonify

INCLUDE_GIFS = True
GIF_DIR_NAME = 'gifs'
IMAGE_DIR_NAME = 'images'
STATIC_DIR = Path(__file__).parent / 'static'
IMAGE_DIR = STATIC_DIR / IMAGE_DIR_NAME
CSV_FILE = Path(__file__).parent / 'labels.csv'

if not CSV_FILE.exists():
    image_files = [img.name for img in IMAGE_DIR.glob('*.png')]
    with CSV_FILE.open(mode='w', newline='') as new_file:
        writer = csv.writer(new_file)
        for img in image_files:
            writer.writerow([img, ''])

MESSAGE_TEMPLATE = 'Seems like all images have been labeled - Great Job'
FUNKY_EMOJIS = ["(ง︡'-'︠)ง", "(ɔ◔‿◔)ɔ", "ᕙ(`▿´)ᕗ", "（っ＾▿＾）", "(づ｡◕‿‿◕｡)づ"]

app = Flask(__name__)


@app.route('/')
def index():
    image_file, total_num_images, num_labeled_images = get_next_image_and_progress()
    gif_file = fetch_gif_file(image_file)

    if image_file:
        message = None
        image_name = image_file.split('/')[1]
    else:
        message = f'{MESSAGE_TEMPLATE} {random.choice(FUNKY_EMOJIS)}'
        image_name = None

    return render_template('index.html',
                           image_file=image_file,
                           gif_file=gif_file,
                           message=message,
                           image_name=image_name,
                           progress=f'{num_labeled_images}/{total_num_images}')


def fetch_gif_file(image_file: str) -> Optional[str]:
    if INCLUDE_GIFS and image_file is not None:
        gif_name = image_file.split('/')[1].replace('.png', '.gif')
        if (STATIC_DIR / GIF_DIR_NAME / gif_name).exists():
            return f'{GIF_DIR_NAME}/{gif_name}'


@app.route('/label', methods=['POST'])
def label_image():
    data = request.json
    image_name = data['image_name']
    label = data['label']
    save_label(image_name, label)
    return jsonify({'message': 'Label saved successfully'})


def get_next_image_and_progress() -> Tuple[Optional[str], int, int]:
    """
    :return: a Tuple of
    - the string path to an unlabeled image or None
    - the total number of images
    - the number of already labeled images
    """
    unlabeled_images = []
    total_num_images = 0

    with CSV_FILE.open(mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            total_num_images += 1
            if row[1] == '':
                unlabeled_images.append(f'{IMAGE_DIR_NAME}/{row[0]}')

    if unlabeled_images:
        return random.choice(unlabeled_images), total_num_images, total_num_images - len(unlabeled_images)
    else:
        return None, total_num_images, total_num_images


def save_label(image_name, label) -> None:
    temp_rows = []
    with CSV_FILE.open(mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == image_name:
                row[1] = label
            temp_rows.append(row)

    with CSV_FILE.open(mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(temp_rows)


if __name__ == '__main__':
    app.run(debug=True)
