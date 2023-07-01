import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TranslateImages:
    def go(self, filename_list):
        driver = webdriver.Chrome()

        driver.get("https://translate.yandex.com/en/ocr?source_lang=he&target_lang=en")

        self.actions = ActionChains(driver)

        [x0, y0] = [33, 184]
        points = [
            [400, 290],
            [130, 730],
            [500, 280],
            [130, 1040]
        ]
        download_point = [725, 285]
        clear_point = [810, 285]

        [self.xp, self.yp] = [0, 0]

        def click_point(p):
            [xt, yt] = [p[0], p[1]]
            [x1, y1] = [xt - x0, yt - y0]
            [xm, ym] = [x1 - self.xp, y1 - self.yp]
            # print('[x0, y0]=', [x0, y0],'[x1, y1]=', [x1, y1],'[xm, ym]=', [xm, ym],'[xp, yp]=', [self.xp, self.yp])
            [self.xp, self.yp] = [x1, y1]
            self.actions.move_by_offset(xm, ym)
            self.actions.click().perform()

        for p in points:
            click_point(p)

        file_button = driver.find_element(By.ID, "fileInput")

        for filename in filename_list:
            file_button.send_keys(filename)
            time.sleep(3)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "downloadButton")))#.get_attribute("src")
            click_point(download_point)
            time.sleep(1)
            click_point(clear_point)
            time.sleep(1)

        driver.quit()

if __name__ == '__main__':
    folder = os.path.expanduser("~") + "/Downloads/Scanned_20230516-1246"
    files_in_folder = sorted(os.listdir(folder))
    files = [os.path.join(folder, f) for f in files_in_folder]
    TranslateImages().go(files)
    