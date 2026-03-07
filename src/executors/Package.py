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

class CensorExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.executor_type = self.request.model.configs.executor.value.name
        
        censor_menu = self.request.get_param("CensorMenu")
        self.blur_method = censor_menu.get("name") if censor_menu else "CensorMethod1"
        
        self.image_one_data = self.request.get_param("inputImageOne")
        self.blur_intensity = self.request.get_param("BlurIntensityParam")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_censor(self, img_value):
        intensity = int(self.blur_intensity) if self.blur_intensity else 15
        k_size = intensity if intensity % 2 != 0 else intensity + 1
        
        if self.blur_method == "CensorMethod2":
            return cv2.medianBlur(img_value, k_size)
        else:
            return cv2.GaussianBlur(img_value, (k_size, k_size), 0)

    def run(self):
        img1 = Image.get_frame(img=self.image_one_data, redis_db=self.redis_db)
        img1.value = self.process_censor(img1.value)
        self.outputImage = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        
        packageModel = build_response(context=self)
        return packageModel

class MixExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.executor_type = self.request.model.configs.executor.value.name
        
        mix_menu = self.request.get_param("MixMenu")
        self.mix_method = mix_menu.get("name") if mix_menu else "MixMethod1"
        
        self.image_one_data = self.request.get_param("inputImageOne")
        self.image_two_data = self.request.get_param("inputImageTwo")
        self.mix_size = self.request.get_param("MixSizeParam")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_mix(self, img1_value, img2_value):
        height, width = img1_value.shape[:2]
        img2_resized = cv2.resize(img2_value, (width, height))
        
        if self.mix_method == "MixMethod2":
            mixed_img = cv2.addWeighted(img1_value, 0.7, img2_resized, 0.3, 0)
        else:
            mixed_img = cv2.addWeighted(img1_value, 0.5, img2_resized, 0.5, 0)
        return mixed_img

    def run(self):
        img1 = Image.get_frame(img=self.image_one_data, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two_data, redis_db=self.redis_db)
        
        mixed_val = self.process_mix(img1.value, img2.value)
        img1.value = mixed_val
        
        self.outputImage = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.processingLog = f"Islem Basarili! Resimler {self.mix_method} moduyla ve {self.mix_size} boyutuyla birlestirildi."

        packageModel = build_response(context=self)
        return packageModel

if "__main__" == __name__:
    Executor(sys.argv[1]).run()