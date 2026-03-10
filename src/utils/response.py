from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackageSarp.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    CensorExecutor, CensorResponse, CensorOutputs,
    MixExecutor, MixResponse, MixOutputs,
    OutputImage, OutputLog
)

def build_response_censor(context):
    output_image = OutputImage(value=context.outputImage)
    outputs = CensorOutputs(outputImage=output_image)
    package_response = CensorResponse(outputs=outputs)
    package_executor = CensorExecutor(value=package_response)
    
    executor = ConfigExecutor(value=package_executor)
    package_configs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)

def build_response_mix(context):
    output_image = OutputImage(value=context.outputImage)
    output_log = OutputLog(value=context.processingLog)
    outputs = MixOutputs(outputImage=output_image, outputLog=output_log)
    package_response = MixResponse(outputs=outputs)
    package_executor = MixExecutor(value=package_response)
    
    executor = ConfigExecutor(value=package_executor)
    package_configs = PackageConfigs(executor=executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)