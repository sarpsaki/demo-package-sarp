from __future__ import annotations
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response, 
    Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Processed Image"

class OutputLog(Output):
    name: Literal["outputLog"] = "outputLog"
    value: str = ""
    type: Literal["string"] = "string"
    class Config: title = "Status Log"


class GaussianIntensity(Config):
    name: Literal["GaussianIntensity"] = "GaussianIntensity"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Intensity"

class GaussianGrayToggle(Config):
    name: Literal["GaussianGrayToggle"] = "GaussianGrayToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Apply Grayscale"

class MedianIntensity(Config):
    name: Literal["MedianIntensity"] = "MedianIntensity"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Intensity"

class MedianGrayToggle(Config):
    name: Literal["MedianGrayToggle"] = "MedianGrayToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Apply Grayscale"

class OptionGaussian(Config):
    name: Literal["optionGaussian"] = "optionGaussian"
    GaussianIntensity: GaussianIntensity 
    GaussianGrayToggle: GaussianGrayToggle 
    value: Literal["GAUSSIAN"] = "GAUSSIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionMedian(Config):
    name: Literal["optionMedian"] = "optionMedian"
    MedianIntensity: MedianIntensity 
    MedianGrayToggle: MedianGrayToggle 
    value: Literal["MEDIAN"] = "MEDIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Median Blur"

class ConfigCensorMethods(Config):
    name: Literal["configCensorMethods"] = "configCensorMethods"
    value: Union[OptionGaussian, OptionMedian]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Blur Methods"
        json_schema_extra = {"target": "value"}

class CensorConfigs(Configs):
    configCensorMethods: ConfigCensorMethods

class CensorInputs(Inputs):
    inputImage: InputImage

class CensorOutputs(Outputs):
    outputImage: OutputImage

class CensorRequest(Request):
    inputs: Optional[CensorInputs]
    configs: CensorConfigs
    class Config: json_schema_extra = {"target": "configs"}

class CensorResponse(Response):
    outputs: CensorOutputs

class CensorExecutor(Config):
    name: Literal["Censor"] = "Censor"
    value: Union[CensorRequest, CensorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Censor"
        json_schema_extra = {"target": {"value": 0}}


class NormalBlendRatio(Config):
    name: Literal["NormalBlendRatio"] = "NormalBlendRatio"
    value: int = Field(default=50)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Blend Ratio"

class NormalInvertToggle(Config):
    name: Literal["NormalInvertToggle"] = "NormalInvertToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Invert Image"

class HardBlendRatio(Config):
    name: Literal["HardBlendRatio"] = "HardBlendRatio"
    value: int = Field(default=70)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Blend Ratio"

class HardInvertToggle(Config):
    name: Literal["HardInvertToggle"] = "HardInvertToggle"
    value: bool = Field(default=False)
    type: Literal["boolean"] = "boolean"
    field: Literal["checkbox"] = "checkbox"
    class Config: title = "Invert Image"

class OptionNormalBlend(Config):
    name: Literal["optionNormalBlend"] = "optionNormalBlend"
    NormalBlendRatio: NormalBlendRatio
    NormalInvertToggle: NormalInvertToggle
    value: Literal["NORMAL"] = "NORMAL"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Normal Blend (50%)"

class OptionHardBlend(Config):
    name: Literal["optionHardBlend"] = "optionHardBlend"
    HardBlendRatio: HardBlendRatio
    HardInvertToggle: HardInvertToggle
    value: Literal["HARD"] = "HARD"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Hard Blend (70%)"

class ConfigMixMethods(Config):
    name: Literal["configMixMethods"] = "configMixMethods"
    value: Union[OptionNormalBlend, OptionHardBlend]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Mix Methods"
        json_schema_extra = {"target": "value"}

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
    class Config: json_schema_extra = {"target": "configs"}

class MixResponse(Response):
    outputs: MixOutputs

class MixExecutor(Config):
    name: Literal["Mix"] = "Mix"
    value: Union[MixRequest, MixResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Mixer"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CensorExecutor, MixExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task Type"
        json_schema_extra = {"target": "value"}

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"
    uID: str = "1234567"