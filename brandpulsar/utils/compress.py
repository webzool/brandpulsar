import uuid

from io import BytesIO
from PIL import Image
from django.core.files import File

def compress_image(img, instance):
    im = Image.open(img)
    im = im.convert("RGB")
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=80) 
    # create a django-friendly Files object
    new_image = File(im_io, name=f'{instance}-{str(uuid.uuid4())}.jpg')
    return new_image