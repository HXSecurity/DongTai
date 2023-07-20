from django.core.management.base import BaseCommand
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.asset_vul import IastAssetVul


class Command(BaseCommand):
    help = "scripts to deal with old data to new version"
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        agent_count = IastAgent.objects.all().count()
        online_agent_count = IastAgent.objects.filter(online=1).count()
        total_method_pool_count = MethodPool.objects.all().count()
        total_vulnerability = IastVulnerabilityModel.objects.all().count()
        total_high_vulnerability = IastVulnerabilityModel.objects.filter(
            level_id=1
        ).count()
        total_medium_vulnerability = IastVulnerabilityModel.objects.filter(
            level_id=2
        ).count()
        total_low_vulnerability = IastVulnerabilityModel.objects.filter(
            level_id=3
        ).count()
        total_info_vulnerability = IastVulnerabilityModel.objects.filter(
            level_id=4
        ).count()
        total_note_vulnerability = IastVulnerabilityModel.objects.filter(
            level_id=5
        ).count()
        total_high_asset_vulnerability = IastAssetVul.objects.filter(level_id=1).count()
        total_medium_asset_vulnerability = IastAssetVul.objects.filter(
            level_id=2
        ).count()
        total_low_asset_vulnerability = IastAssetVul.objects.filter(level_id=3).count()
        total_info_asset_vulnerability = IastAssetVul.objects.filter(level_id=4).count()
        total_note_asset_vulnerability = IastAssetVul.objects.filter(level_id=5).count()

        self.stdout.write(
            f"""
        =============================================
        agent_count={agent_count}
        online_agent_count={online_agent_count}
        total_method_pool_count={total_method_pool_count}
        total_vulnerability={total_vulnerability}
        total_high_vulnerability={total_high_vulnerability}
        total_medium_vulnerability={total_medium_vulnerability}
        total_low_vulnerability={total_low_vulnerability}
        total_info_vulnerability={total_info_vulnerability}
        total_note_vulnerability={total_note_vulnerability}
        total_high_asset_vulnerability={total_high_asset_vulnerability}
        total_medium_asset_vulnerability={total_medium_asset_vulnerability}
        total_low_asset_vulnerability={total_low_asset_vulnerability}
        total_info_asset_vulnerability={total_info_asset_vulnerability}
        total_note_asset_vulnerability={total_note_asset_vulnerability}
        ==============================================
        """
        )
