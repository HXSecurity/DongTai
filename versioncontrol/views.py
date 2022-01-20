from django.shortcuts import render
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint

# Create your views here.


class VersionListView(UserEndPoint):
    def get(self, request):
        data = {
            "DongTai": {
                "version": "1.3.0"
            },
            "DongTai-agent-java": {
                "version":
                "1.3.0",
                "commit_hash":
                "67d6474b0c7a6406c0e47492594f4f7445345a24",
                "iast-core.jar":
                "1637b41d6113265ff6eb1a09a7e65bc01ce62ebcd5b85c1ef1840ca7a30d19b6"
            },
            "DongTai-agent-python": {
                "version": "1.3.0",
                "commit_hash": "a98d09263180cb7f8a2d441892e7d24c6b7e8933"
            },
            "DongTai-engine": {
                "version": "1.3.0",
                "commit_hash": "a1f88d215667df26154fb762b1eefcec85ccbdb5"
            },
            "DongTai-openapi": {
                "version": "1.3.0",
                "commit_hash": "e787809c741b7ed1595a53f0e7d4c6cf7f1f1438"
            },
            "DongTai-webapi": {
                "version": "1.3.0",
                "commit_hash": "328057d82f0aa4899573d19d525222a6efc9b701"
            }
        }
        return R.success(data=data)
