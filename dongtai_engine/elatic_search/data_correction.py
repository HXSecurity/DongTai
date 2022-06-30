from dongtai_common.models.vulnerablity import IastVulnerabilityModel, IastVulnerabilityDocument


def data_correction(project_id):
    qs = IastVulnerabilityModel.objects.filter(
        agent__bind_project_id=project_id).all()
    IastVulnerabilityDocument().update(list(qs))
