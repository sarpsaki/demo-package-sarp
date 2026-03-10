from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackageSarp.src.models.PackageModel import (PackageModel, OutputImage, OutputLog, ConfigExecutor,
PackageConfigs, CensorExecutor, CensorOutputs, CensorResponse, MixOutputs, MixResponse, MixExecutor)

def build_response_censor(context):
    outputImage = OutputImage(value=context.outputImage)
    Outputs = CensorOutputs(outputImage=outputImage)
    packageResponse = CensorResponse(outputs=Outputs)
    packageExecutor = CensorExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel

def build_response_mix(context):
    outputImage = OutputImage(value=context.outputImage)
    outputLog = OutputLog(value=context.processingLog)
    Outputs = MixOutputs(outputImage=outputImage, outputLog=outputLog)
    packageResponse = MixResponse(outputs=Outputs)
    packageExecutor = MixExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel