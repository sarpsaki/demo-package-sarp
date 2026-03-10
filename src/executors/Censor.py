import sys
import os
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackageSarp.src.utils.response import build_response_censor
from components.DemoPackageSarp.src.models.PackageModel import PackageModel

class Censor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.image_one_data = self.request.get_param("inputImageOne")
        
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        censor_menu = self.request.get_param("CensorMenu")
        self.blur_method = censor_menu.get("name") if censor_menu else "CensorMethod1"
        
        if self.blur_method == "CensorMethod1":
            intensity = self.request.get_param("GaussianIntensity")
        else:
            intensity = self.request.get_param("MedianIntensity")
            
        intensity = int(intensity) if intensity else 15
        k_size = intensity if intensity % 2 != 0 else intensity + 1
        
        img_obj = Image.get_frame(img=self.image_one_data, redis_db=self.redis_db)
        
        if self.blur_method == "CensorMethod2":
            img_obj.value = cv2.medianBlur(img_obj.value, k_size)
        else:
            img_obj.value = cv2.GaussianBlur(img_obj.value, (k_size, k_size), 0)
        
        self.outputImage = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)
        
        return build_response_censor(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()