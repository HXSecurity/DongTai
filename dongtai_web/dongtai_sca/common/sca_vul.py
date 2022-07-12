from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_vul import IastAssetVulTypeRelation
from dongtai_web.dongtai_sca.models import VulCveRelation


# 通过asset_vul获取 组件详情信息
def GetScaVulData(asset_vul, asset_queryset):
    data = {'base_info': dict(), 'poc_info': dict()}
    vul_id = asset_vul.id

    data['base_info'] = {'package_name': asset_vul.aql, 'version': asset_vul.package_version,
                         'safe_version': asset_vul.package_safe_version, 'language': asset_vul.package_language}

    data['base_info']['first_time'] = asset_vul.vul_publish_time
    data['base_info']['last_time'] = asset_vul.vul_update_time

    data['base_info']['cwe'] = ''
    data['base_info']['cnvd'] = ''
    data['base_info']['cve'] = ''
    data['base_info']['cnnvd'] = ''
    data['base_info']['level_id'] = asset_vul.level.id
    data['base_info']['level'] = asset_vul.level.name_value
    vul_cve_nums = asset_vul.vul_cve_nums
    if vul_cve_nums:
        data['base_info']['cwe'] = vul_cve_nums['cwe'] if vul_cve_nums['cwe'] else ''
        data['base_info']['cnvd'] = vul_cve_nums['cnvd'] if vul_cve_nums['cnvd'] else ''
        data['base_info']['cve'] = vul_cve_nums['cve'] if vul_cve_nums['cve'] else ''
        data['base_info']['cnnvd'] = vul_cve_nums['cnnvd'] if vul_cve_nums['cnnvd'] else ''

    data['base_info']['vul_title'] = asset_vul.vul_name
    data['base_info']['vul_detail'] = asset_vul.vul_detail
    data['base_info']['vul_cve_id'] = asset_vul.cve_code
    data['base_info']['have_article'] = asset_vul.have_article
    data['base_info']['have_poc'] = asset_vul.have_poc
    data['base_info']['vul_type'] = ''
    data['base_info']['vul_id'] = vul_id
    vul_type_relation = IastAssetVulTypeRelation.objects.filter(asset_vul_id=asset_vul.id)
    if vul_type_relation:
        vul_types = [_i.asset_vul_type.name for _i in vul_type_relation]
        data['base_info']['vul_type'] = ','.join(vul_types)

    asset_queryset = asset_queryset.filter(
        signature_value=asset_vul.package_hash, version=asset_vul.package_version, project_id__gt=0
    ).values('project_id', 'id').all()
    if asset_queryset:
        #_temp_data = {_a['project_id']: _a['id'] for _a in asset_queryset}
        #asset_ids = [_temp_data[p_id] for p_id in _temp_data]

        project_list = []
        projects_data = Asset.objects.filter(
            signature_value=asset_vul.package_hash,
            version=asset_vul.package_version,
            project_id__gt=0).values('project_name').all()
        for project in projects_data:
            project_list.append(project['project_name'])

        data['base_info']['project_names'] = project_list

    cve_relation = VulCveRelation.objects.filter(id=asset_vul.cve_id).first()

    if cve_relation:
        data['poc_info']['poc_list'] = cve_relation.poc if cve_relation.poc else []

        data['poc_info']['reference_link'] = []
        if cve_relation.references:
            for lk in cve_relation.references:
                if lk['type'] == 'in':
                    data['poc_info']['reference_link'].append({'url': lk['content'], 'source': lk['source']})
    return data
