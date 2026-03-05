from pydantic import Field
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Configs, Config, Request, Response

# 1. En Basit Ayar Bileşeni
class TestAyari(Config):
    name: Literal["TestAyari"] = "TestAyari"
    value: int = Field(default=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Sarp Test Degeri"

# 2. Zorunlu Hiyerarşi Katmanları
class PackageConfigs(Configs):
    test_ayar: TestAyari

class PackageRequest(Request):
    configs: PackageConfigs
    class Config: json_schema_extra = {"target": "configs"}

class PackageExecutor(Config):
    name: Literal["Package"] = "Package"
    value: Union[PackageRequest, Response]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: 
        title = "Görüntü İşleyici"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçimi"

class MainConfigs(Configs):
    executor: ConfigExecutor

# 3. Ana Model (İsim düzeltildi)
class PackageModel(Package):
    configs: MainConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"