######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : systemsettings
# @created     : 星期二 11月 30, 2021 19:54:50 CST
#
# @description :
######################################################################


from dongtai_common.models.profile import IastProfile


def get_vul_validate():
    vul_verifiy = IastProfile.objects.filter(key="vul_verifiy").values_list("value", flat=True).first()
    return bool(not vul_verifiy or vul_verifiy == "1")


def get_circuit_break():
    circuit_break = IastProfile.objects.filter(key="circuit_break").values_list("value", flat=True).first()
    return bool(not circuit_break or circuit_break == "1")
