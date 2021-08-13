######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : translation
# @created     : Friday Aug 13, 2021 14:31:38 CST
#
# @description :
######################################################################


from modeltranslation.translator import translator, TranslationOptions, register
from models.strategy import IastStrategyModel
from models.vul_level import IastVulLevel
from models.vulnerablity import IastVulnerabilityModel
from models.deploy import IastDeployDesc
from models.document import IastDocument
from models.hook_type import HookType


@register(IastStrategyModel)
class IastStrategyModelTranslationOptions(TranslationOptions):
    fields = ('vul_name', 'vul_desc', 'vul_fix')


@register(IastVulLevel)
class IastVulLevelTranslationOptions(TranslationOptions):
    fields = ('name_value', 'name_type')


@register(IastVulnerabilityModel)
class IastVulnerabilityModelTranslationOptions(TranslationOptions):
    fields = ('type')


@register(IastDeployDesc)
class IastDeployDescTranslationOptions(TranslationOptions):
    fields = ('desc')


@register(IastDocument)
class IastDocumentTranslationOptions(TranslationOptions):
    fields = ('title')


@register(IastDocument)
class IastDocumentTranslationOptions(TranslationOptions):
    fields = ('title')


@register(HookType)
class HookTypeTranslationOptions(TranslationOptions):
    fields = ('name')
