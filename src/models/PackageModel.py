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

class OptionGaussian(Config):
    name: Literal["optionGaussian"] = "optionGaussian"
    value: Literal["GAUSSIAN"] = "GAUSSIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionMedian(Config):
    name: Literal["optionMedian"] = "optionMedian"
    value: Literal["MEDIAN"] = "MEDIAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Median Blur"

class ConfigCensorMethods(Config):
    name: Literal["configCensorMethods"] = "configCensorMethods"
    value: List[Union[OptionGaussian, OptionMedian]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"
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
        json_schema_extra = {"target": "configs"}

class CensorResponse(Response):
    outputs: CensorOutputs

class CensorExecutor(Config):
    name: Literal["Censor"] = "Censor"
    value: Union[CensorRequest, CensorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Censor"
        json_schema_extra = {"target": {"value": 0}}



class OutputLog(Output):
    name: Literal["outputLog"] = "outputLog"
    value: str = ""
    type: Literal["string"] = "string"
    class Config: title = "Status Log"

class OptionNormalBlend(Config):
    name: Literal["optionNormalBlend"] = "optionNormalBlend"
    value: Literal["NORMAL"] = "NORMAL"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Normal Blend (50%)"

class OptionHardBlend(Config):
    name: Literal["optionHardBlend"] = "optionHardBlend"
    value: Literal["HARD"] = "HARD"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Hard Blend (70%)"

class ConfigMixMethods(Config):
    name: Literal["configMixMethods"] = "configMixMethods"
    value: List[Union[OptionNormalBlend, OptionHardBlend]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"
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
        json_schema_extra = {"target": "configs"}

class MixResponse(Response):
    outputs: MixOutputs

class MixExecutor(Config):
    name: Literal["Mix"] = "Mix"
    value: Union[MixRequest, MixResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Mix"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CensorExecutor, MixExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task Type"
        json_schema_extra = {
            "shortDescription": "Select the engine."
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"
    uID: str = "1234567"