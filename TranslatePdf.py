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

    def go(self, pdf_input, pdf_output, from_lang = 'english', to_lang = 'hebrew', input_is_images_folder=False):
        self._makedir(self.temp_folder) # cleanup
        temp_in  = self._makedir(join(self.temp_folder, 'in'))
        temp_out  = self._makedir(join(self.temp_folder, 'out'))

        input_names = []
        names = []
        if input_is_images_folder:
            for n in sorted(os.listdir(pdf_input)):
                barename = os.path.splitext(n)[0]
                names.append(barename)
                input_names.append(join(pdf_input, n))                
        else:
            # split to images
            id = uuid.uuid4().hex
            images = convert_from_path(pdf_input)
            names = ['page_' + id + '_' + str(i) for i in range(len(images))]
            for i, n in enumerate(names):
                n0 = join(temp_in, n + '.png')
                input_names.append(n0)
                images[i].save(n0, 'PNG')

        # translate images in folder, out to download folder
        TranslateImages(from_lang, to_lang).go(input_names)

        # move from download folder to temp out folder 
        for n in names:
            shutil.move(join(self.download_folder, n + '.translated.jpg'), temp_out)

        # Combine images to pdf
        out_names = [join(temp_out, n + '.translated.jpg') for n in names]
        out_images = [Image.open(n) for n in out_names]
        out_images[0].save(pdf_output, "PDF", resolution=150.0, save_all=True, append_images=out_images[1:])

    def _makedir(self, folder):
        os.makedirs(folder, exist_ok=True)
        if folder not in ['', '.', '..']:
            for f in os.listdir(folder):
                if os.path.isfile(join(folder, f)):
                    os.remove(join(folder, f))
        return folder


if __name__ == '__main__':
    # TranslatePdf().go('sample.pdf', 'output.pdf')
    TranslatePdf().go('/home/eran/Downloads/Photos-001 (3)', 'output.pdf', from_lang='bulgarian', to_lang='english', input_is_images_folder=True)
