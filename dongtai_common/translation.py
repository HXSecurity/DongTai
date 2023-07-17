######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : translation
# @created     : Friday Aug 13, 2021 14:31:38 CST
#
# @description :
######################################################################


from modeltranslation.translator import translator, TranslationOptions, register
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
from dongtai_common.models.deploy import IastDeployDesc
from dongtai_common.models.document import IastDocument
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.department import Department
from dongtai_common.models.talent import Talent
from dongtai_common.models.engine_monitoring_indicators import IastEnginMonitoringIndicators


@register(IastStrategyModel)
class IastStrategyModelTranslationOptions(TranslationOptions):
    fields = ('vul_name', 'vul_desc', 'vul_fix')


@register(IastVulLevel)
class IastVulLevelTranslationOptions(TranslationOptions):
    fields = ('name_value', 'name_type')


@register(IastDeployDesc)
class IastDeployDescTranslationOptions(TranslationOptions):
    fields = ('desc', )


@register(IastDocument)
class IastDocumentTranslationOptions(TranslationOptions):
    fields = ('title', 'url')


@register(HookType)
class HookTypeTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(IastEnginMonitoringIndicators)
class IastEnginMonitoringIndicatorsOptions(TranslationOptions):
    fields = ('name', )


@register(IastVulnerabilityStatus)
class IastVulnerabilityStatusOptions(TranslationOptions):
    fields = ('name', )
