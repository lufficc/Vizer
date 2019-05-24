# Created by lufficc
import cv2
import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

try:
    FONT = ImageFont.truetype('arial.ttf', 24)
except IOError:
    FONT = ImageFont.load_default()


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    palette = [2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1]
    color = [int((p * label) % 255) for p in palette]
    return tuple(color)


def _draw_single_box(image, xmin, ymin, xmax, ymax, color=(0, 255, 0), display_str=None, font=None, width=2, alpha=0.5):
    if font is None:
        font = FONT

    draw = ImageDraw.Draw(image, mode='RGBA')
    left, right, top, bottom = xmin, xmax, ymin, ymax
    alpha_color = color + (int(255 * alpha),)
    draw.rectangle([(left, top), (right, bottom)], outline=color, width=width)

    if display_str:
        text_bottom = bottom
        # Reverse list and print from bottom to top.
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            xy=[(left + width, text_bottom - text_height - 2 * margin - width),
                (left + text_width + width, text_bottom - width)],
            fill=alpha_color)
        draw.text((left + margin + width, text_bottom - text_height - margin - width),
                  display_str,
                  fill='black',
                  font=font)

    return image


def draw_boxes(image,
               boxes,
               labels=None,
               scores=None,
               class_name_map=None,
               width=2,
               alpha=0.5,
               font=None):
    """Draw bboxes(labels, scores) on image
    Args:
        image: numpy array image, shape should be (height, width, channel)
        boxes: bboxes, shape should be (N, 4), and each row is (xmin, ymin, xmax, ymax)
        labels: labels, shape: (N, )
        scores: label scores, shape: (N, )
        class_name_map: list or dict, map class id to class name for visualization.
        width: box width
        alpha: text background alpha
        font: text font
    Returns:
        An image with information drawn on it.
    """
    boxes = np.array(boxes)
    num_boxes = boxes.shape[0]
    if isinstance(image, Image.Image):
        draw_image = image
    elif isinstance(image, np.ndarray):
        draw_image = Image.fromarray(image)
    else:
        raise AttributeError('Unsupported images type {}'.format(type(image)))

    for i in range(num_boxes):
        display_str = ''
        color = (0, 255, 0)
        if labels is not None:
            this_class = labels[i]
            color = compute_color_for_labels(this_class)
            class_name = class_name_map[this_class] if class_name_map is not None else str(this_class)
            display_str = class_name

        if scores is not None:
            prob = scores[i]
            if display_str:
                display_str += ':{:.2f}'.format(prob)
            else:
                display_str += 'score:{:.2f}'.format(prob)

        draw_image = _draw_single_box(image=draw_image,
                                      xmin=boxes[i, 0],
                                      ymin=boxes[i, 1],
                                      xmax=boxes[i, 2],
                                      ymax=boxes[i, 3],
                                      color=color,
                                      display_str=display_str,
                                      font=font,
                                      width=width,
                                      alpha=alpha)

    image = np.array(draw_image, dtype=np.uint8)
    return image


def draw_masks(image,
               masks,
               labels=None,
               border=True,
               border_width=2,
               border_color=(255, 255, 255),
               alpha=0.5,
               color=None):
    """
    Args:
        image: numpy array image, shape should be (height, width, channel)
        masks: (N, 1, Height, Width)
        labels: mask label
        border: draw border on mask
        border_width: border width
        border_color: border color
        alpha: mask alpha
        color: mask color

    Returns:
        np.ndarray
    """
    assert isinstance(image, np.ndarray)
    masks = np.array(masks)
    for i, mask in enumerate(masks):
        mask = mask.squeeze()[:, :, None].astype(np.bool)

        label = labels[i] if labels is not None else 1
        _color = compute_color_for_labels(label) if color is None else tuple(color)

        image = np.where(mask,
                         mask * np.array(_color) * alpha + image * (1 - alpha),
                         image)
        if border:
            _, contours, hierarchy = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            image = cv2.drawContours(image, contours, -1, border_color, thickness=border_width, lineType=cv2.LINE_AA)

    image = image.astype(np.uint8)
    return image
