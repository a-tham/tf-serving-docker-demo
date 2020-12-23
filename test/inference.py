import requests
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
from tensorflow import nn

# Batchsize for inference set to number of cells in folder for inference sorting later
def get_bs(folder='test_data'):
    bs = len(os.listdir(os.path.join(folder, os.listdir(folder)[0])))
    return bs

def get_removals(config, location):
    # Cell numbers that are unneeded for training eg. sky, trees etc
    removals_config = config['removals'][location]

    all_cells = []

    for i in removals_config:
        if type(i) == int:
            i = [x for x in range(i)]
            all_cells.append(i)
        else:
            all_cells.append(i)

    removals = [j for i in all_cells for j in i]

    return removals

#Image data generator
def datagen(batch_size, img_folder='test_data'):
    test_datagenerator = ImageDataGenerator()

    test_img_gen = test_datagenerator.flow_from_directory(
        img_folder,
        target_size=(32, 32),
        color_mode="rgb",
        classes=None,
        class_mode=None,
        batch_size=batch_size,
        shuffle=False,
        seed=None,
        save_to_dir=None,
        save_prefix="",
        save_format="jpg",
        follow_links=False,
        subset=None,
        interpolation="nearest",
    )

    return test_img_gen

#server URL
def url_hit(model_name):
    url = 'http://localhost:8501/v1/models/{}:predict'.format(model_name)
    return url

#Predictions
def make_prediction(instances, url):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    predictions = np.squeeze(nn.softmax(predictions))
    return predictions

# Full function
def img_pred(data, model, removals, batch_size, input_folder='test_data'):

    filenames = [i + '.jpg' for i in os.listdir(input_folder)]
    cell_num = [int(i.split('.')[-2].split('_')[-1]) for i in data.filenames[:batch_size]]
    zeros = np.full((len(removals), 5), -1)
    masked_items = list(zip(removals, zeros))

    preds = []

    for i in range(len(data)):
        preds.append(make_prediction(data[i], url_hit(model)))

    final_proba = []

    for i in preds:
        zipped_proba = (list(zip(cell_num, i)))
        proba = sorted(list(zipped_proba + masked_items), key=lambda x: x[0])
        proba = [i[-1] for i in proba]
        final_proba.append(np.array(proba).reshape(22, 40, 5))

    return final_proba, filenames