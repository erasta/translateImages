# translateImages
Translate multiple images with python selenium on Yandex translate webpage
Uses coordinates of mouse clicks since some of the buttons are ghosts.

## Setup
```sh
git clone https://github.com/erasta/translateImages.git
cd translateImages
pipenv shell && pipenv install
```
## Run
```sh
python -m main
```

Note:  
If coordinates are wrong, reconfigure them manually using
```sh
sh coords.sh
```