from pydantic import Field
from typing import Literal
from sdks.novavision.src.base.model import Package, Configs, Config

# Ekranda görünecek test alanımız
class TestMetni(Config):
    name: Literal["TestMetni"] = "TestMetni"
    value: str = Field(default="Merhaba NovaVision!")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Sarp'ın Bağlantı Testi" # Sağ menüde bu yazıyı arayacağız!

class PackageConfigsMain(Configs):
    test_metni: TestMetni

class PackageModel(Package):
    configs: PackageConfigsMain
    type: Literal["component"] = "component"
    name: Literal["DemoPackageSarp"] = "DemoPackageSarp"