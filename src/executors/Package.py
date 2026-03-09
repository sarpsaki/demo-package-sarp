import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackageSarp.src.utils.response import build_response
from components.DemoPackageSarp.src.models.PackageModel import PackageModel

class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.executor_type = self.request.model.configs.executor.value.name
        
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_censor(self):
        self.image_one_data = self.request.get_param("inputImageOne")
        censor_menu = self.request.get_param("CensorMenu")
        self.blur_method = censor_menu.get("name") if censor_menu else "CensorMethod1"
        
        if self.blur_method == "CensorMethod1":
            intensity = self.request.get_param("GaussianIntensity")
        else:
            intensity = self.request.get_param("MedianIntensity")
            
        intensity = int(intensity) if intensity else 15
        k_size = intensity if intensity % 2 != 0 else intensity + 1
        
        img1 = Image.get_frame(img=self.image_one_data, redis_db=self.redis_db)
        if self.blur_method == "CensorMethod2":
            img1.value = cv2.medianBlur(img1.value, k_size)
        else:
            img1.value = cv2.GaussianBlur(img1.value, (k_size, k_size), 0)
        
        self.outputImage = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

    def process_mix(self):
        self.image_one_data = self.request.get_param("inputImageOne")
        self.image_two_data = self.request.get_param("inputImageTwo")
        mix_menu = self.request.get_param("MixMenu")
        self.mix_method = mix_menu.get("name") if mix_menu else "MixMethod1"
        
        if self.mix_method == "MixMethod1":
            self.mix_size = self.request.get_param("Blend50Size")
        else:
            self.mix_size = self.request.get_param("Blend70Size")

        img1 = Image.get_frame(img=self.image_one_data, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two_data, redis_db=self.redis_db)
        
        height, width = img1.value.shape[:2]
        img2_resized = cv2.resize(img2.value, (width, height))
        
        alpha = 0.7 if self.mix_method == "MixMethod2" else 0.5
        mixed_val = cv2.addWeighted(img1.value, 1-alpha, img2_resized, alpha, 0)
        
        img1.value = mixed_val
        self.outputImage = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.processingLog = f"Mod: {self.mix_method}, Boyut: {self.mix_size}"

    def run(self):
        if self.executor_type == "CensorExecutor":
            self.process_censor()
        elif self.executor_type == "MixExecutor":
            self.process_mix()
            
        packageModel = build_response(context=self)
        return packageModel

if "__main__" == __name__:
    Executor(sys.argv[1]).run()