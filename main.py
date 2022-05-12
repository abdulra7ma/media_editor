import glob
import os
from os.path import isdir, join

from PIL import Image, ImageDraw, ImageFont


def watermark_image(image, watermark_text="WHATS POPEN"):
    """
    Adds watermark to the input image.
    Returns -> PIL image object
    """

    font =  ImageFont.truetype("fonts/arial.ttf", 50)

    canva = ImageDraw.Draw(image)
    textwidth, textheight = canva.textsize(watermark_text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    width, height = image.size
    x = width - textwidth - margin
    y = height - textheight - margin
    
    # draw watermark text
    canva.text((x, y), watermark_text, (255,0,0), font=font)

    return image


def crop_image_and_add_watermark(images_folder, size=(1080, 1080)):
    """
    Crops all the images of one folder by 1080 x 1080,
    and add watermark text to the image file
    Returns a list of PIL objects.
    """
    pil_images_list = []

    for img in glob.glob(images_folder + "/*"):
        image_name = "".join(img.split(".")[::-1][1:][::-1]).split("/")[-1]
        image_extension = img.split(".")[-1]

        image_obj = Image.open(img)
        cropped_image = image_obj.resize(size)
        cropped_images_folder = os.path.abspath("edited_images")
        copped_image_path = join(
            cropped_images_folder,
            f"{image_name}_cropped.{image_extension}",
        )

        if isdir(cropped_images_folder):
            # add watermark to the image
            cropped_image = watermark_image(cropped_image)
            cropped_image.save(copped_image_path)
        else:
            # if cropped_images folder does not exists
            # than create it and save the image
            os.mkdir("edited_images")

            # add watermark to the image
            cropped_image = watermark_image(cropped_image)
            cropped_image.save(copped_image_path)

        pil_images_list.append(image_obj)

    return pil_images_list


crop_image_and_add_watermark("images")
