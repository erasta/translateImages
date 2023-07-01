import os
import shutil
import uuid
from TranslateImages import TranslateImages
from pdf2image import convert_from_path

class TranslatePdf:
    def __init__(self, download_folder=None, temp_folder=None) -> None:
        self.download_folder = download_folder or os.path.join(os.path.expanduser("~"), 'Downloads')
        self.temp_folder = temp_folder or os.path.join(os.getcwd(), 'images')

    def go(self, pdf_file_name):
        self._makedir(self.temp_folder) # cleanup
        temp_in  = self._makedir(os.path.join(self.temp_folder, 'in'))
        temp_out  = self._makedir(os.path.join(self.temp_folder, 'out'))

         # split to images
        id = uuid.uuid4().hex
        images = convert_from_path(pdf_file_name)
        names = ['page_' + id + '_' + str(i) for i in range(len(images))]
        for i, n in enumerate(names):
            images[i].save(os.path.join(temp_in, n + '.png'), 'PNG')

        # translate images in folder, out to download folder
        TranslateImages().go([os.path.join(temp_in, n + '.png') for n in names])

        # move from download folder to temp out folder 
        for n in names:
            shutil.move(os.path.join(self.download_folder, n + '.translated.jpg'), temp_out)

    def _makedir(self, folder):
        os.makedirs(folder, exist_ok=True)
        if folder not in ['', '.', '..']:
            for f in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, f)):
                    os.remove(os.path.join(folder, f))
        return folder


if __name__ == '__main__':
    TranslatePdf().go('sample.pdf')
