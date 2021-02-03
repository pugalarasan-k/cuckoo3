# Copyright (C) 2020 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from rest_framework.parsers import MultiPartParser
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from cuckoo.common.importing import (
    store_importable, AnalysisImportError, list_importables, notify
)

class AnalysisImport(serializers.Serializer):
    file = serializers.FileField()

class ImportAnalysis(APIView):

    permission_classes = (IsAdminUser,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AnalysisImport(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        uploaded = request.FILES["file"]

        try:
            store_importable(uploaded.temporary_file_path())
        except AnalysisImportError as e:
            return Response({"error": str(e)}, status=400)

        return Response(status=200)

    def get(self, request):
        return Response(list_importables())

    def put(self, request):
        try:
            notify()
        except AnalysisImportError as e:
            return Response({"error": str(e)}, status=500)

        return Response(status=200)
