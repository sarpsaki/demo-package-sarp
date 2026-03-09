from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, Union, Literal, List
from sdks.novavision.src.base.model import (
    Package, Configs, Config, Request, Response, 
    Image, Input, Output, Inputs, Outputs
)

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Image 1"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Image 2"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Output Image"

class OutputLog(Output):
    name: Literal["outputLog"] = "outputLog"
    value: str = ""
    type: Literal["string"] = "string"
    class Config: title = "Processing Log"

class GaussianIntensity(Config):
    name: Literal["GaussianIntensity"] = "GaussianIntensity"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Intensity"

class MedianIntensity(Config):
    name: Literal["MedianIntensity"] = "MedianIntensity"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Intensity"

class Blend50Size(Config):
    name: Literal["Blend50Size"] = "Blend50Size"
    value: int = Field(default=30)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Size"

class Blend70Size(Config):
    name: Literal["Blend70Size"] = "Blend70Size"
    value: int = Field(default=30)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Size"

class CensorMethod1(Config):
    name: Literal["CensorMethod1"] = "CensorMethod1"
    GaussianIntensity: GaussianIntensity
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class CensorMethod2(Config):
    name: Literal["CensorMethod2"] = "CensorMethod2"
    MedianIntensity: MedianIntensity
    value: Literal["Median"] = "Median"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Median Blur"

class MixMethod1(Config):
    name: Literal["MixMethod1"] = "MixMethod1"
    Blend50Size: Blend50Size
    value: Literal["Blend50"] = "Blend50"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Normal Blend (50%)"

class MixMethod2(Config):
    name: Literal["MixMethod2"] = "MixMethod2"
    Blend70Size: Blend70Size
    value: Literal["Blend70"] = "Blend70"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Hard Blend (70%)"

class CensorMenu(Config):
    name: Literal["CensorMenu"] = "CensorMenu"
    value: Union[CensorMethod1, CensorMethod2]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Blur Settings"
        json_schema_extra = {"target": "value"}

class MixMenu(Config):
    name: Literal["MixMenu"] = "MixMenu"
    value: Union[MixMethod1, MixMethod2]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: 
        title = "Mix Settings"
        json_schema_extra = {"target": "value"}

class CensorExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    value: str = ""
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class MixExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo
    value: str = ""
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class CensorExecutorOutputs(Outputs):
    outputImage: OutputImage
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class MixExecutorOutputs(Outputs):
    outputImage: OutputImage
    outputLog: OutputLog
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class CensorExecutorConfigs(Configs):
    CensorMenu: CensorMenu
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class CensorExecutorRequest(Request):
    inputs: Optional[CensorExecutorInputs]
    configs: CensorExecutorConfigs
    class Config: json_schema_extra = {"target": "configs"}

class CensorExecutorResponse(Response):
    outputs: CensorExecutorOutputs

class MixExecutorConfigs(Configs):
    MixMenu: MixMenu
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class MixExecutorRequest(Request):
    inputs: Optional[MixExecutorInputs]
    configs: MixExecutorConfigs
    class Config: json_schema_extra = {"target": "configs"}

class MixExecutorResponse(Response):
    outputs: MixExecutorOutputs

class CensorExecutor(Config):
    name: Literal["CensorExecutor"] = "CensorExecutor"
    value: Union[CensorExecutorRequest, CensorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Censor"
        json_schema_extra = {"target": {"value": 0}}

class MixExecutor(Config):
    name: Literal["MixExecutor"] = "MixExecutor"
    value: Union[MixExecutorRequest, MixExecutorResponse]
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
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"
    uID: str = "1234567"