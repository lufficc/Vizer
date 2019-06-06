# Created by lufficc
import pickle

import matplotlib.pyplot as plt
from PIL import Image

from vizer.draw import draw_boxes, draw_masks

coco_class_name = ['__bg',
                   'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                   'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
                   'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
                   'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
                   'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
                   'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
                   'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
                   'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
                   'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
                   'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
                   'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
                   'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
                   'scissors', 'teddy bear', 'hair drier', 'toothbrush'
                   ]
if __name__ == '__main__':
    name = '000000308476'
    with open('data/%s.pickle' % name, 'rb') as f:
        data = pickle.load(f)
    img = Image.open('data/%s.jpg' % name)
    img = draw_masks(img, data['masks'], data['labels'])
    img = draw_boxes(img, boxes=data['boxes'], labels=data['labels'], scores=data['scores'], class_name_map=coco_class_name, score_format=':{:.4f}')
    plt.imshow(img)
    plt.show()
