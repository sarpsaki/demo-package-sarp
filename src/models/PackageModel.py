from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Processed Image"


class OutputLog(Output):
    name: Literal["outputLog"] = "outputLog"
    value: str = ""
    type: Literal["string"] = "string"

    class Config:
        title = "Status Log"


class IntensityValue(Config):
    name: Literal["intensityValue"] = "intensityValue"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Intensity / Size"


class GrayscaleToggle(Config):
    name: Literal["grayscaleToggle"] = "grayscaleToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"

    class Config:
        title = "Apply Grayscale"


class InvertToggle(Config):
    name: Literal["invertToggle"] = "invertToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"

    class Config:
        title = "Invert Image"


class OptionGaussian(Config):
    name: Literal["optionGaussian"] = "optionGaussian"
    IntensityValue: IntensityValue   
    GrayscaleToggle: GrayscaleToggle 
    value: Literal["GAUSSIAN"] = "GAUSSIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian Blur"


class OptionMedian(Config):
    name: Literal["optionMedian"] = "optionMedian"
    IntensityValue: IntensityValue   
    GrayscaleToggle: GrayscaleToggle 
    value: Literal["MEDIAN"] = "MEDIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Median Blur"


class ConfigCensorMethods(Config):
    """
    Select specific blur methods to apply to the image.
    Includes options for intensity and grayscale toggling.
    """
    name: Literal["configCensorMethods"] = "configCensorMethods"
    value: Union[OptionGaussian, OptionMedian]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Blur Methods"


class CensorConfigs(Configs):
    configCensorMethods: ConfigCensorMethods


class CensorInputs(Inputs):
    inputImage: InputImage 


class CensorOutputs(Outputs):
    outputImage: OutputImage 


class CensorRequest(Request):
    inputs: Optional[CensorInputs]
    configs: CensorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class CensorResponse(Response):
    outputs: CensorOutputs


class CensorExecutor(Config):
    name: Literal["Censor"] = "Censor"
    value: Union[CensorRequest, CensorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Image Censor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class OptionNormalBlend(Config):
    name: Literal["optionNormalBlend"] = "optionNormalBlend"
    IntensityValue: IntensityValue 
    InvertToggle: InvertToggle     
    value: Literal["NORMAL"] = "NORMAL"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Normal Blend (50%)"


class OptionHardBlend(Config):
    name: Literal["optionHardBlend"] = "optionHardBlend"
    IntensityValue: IntensityValue 
    InvertToggle: InvertToggle     
    value: Literal["HARD"] = "HARD"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Hard Blend (70%)"


class ConfigMixMethods(Config):
    """
    Select specific blending methods to mix two images.
    Includes options for blend ratio and inverting the second image.
    """
    name: Literal["configMixMethods"] = "configMixMethods"
    value: Union[OptionNormalBlend, OptionHardBlend]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Mix Methods"


class MixConfigs(Configs):
    configMixMethods: ConfigMixMethods


class MixInputs(Inputs):
    inputImageOne: InputImage 
    inputImageTwo: InputImage 


class MixOutputs(Outputs):
    outputImage: OutputImage  
    outputLog: OutputLog      


class MixRequest(Request):
    inputs: Optional[MixInputs]
    configs: MixConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class MixResponse(Response):
    outputs: MixOutputs


class MixExecutor(Config):
    name: Literal["Mix"] = "Mix"
    value: Union[MixRequest, MixResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Image Mixer"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    """
    Selects the underlying engine for image processing.
    Censor handles single image blurring, while Mix blends two images together.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CensorExecutor, MixExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task Type"
        json_schema_extra = {
            "shortDescription": "Image Processing Engine"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"
    uID: str = "1234567"