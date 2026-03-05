from __future__ import annotations
from pydantic import Field, validator
from typing import Optional, Union, Literal, List
from sdks.novavision.src.base.model import (
    Package, Configs, Config, Request, Response, 
    Image, Input, Output, Inputs, Outputs
)

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Görüntü Girdisi"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Görüntü Çıktısı"

class OutputLog(Output):
    name: Literal["outputLog"] = "outputLog"
    value: str = ""
    type: Literal["string"] = "string"
    class Config: title = "İşlem Günlüğü"

class OptionA(Config):
    val1: int = Field(default=15, title="Sayı Girişi")
    val2: Literal["Seçenek 1", "Seçenek 2"] = "Seçenek 1"
    name: Literal["OptionA"] = "OptionA"
    value: Literal["Yöntem 1"] = "Yöntem 1"
    field: Literal["option"] = "option"

class OptionB(Config):
    val1: int = Field(default=30, title="Genişlik")
    val2: Literal["Hızlı", "Yavaş"] = "Hızlı"
    name: Literal["OptionB"] = "OptionB"
    value: Literal["Yöntem 2"] = "Yöntem 2"
    field: Literal["option"] = "option"

class MyDependentMenu(Config):
    name: Literal["MyDependentMenu"] = "MyDependentMenu"
    value: Union[OptionA, OptionB]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Alt Ayarlar"

class CensorExecutorInputs(Inputs):
    inputImage: InputImage

class CensorExecutorOutputs(Outputs):
    outputImage: OutputImage

class MixExecutorInputs(Inputs):
    inputImageOne: InputImage
    inputImageTwo: InputImage

class MixExecutorOutputs(Outputs):
    outputImage: OutputImage
    processingLog: OutputLog

class CensorExecutorConfigs(Configs):
    menu: MyDependentMenu

class CensorExecutorRequest(Request):
    inputs: Optional[CensorExecutorInputs]
    configs: CensorExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class CensorExecutorResponse(Response):
    outputs: CensorExecutorOutputs

class MixExecutorConfigs(Configs):
    menu: MyDependentMenu

class MixExecutorRequest(Request):
    inputs: Optional[MixExecutorInputs]
    configs: MixExecutorConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class MixExecutorResponse(Response):
    outputs: MixExecutorOutputs

class CensorExecutor(Config):
    name: Literal["CensorExecutor"] = "CensorExecutor"
    value: Union[CensorExecutorRequest, CensorExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Görüntü Sansürleyici"
        json_schema_extra = {"target": {"value": 0}}

class MixExecutor(Config):
    name: Literal["MixExecutor"] = "MixExecutor"
    value: Union[MixExecutorRequest, MixExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Görüntü Karıştırıcı"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[CensorExecutor, MixExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "İşlem Türü"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"