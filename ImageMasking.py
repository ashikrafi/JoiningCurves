import functools
import io
import numpy as np
from PIL import Image
from pymatting.alpha.estimate_alpha_cf import estimate_alpha_cf
from pymatting.foreground.estimate_foreground_ml import estimate_foreground_ml
from pymatting.util.util import stack_images
from scipy.ndimage.morphology import binary_erosion
import detect
from Resizer import GetImageContour


def alpha_matting_cutout(
        img,
        mask,
        foreground_threshold,
        background_threshold,
        erode_structure_size,
        base_size,
):
    size = img.size

    img.thumbnail((base_size, base_size), Image.LANCZOS)
    mask = mask.resize(img.size, Image.LANCZOS)

    img = np.asarray(img)
    mask = np.asarray(mask)

    # foreground/background
    is_foreground = mask > foreground_threshold
    is_background = mask < background_threshold

    # erase foreground/background
    structure = None
    if erode_structure_size > 0:
        structure = np.ones((erode_structure_size, erode_structure_size), dtype=np.long)

    is_foreground = binary_erosion(is_foreground, structure=structure)
    is_background = binary_erosion(is_background, structure=structure, border_value=1)

    # 0   = background
    # 128 = unknown
    # 255 = foreground
    trimap = np.full(mask.shape, dtype=np.uint8, fill_value=128)
    trimap[is_foreground] = 255
    trimap[is_background] = 0

    # build the cutout image
    img_normalized = img / 255.0
    trimap_normalized = trimap / 255.0

    alpha = estimate_alpha_cf(img_normalized, trimap_normalized)
    foreground = estimate_foreground_ml(img_normalized, alpha)
    cutout = stack_images(foreground, alpha)

    cutout = np.clip(cutout * 255, 0, 255).astype(np.uint8)
    cutout = Image.fromarray(cutout)
    cutout = cutout.resize(size, Image.LANCZOS)

    return cutout


def naive_cutout(img, mask, input_path, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage):
    mask = mask.resize(img.size, Image.LANCZOS)
    mask.save('Images/Conversion/MaskOutput.jpg')
    GetImageContour('Images/Conversion/MaskOutput.jpg', input_path, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage)
    empty = Image.new("RGBA", img.size, 0)
    cutout = Image.composite(img, empty, mask.resize(img.size, Image.LANCZOS))
    return cutout


@functools.lru_cache(maxsize=None)
def get_model(model_name):
    if model_name == "u2netp":
        return detect.load_model(model_name="u2netp")
    else:
        return detect.load_model(model_name="u2net")


def remove(data, input_path='', leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0, IsPercentage=False):
    model_name = "u2net",
    model = get_model(model_name)
    img = Image.open(io.BytesIO(data)).convert("RGB")
    mask = detect.predict(model, np.array(img)).convert("L")

    cutout = naive_cutout(img, mask, input_path, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage)

    bio = io.BytesIO()
    cutout.save(bio, "PNG")

    return bio.getbuffer()
