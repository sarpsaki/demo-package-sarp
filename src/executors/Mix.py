import sys
import os
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackageSarp.src.utils.response import build_response_mix
from components.DemoPackageSarp.src.models.PackageModel import PackageModel

class Mix(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)
        self.img1_data = self.request.get_param("inputImageOne")
        self.img2_data = self.request.get_param("inputImageTwo")
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    def run(self):
        method = self.request.get_param("configMixMethods")
        intensity = self.request.get_param("NormalBlendRatio") or self.request.get_param("HardBlendRatio")
        apply_invert = self.request.get_param("NormalInvertToggle") or self.request.get_param("HardInvertToggle")

        blend_ratio = (int(intensity) if intensity else 50) / 100.0
        
        if method == "HARD":
            blend_ratio = min(blend_ratio * 1.5, 1.0)

        img1 = Image.get_frame(img=self.img1_data, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.img2_data, redis_db=self.redis_db)
        
        h, w = img1.value.shape[:2]
        img2_res = cv2.resize(img2.value, (w, h))
        
        if apply_invert:
            img2_res = cv2.bitwise_not(img2_res)
        
        img1.value = cv2.addWeighted(img1.value, 1 - blend_ratio, img2_res, blend_ratio, 0)
        
        self.outputImage = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.processingLog = f"Mod: {method}, Ratio: {blend_ratio}, Invert: {apply_invert}"
        
        return build_response_mix(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()