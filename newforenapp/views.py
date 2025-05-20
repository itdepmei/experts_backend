from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *  #
from .serializers import *
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

class ReportAPIView(APIView):
    permission_classes = [AllowAny]

    
    def get(self, request, uuid=None):
        if uuid:
            report = get_object_or_404(Report, uuid=uuid)
            serializer = ReportSerializer(report)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
    
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, uuid =None ):
        if uuid:
            try:
                report = Report.objects.get(uuid=uuid)
                report.delete()
                return Response({"message": "Report deleted"}, status=status.HTTP_200_OK)
            except Report.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            reports = Report.objects.all()
            reports.delete()
            return Response({"message": "All reports deleted"}, status=status.HTTP_200_OK)
        
        

class CommitteeMemberView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uuid=None):
        if uuid:
            member = get_object_or_404(CommitteeMember, uuid=uuid)
            serializer = CommitteeMemberSerializer(member)
            return Response({"data": serializer.data})
        members = CommitteeMember.objects.all()
        serializer = CommitteeMemberSerializer(members, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = CommitteeMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CommitteeMemberBySection(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        try:
            members = CommitteeMember.objects.filter( section_uuid=uuid)
            serializer = CommitteeMemberSerializer(members, many=True)
            return Response({"data": serializer.data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        