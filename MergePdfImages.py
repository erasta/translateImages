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
    return new_im, offsets[:-1]

def vconcat(images):
    widths, heights = zip(*(i.size for i in images))
    new_im = Image.new('RGB', (max(widths), sum(heights)))
    offsets = [0]
    for im in images:
        new_im.paste(im, (0, offsets[-1]))
        offsets.append(offsets[-1] + im.size[1])
    return new_im, offsets[:-1]

def partition(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def flatten (l):
    return [item for sublist in l for item in sublist]

def tileImages(images, numPerRow):
    p = partition(images, numPerRow)

    rows = []
    x_offsets = []
    for image_in_row in p:
        imrow, x_offsets_curr = hconcat(image_in_row)
        rows.append(imrow)
        x_offsets.append(x_offsets_curr)

    im, y_offsets = vconcat(rows)
    (w, h) = im.size

    rects = []
    for y0, y1, xs in zip(y_offsets, y_offsets[1:] + [h], x_offsets):
        for x0, x1 in zip(xs, xs[1:] + [w]):
            rects.append((x0, y0, x1, y1))

    return im, rects
    
def MergePdfImages(pdfFileNames, output_folder=None):
    if output_folder is None:
        output_folder = join(os.getcwd(), 'merged')
    makeEmptyDir(output_folder)

    images_for_pdfs = [convert_from_path(pdf) for pdf in pdfFileNames]
    images = flatten(images_for_pdfs)
    rows = 2
    cols = 2
    p = partition(images, cols * rows)
    for i, images_in_tile in enumerate(p):
        im, rects = tileImages(images_in_tile, cols)
        name = join(output_folder, 'im_' + '_' + str(i) + '.png')
        print('on ', name, ' got ', rects)
        im.save(name)
            
def combineImagesToPdf(imagesFileNames, pdfFileName):
    # Combine images to pdf
    out_images = [Image.open(n) for n in imagesFileNames]
    out_images[0].save(pdfFileName, "PDF", resolution=150.0, save_all=True, append_images=out_images[1:])

def CombineTranslatedPdf(pdfFileNames, input_orig_images=None, input_translated_images=None, output_pdfs=None):
    if input_orig_images is None:
        input_orig_images = join(os.getcwd(), 'merged')
    if input_translated_images is None:
        input_translated_images = join(os.getcwd(), 'translated')
    if output_pdfs is None:
        output_pdfs = join(os.getcwd(), 'output_pdfs')

    makeEmptyDir(output_pdfs)
    temp_folder = makeEmptyDir(join(output_pdfs, 'temp'))

    images_for_pdfs = [convert_from_path(pdf) for pdf in pdfFileNames]
    images = flatten(images_for_pdfs)
    rows = 2
    cols = 2
    index = 0
    p = partition(images, cols * rows)
    curr_image_batch = []
    batch_index = 0
    for i, images_in_tile in enumerate(p):
        im, rects = tileImages(images_in_tile, cols)
        name = join(input_orig_images, 'im__' + str(i) + '.png')
        print('on', name, 'got', rects)

        name_trans = join(input_translated_images, 'im__' + str(i) + '.png')
        im_trans = Image.open(name_trans)
        
        for (x0, y0, x1, y1) in rects:
            im0 = im.crop((x0, y0, x1, y1))
            im1 = im_trans.crop((x0, y0, x1, y1))
            imboth, _ = hconcat([im0, im1])
            name_temp = join(temp_folder, 'im_' + str(index) + '.jpg')
            index += 1
            print ('saving', name_temp, (x0, y0, x1, y1))
            imboth.save(name_temp)
            curr_image_batch.append(name_temp)
            if index % 20 == 0:
                batch_index += 1
                pdf_name = join(output_pdfs, str(batch_index) + '.pdf')
                print ('combining into', pdf_name)
                combineImagesToPdf(curr_image_batch, pdf_name)
                curr_image_batch = []

    batch_index += 1
    pdf_name = join(output_pdfs, str(batch_index) + '.pdf')
    print ('combining into', pdf_name)
    combineImagesToPdf(curr_image_batch, pdf_name)
    curr_image_batch = []

        # im.save(name)
        # imr, _ = hconcat([im, im_trans])
        # imr.save(name_temp)        
            


if __name__ == '__main__':
    # MergePdfImages([
    #     '/home/eran/Downloads/Adobe Scan Aug 28, 2023.pdf', 
    #     '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (1).pdf', 
    #     '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (3).pdf', 
    #     '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (2).pdf', 
    #     ])
    CombineTranslatedPdf([
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023.pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (1).pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (3).pdf', 
        '/home/eran/Downloads/Adobe Scan Aug 28, 2023 (2).pdf', 
        ])
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '1')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (1).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '2')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (2).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
    # TranslatePdf(temp_folder=join(os.getcwd(), 'images', '3')).go('/home/eran/Downloads/Adobe Scan Aug 28, 2023 (3).pdf', 'output.pdf', from_lang='bulgarian', to_lang='english')
