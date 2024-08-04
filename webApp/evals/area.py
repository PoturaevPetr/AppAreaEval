import numpy as np
import cv2, io, os
from config import config


class Helper():
    @staticmethod
    def data_area_bar(areas_list, count):
        ### логический баг, неверно определяет контуры, неверно считает площади, появилась после обновления под ручной поиск
        """Пострение диаграммы распределения по площади кристаллов"""

        areas = [i for i in areas_list if type(i) != str]
        MIN = min(areas)
        MAX = max(areas)
        
        DELTA = (MAX-MIN)/count
        count = np.arange(MIN, MAX, DELTA)
        div_area = []
        titles = []
        for i in count:
            area_count = []

            titles += [str(i) + ' - ' + str(i + DELTA)]
            for j in areas:
                if i <= j <= i + DELTA:
                    area_count.append(float(j))
            div_area.append(len(area_count))

        index = [float(i) for i in range(len(titles))]
        return index, div_area, titles

class Vision():
    def __init__(self):
        self.image_top = None
        self.image_side = None
        self.src = {}
        self.edited = {}
    
    def clear(self):
        self.image_top = None
        self.image_side = None
        self.src = {}
        self.edited = {}
    
    def read_images(self, type):
        img = cv2.imread(os.path.join(config['WEB_APP']['data_path'], "temp.png"))
        self.src[type] = img
        self.edited[type] = img

    def preview(self, type, part):
        if part == "src":
            image = self.src[type]
        else:
            image = self.edited[type]

        is_success, buffer = cv2.imencode(".png", image)
        return io.BytesIO(buffer).read()
        
    def crop(self, type, params:dict):
        image = self.src[type]
        self.px, self.py, _ = image.shape

        x_set = params.get("x", [0, self.px])
        y_set = params.get("y", [0, self.py])
        x0 = int(x_set[0]) if x_set[0] != '' else 0
        x1 = int(x_set[1]) if x_set[1] != '' else self.px
        y0 = int(y_set[0]) if y_set[0] != '' else 0
        y1 = int(y_set[1]) if y_set[1] != '' else self.py
        image = image[
            int(x0):int(x1), 
            int(y0):int(y1), 
            :
        ]     
        self.edited[type] = image
        start_point, end_point = (y0, x0), (y1, x1)
        self.add_rect(type, start_point, end_point)
    
    def add_rect(self, type, start_point, end_point):
        color = (0, 0, 255) 
        thickness = 5
        rect_image = cv2.rectangle(self.src[type].copy(), start_point, end_point, color, thickness)
        self.edited[type + "_rect"] = rect_image

    
    def generate_mask(self, props):
        mode = props.get("mode", "gausian")
        tresh = int(props.get('tresh', 100))
        type = props.get("type")

        img = self.edited[type] 
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        self.edited[type + "_gray"] = gray
        if mode == "gausian":
            self.mask=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 1023,5)
        if mode == "mean":
            self.mask=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 1023,5)
        elif mode == "tresh":
            ret, self.mask = cv2.threshold(gray, tresh, 1, 0)
        self.edited[type + "_mask"] = self.mask
        
    def find_conts(self, props):
        type = props.get("type")
        sep = props.get('sep', 0)
        if sep == "":
            sep = 0
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.conts=[]
        if sep:
            for contour in contours:
                if cv2.contourArea(contour) > float(sep):
                    self.conts.append(contour)
        else:
            self.conts = contours

        self.edited[type + "_cnts"] = cv2.drawContours(self.edited[type].copy(), self.conts, -1, (0,0, 255), 3, cv2.LINE_AA, hierarchy, 1 )
    
    def calc_area(self, props):
        real = props.get("real", {"x": 1, "y": 1, "z": 1})
        x, y, z = float(real["x"]), float(real["y"]), float(real["z"])
        areas = []
        lenghts = []
        for contour in self.conts:
            areas.append(cv2.contourArea(contour))
            lenghts.append(cv2.arcLength(contour, True))
        ks = (x*y)/(self.px*self.py)
        kl = x/self.px
        real_areas = np.array(areas) * ks
        real_lenghts = np.array(lenghts) * kl
        real_volum = sum(real_areas) + sum(real_lenghts) * z
        self.result = {
            "areas_top": list(real_areas),
            "length_top": list(real_lenghts), 
            "all_area": real_volum,
            #"gray": list(self.edited[props['type'] + "_gray"])
        }
        
        


    
    