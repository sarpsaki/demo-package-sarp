from sdks.novavision.src.helper.package import PackageHelper

from components.DemoPackageSarp.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    CensorExecutor, CensorExecutorResponse, CensorExecutorOutputs,
    MixExecutor, MixExecutorResponse, MixExecutorOutputs,
    OutputImage, OutputLog
)

def build_response(context):
    if context.executor_type == "CensorExecutor":
        output_image = OutputImage(value=context.outputImage)
        outputs = CensorExecutorOutputs(outputImage=output_image)
        response = CensorExecutorResponse(outputs=outputs)
        executor_node = CensorExecutor(value=response)
        
    elif context.executor_type == "MixExecutor":
        output_image = OutputImage(value=context.outputImage)
        output_log = OutputLog(value=context.processingLog)
        outputs = MixExecutorOutputs(outputImage=output_image, outputLog=output_log)
        response = MixExecutorResponse(outputs=outputs)
        executor_node = MixExecutor(value=response)
        
    else:
        raise ValueError("Bilinmeyen Executor Türü!")

    config_executor = ConfigExecutor(value=executor_node)
    package_configs = PackageConfigs(executor=config_executor)
    
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model_result = package.build_model(context)
    
    return package_model_result