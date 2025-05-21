from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *  #
from .serializers import *
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

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
        



class IncidentImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        insertUuid = request.data.get('insertUuid')
        files = request.FILES.getlist('image')

        if not insertUuid or not files:
            return Response(
                {"error": "insertUuid and image files are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        images = []
        for file in files:
            image = IncidentImage.objects.create(insert_uuid=insertUuid, image=file)
            
            images.append(IncidentImageSerializer(image).data)

        return Response(
            {"message": "Images uploaded successfully.", "images": images},
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, *args, **kwargs):
        insertUuid = kwargs.get('insertUuid')

        if not insertUuid:
            images = IncidentImage.objects.all()
            serializer = IncidentImageSerializer(images, many=True)
            return Response(
                {"data": serializer.data},
                
            )


        images = IncidentImage.objects.filter(insert_uuid=insertUuid)
        
        if not images:
            return Response({"error": "No images found for this accident UUID."}, status=status.HTTP_404_NOT_FOUND)
        

        serializer = IncidentImageSerializer(images, many=True)
        return Response(
                            {"data": serializer.data},
                            status=status.HTTP_200_OK
                        ) 

    def delete(self, request, *args, **kwargs):
        image_id = request.query_params.get('id')
        insert_uuid = request.query_params.get('insertUuid')

        if image_id:
            try:
                image = IncidentImage.objects.get(id=image_id)
                image.delete()
                return Response({"message": f"Image with ID {image_id} deleted."}, status=status.HTTP_200_OK)
            except IncidentImage.DoesNotExist:
                return Response({"error": f"Image with ID {image_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        elif insert_uuid:
            deleted_count, _ = IncidentImage.objects.filter(insert_uuid=insert_uuid).delete()
            return Response({"message": f"{deleted_count} images deleted for insertUuid {insert_uuid}."}, status=status.HTTP_200_OK)

        else:
            deleted_count, _ = IncidentImage.objects.all().delete()
            return Response({"message": f"All {deleted_count} incident images deleted."}, status=status.HTTP_200_OK)

