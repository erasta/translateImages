import os
from os.path import join
import shutil
import uuid
from TranslateImages import TranslateImages
from pdf2image import convert_from_path
from PIL import Image

def makeEmptyDir(folder):
    os.makedirs(folder, exist_ok=True)
    if folder not in ['', '.', '..']:
        for f in os.listdir(folder):
            if os.path.isfile(join(folder, f)):
                os.remove(join(folder, f))
    return folder

def hconcat(images):
    widths, heights = zip(*(i.size for i in images))
    new_im = Image.new('RGB', (sum(widths), max(heights)))
    offsets = [0]
    for im in images:
        new_im.paste(im, (offsets[-1], 0))
        offsets.append(offsets[-1] + im.size[0])
    return new_im

def vconcat(images):
    widths, heights = zip(*(i.size for i in images))
    new_im = Image.new('RGB', (max(widths), sum(heights)))
    offsets = [0]
    for im in images:
        new_im.paste(im, (0, offsets[-1]))
        offsets.append(offsets[-1] + im.size[1])
    return new_im

def partition(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def flatten (l):
    return [item for sublist in l for item in sublist]

def tileImages(images, numPerRow):
    p = partition(images, numPerRow)
    rows = [hconcat(image_in_row) for image_in_row in p]
    im = vconcat(rows)
    return im
    
def MergePdfImages(pdfFileNames, output_folder=None):
    if output_folder is None:
        output_folder = join(os.getcwd(), 'merged')
    makeEmptyDir(output_folder)

    images_for_pdfs = [convert_from_path(pdf) for pdf in pdfFileNames]
    images = flatten(images_for_pdfs)
    rows = 3
    cols = 3
    p = partition(images, cols * rows)
    for i, images_in_tile in enumerate(p):
        im = tileImages(images_in_tile, cols)
        name = join(output_folder, 'im_' + '_' + str(i) + '.png')
        im.save(name)

if __name__ == '__main__':
    MergePdfImages([
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023.pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (1).pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (3).pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (2).pdf', 
        ])
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '1')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (1).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '2')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (2).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '3')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (3).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
