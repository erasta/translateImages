import os
from os.path import join
import shutil
import uuid
from TranslateImages import TranslateImages
from pdf2image import convert_from_path
from PIL import Image

class TranslatePdf:
    def __init__(self, download_folder=None, temp_folder=None) -> None:
        self.download_folder = download_folder or join(os.path.expanduser("~"), 'Downloads')
        self.temp_folder = temp_folder or join(os.getcwd(), 'images')

    def go(self, pdf_file_name, pdf_output):
        self._makedir(self.temp_folder) # cleanup
        temp_in  = self._makedir(join(self.temp_folder, 'in'))
        temp_out  = self._makedir(join(self.temp_folder, 'out'))

         # split to images
        id = uuid.uuid4().hex
        images = convert_from_path(pdf_file_name)
        names = ['page_' + id + '_' + str(i) for i in range(len(images))]
        for i, n in enumerate(names):
            images[i].save(join(temp_in, n + '.png'), 'PNG')

        # translate images in folder, out to download folder
        TranslateImages().go([join(temp_in, n + '.png') for n in names])

        # move from download folder to temp out folder 
        for n in names:
            shutil.move(join(self.download_folder, n + '.translated.jpg'), temp_out)

        # Combine images to pdf
        out_names = [join(temp_out, n + '.translated.jpg') for n in names]
        out_images = [Image.open(n) for n in out_names]
        out_images[0].save(pdf_output, "PDF", resolution=100.0, save_all=True, append_images=out_images[1:])

    def _makedir(self, folder):
        os.makedirs(folder, exist_ok=True)
        if folder not in ['', '.', '..']:
            for f in os.listdir(folder):
                if os.path.isfile(join(folder, f)):
                    os.remove(join(folder, f))
        return folder


if __name__ == '__main__':
    TranslatePdf().go('sample.pdf', 'output.pdf')
    # temp_out = 'images/out'
    # out_names = sorted(os.listdir(temp_out))
    # # for n in out_names:
    # #     im = Image.open(join(temp_out, n))
    # #     im.save(join('images/out2', n + '.png'))
    # out_images = [Image.open(join(temp_out, n)) for n in out_names]
    # # for 
    # print(out_images)
    # pdf_output = 'output.pdf'
    # out_images[0].save(pdf_output, "PDF", resolution=100.0, save_all=True, append_images=out_images[1:])
