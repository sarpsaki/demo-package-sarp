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
        self.imagesOne = self.request.get_param("inputImageOne")
        self.imagesTwo = self.request.get_param("inputImageTwo")
        self.mixMethods = self.request.get_param("configMixMethods")
        self.intensity = self.request.get_param("NormalBlendRatio") or self.request.get_param("HardBlendRatio")
        self.invertToggle = self.request.get_param("NormalInvertToggle") or self.request.get_param("HardInvertToggle")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_image(self, image_array_1: np.ndarray, image_array_2: np.ndarray):

        if image_array_1.dtype != np.uint8: image_array_1 = image_array_1.astype(np.uint8)
        if image_array_2.dtype != np.uint8: image_array_2 = image_array_2.astype(np.uint8)

        blend_ratio = (int(self.intensity) if self.intensity else 50) / 100.0
        
        if self.mixMethods == "HARD":
            blend_ratio = min(blend_ratio * 1.5, 1.0)

        h, w = image_array_1.shape[:2]
        image_array_2_res = cv2.resize(image_array_2, (w, h))

        if self.invertToggle:
            image_array_2_res = cv2.bitwise_not(image_array_2_res)

        processed_image = cv2.addWeighted(image_array_1, 1 - blend_ratio, image_array_2_res, blend_ratio, 0)
        log_text = f"Mod: {self.mixMethods}, Ratio: {blend_ratio}, Invert: {bool(self.invertToggle)}"
        
        return processed_image, log_text

    def run(self):
        image_obj_1 = Image.get_frame(img=self.imagesOne, redis_db=self.redis_db)
        image_obj_2 = Image.get_frame(img=self.imagesTwo, redis_db=self.redis_db)
        
        processed_array, process_log = self.process_image(np.array(image_obj_1.value), np.array(image_obj_2.value))
        image_obj_1.value = processed_array
        
        self.outputImage = Image.set_frame(img=image_obj_1, package_uID=self.uID, redis_db=self.redis_db)
        self.processingLog = process_log
        
        return build_response_mix(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()