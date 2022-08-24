import warnings
import cv2
import numpy as np
from PIL import Image
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer
from google.colab.patches import cv2_imshow

warnings.filterwarnings("ignore")
setup_logger()

im = cv2.imread("/home/kow/PycharmProjects/ImageBkRemoval/Images/Person_01.jpg")
print("Image dimensions:", im.shape)
print("\nImage array:")
print(im[0])


cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)
outputs = predictor(im)

v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=0.8)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2_imshow(out.get_image()[:, :, ::-1])

print(outputs["instances"].pred_classes)
print(outputs["instances"].pred_masks)

predictor.metadata.as_dict()["thing_classes"][0]
print(predictor.metadata.as_dict()["thing_classes"])

class_ids = np.array(outputs["instances"].pred_classes.cpu())
class_index = np.where(class_ids == 0)
mask_tensor = outputs["instances"].pred_masks[class_index]
print(mask_tensor.shape)
print(mask_tensor)

hobbes_mask = mask_tensor.cpu()
print("Before:", type(hobbes_mask))
print(hobbes_mask.shape)
hobbes_mask = np.array(hobbes_mask[0])
print("After:", type(hobbes_mask))
print(hobbes_mask.shape)

background = np.zeros(hobbes_mask.shape)
background.shape

bin_mask = np.where(hobbes_mask, 255, background).astype(np.uint8)
print(bin_mask)
im = Image.fromarray(bin_mask)
im.save("/home/kow/PycharmProjects/ImageBkRemoval/Images/Person_01_Masking.jpg")
