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

class BlurIntensityParam(Config):
    name: Literal["BlurIntensityParam"] = "BlurIntensityParam"
    value: int = Field(default=15)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Intensity"

class BlurTypeParam(Config):
    name: Literal["BlurTypeParam"] = "BlurTypeParam"
    value: Literal["Type 1", "Type 2"] = "Type 1"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Type"

class OptionA(Config):
    name: Literal["OptionA"] = "OptionA"
    param1: BlurIntensityParam
    param2: BlurTypeParam
    value: Literal["Method 1"] = "Method 1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Method 1"

class SizeParam(Config):
    name: Literal["SizeParam"] = "SizeParam"
    value: int = Field(default=30)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Size"

class SpeedParam(Config):
    name: Literal["SpeedParam"] = "SpeedParam"
    value: Literal["Fast", "Slow"] = "Fast"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Speed"

class OptionB(Config):
    name: Literal["OptionB"] = "OptionB"
    param1: SizeParam
    param2: SpeedParam
    value: Literal["Method 2"] = "Method 2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Method 2"

class MyDependentMenu(Config):
    name: Literal["MyDependentMenu"] = "MyDependentMenu"
    value: Union[OptionA, OptionB]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Sub Settings"

# --- EKSİKLERİN GİDERİLDİĞİ KISIM (Inputs) ---
class CensorExecutorInputs(Inputs):
    inputImage: InputImageOne
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
    processingLog: OutputLog
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


class CensorExecutorConfigs(Configs):
    menu: MyDependentMenu
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
    menu: MyDependentMenu
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
    class Config: title = "Task Type"

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