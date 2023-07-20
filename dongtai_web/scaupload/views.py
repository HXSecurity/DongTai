from django.shortcuts import render
from dongtai_common.endpoint import UserEndPoint
from django.db.models import Q
from dongtai_common.models.sca_maven_db import (
    ScaMavenDb,
    ImportFrom,
)
from rest_framework import serializers
from rest_framework import generics
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _
from dongtai_common.permissions import TalentAdminPermission
from dongtai_common.endpoint import R
import csv
from django.http import FileResponse
from dongtai_conf.settings import BASE_DIR
import os
from dongtai_web.scaupload.utils import (
    get_packge_from_sca_lib,
    ScaLibError,
)
from django.db.utils import IntegrityError


# Create your views here.


class ScaDBSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))


class ScaMavenDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScaMavenDb
        fields = "__all__"


class ScaMavenDbUploadSerializer(serializers.Serializer):
    group_id = serializers.CharField()
    atrifact_id = serializers.CharField()
    version = serializers.CharField()
    sha_1 = serializers.CharField()
    package_name = serializers.CharField()
    license = serializers.CharField(default="", required=False)


class ScaDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class SCADBMavenBulkViewSet(UserEndPoint, viewsets.ViewSet):
    permission_classes_by_action = {
        "POST": (TalentAdminPermission,),
        "DELETE": (TalentAdminPermission,),
        "PUT": (TalentAdminPermission,),
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.request.method]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [ScaDBSerializer],
        summary=_("Get sca db bulk"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def list(self, request):
        ser = ScaDBSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q(import_from=ImportFrom.USER)
        if ser.validated_data.get("name"):
            q = Q(package_name__icontains=ser.validated_data["name"])
        queryset = ScaMavenDb.objects.filter(q)
        page_summary, page_data = self.get_paginator(
            queryset, ser.validated_data["page"], ser.validated_data["page_size"]
        )
        return R.success(
            data=ScaMavenDbSerializer(page_data, many=True).data, page=page_summary
        )

    @extend_schema_with_envcheck(
        request=ScaMavenDbUploadSerializer,
        summary=_("Get sca db bulk"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def create(self, request):
        if not request.FILES.get("file"):
            return R.failure(msg="file required")
        stream = request.FILES["file"].read().replace(b"\xEF\xBB\xBF", b"")
        decoded_files = stream.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_files)
        datas = [dict(row) for row in reader]
        ser = ScaMavenDbUploadSerializer(data=datas, many=True)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        objs = [ScaMavenDb(**i) for i in ser.validated_data]
        ScaMavenDb.objects.bulk_create(objs, ignore_conflicts=True)
        return R.success()


class SCADBMavenBulkDeleteView(UserEndPoint):
    permission_classes_by_action = {
        "POST": (TalentAdminPermission,),
        "DELETE": (TalentAdminPermission,),
        "PUT": (TalentAdminPermission,),
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.request.method]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        request=ScaDeleteSerializer,
        summary=_("Get sca db bulk"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def post(self, request):
        ids = request.data.get("ids")
        ScaMavenDb.objects.filter(pk__in=ids).delete()
        return R.success()


class SCADBMavenViewSet(UserEndPoint, viewsets.ViewSet):
    permission_classes_by_action = {
        "POST": (TalentAdminPermission,),
        "DELETE": (TalentAdminPermission,),
        "PUT": (TalentAdminPermission,),
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.request.method]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        summary=_("Get sca db"), description=_("Get sca list"), tags=[_("SCA DB")]
    )
    def retrieve(self, request, pk):
        q = Q(pk=pk)
        data = ScaMavenDb.objects.filter(q).first()
        return R.success(data=ScaDBSerializer(data).data)

    @extend_schema_with_envcheck(
        request=ScaMavenDbUploadSerializer,
        summary=_("Get sca db"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def create(self, request):
        ser = ScaMavenDbUploadSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            ScaMavenDb.objects.create(**ser.data)
        except IntegrityError:
            return R.failure(msg="same sha_1 component exists")
        return R.success()

    @extend_schema_with_envcheck(
        summary=_("Get sca db"), description=_("Get sca list"), tags=[_("SCA DB")]
    )
    def destory(self, request, pk):
        q = Q(pk=pk)
        ScaMavenDb.objects.filter(q).delete()
        return R.success()

    @extend_schema_with_envcheck(
        request=ScaMavenDbUploadSerializer,
        summary=_("Get sca db"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def update(self, request, pk):
        ser = ScaMavenDbUploadSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q(pk=pk)
        ScaMavenDb.objects.filter(q).update(**ser.data)
        return R.success()


LICENSE_LIST = [
    "Apache-1.0",
    "Apache-1.1",
    "Apache-2.0",
    "0BSD",
    "BSD-1-Clause",
    "BSD-2-Clause-FreeBSD",
    "BSD-2-Clause-NetBSD",
    "BSD-2-Clause-Patent",
    "BSD-2-Clause-Views",
    "BSD-2-Clause",
    "BSD-3-Clause-Attribution",
    "BSD-3-Clause-Clear",
    "BSD-3-Clause-LBNL",
    "BSD-3-Clause-Modification",
    "BSD-3-Clause-No-Military-License",
    "BSD-3-Clause-No-Nuclear-License-2014",
    "BSD-3-Clause-No-Nuclear-License",
    "BSD-3-Clause-No-Nuclear-Warranty",
    "BSD-3-Clause-Open-MPI",
    "BSD-3-Clause",
    "BSD-4-Clause-Shortened",
    "BSD-4-Clause-UC",
    "BSD-4-Clause",
    "BSD-Protection",
    "BSD-Source-Code",
    "AGPL-1.0-only",
    "AGPL-1.0-or-later",
    "AGPL-1.0",
    "AGPL-3.0-only",
    "AGPL-3.0-or-later",
    "AGPL-3.0",
    "GPL-1.0+",
    "GPL-1.0-only",
    "GPL-1.0-or-later",
    "GPL-1.0",
    "GPL-2.0+",
    "GPL-2.0-only",
    "GPL-2.0-or-later",
    "GPL-2.0-with-autoconf-exception",
    "GPL-2.0-with-bison-exception",
    "GPL-2.0-with-classpath-exception",
    "GPL-2.0-with-font-exception",
    "GPL-2.0-with-GCC-exception",
    "GPL-2.0",
    "GPL-3.0+",
    "GPL-3.0-only",
    "GPL-3.0-or-later",
    "GPL-3.0-with-autoconf-exception",
    "GPL-3.0-with-GCC-exception",
    "GPL-3.0",
    "LGPL-2.0+",
    "LGPL-2.0-only",
    "LGPL-2.0-or-later",
    "LGPL-2.0",
    "LGPL-2.1+",
    "LGPL-2.1-only",
    "LGPL-2.1-or-later",
    "LGPL-2.1",
    "LGPL-3.0+",
    "LGPL-3.0-only",
    "LGPL-3.0-or-later",
    "LGPL-3.0",
    "LGPLLR",
    "MIT-0",
    "MIT-advertising",
    "MIT-CMU",
    "MIT-enna",
    "MIT-feh",
    "MIT-Modern-Variant",
    "MIT-open-group",
    "MIT",
    "MITNFA",
    "MPL-1.0",
    "MPL-1.1",
    "MPL-2.0-no-copyleft-exception",
    "MPL-2.0",
]


class SCALicenseViewSet(UserEndPoint):
    @extend_schema_with_envcheck(
        summary=_("Get sca license list"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def get(self, request):
        return R.success(data=LICENSE_LIST)


class SCATemplateViewSet(UserEndPoint):
    @extend_schema_with_envcheck(
        summary=_("Get sca license list"),
        description=_("Get sca list"),
        tags=[_("SCA DB")],
    )
    def get(self, request):
        return FileResponse(
            open(os.path.join(BASE_DIR, "static/assets/template/maven_sca.csv"), "rb"),
            filename="maven_sca.csv",
        )
