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
        self.images = self.request.get_param("inputImage")
        self.censorMethods = self.request.get_param("configCensorMethods")
        self.intensity = self.request.get_param("GaussianIntensity") or self.request.get_param("MedianIntensity")
        self.grayToggle = self.request.get_param("GaussianGrayToggle") or self.request.get_param("MedianGrayToggle")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_image(self, image_array: np.ndarray):

        if image_array.dtype != np.uint8: image_array = image_array.astype(np.uint8)
        
        intensity = int(self.intensity) if self.intensity else 15
        k_size = intensity if intensity % 2 != 0 else intensity + 1
        
        if self.grayToggle:
            image_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            image_array = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
            
        if self.censorMethods == "GAUSSIAN":
            processed_image = cv2.GaussianBlur(image_array, (k_size, k_size), 0)
        elif self.censorMethods == "MEDIAN":
            processed_image = cv2.medianBlur(image_array, k_size)
        else:
            processed_image = image_array

        return processed_image

    def run(self):
        image_obj = Image.get_frame(img=self.images, redis_db=self.redis_db)
        image_obj.value = self.process_image(np.array(image_obj.value))
        
        self.outputImage = Image.set_frame(img=image_obj, package_uID=self.uID, redis_db=self.redis_db)
        return build_response_censor(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()