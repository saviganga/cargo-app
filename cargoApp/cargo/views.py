from django.shortcuts import render
from cargo import serializers as cargo_serializers
from cargo import models as cargo_models
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q


# Create your views here.

class CargoViewSet(ModelViewSet):

    queryset = cargo_models.CargoInfo.objects.all()
    serializer_class = cargo_serializers.CargoInfoSerializer

    def get_queryset(self):
        return self.queryset.all()

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(data={"status": "SUCCESS", "message": "Cargo info successfully added", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception:
            return Response(data={"status": "FAILED", "message": "Unable to add Cargo info", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=["post"], name="get_cargo_by_name")
    def get_cargo_by_name(self, request, *args, **kwargs):
        if request.data.get('name') == 'all':
            request.data['confidence_value'] = 0
        serializer = cargo_serializers.CargoByNameSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data.get('name') != 'all':
                try:
                    cargo = cargo_models.CargoInfo.objects.get( Q(vessel_name=serializer.validated_data.get('name')) | Q(short_name=serializer.validated_data.get('name')) )
                except Exception as get_cargo_error:
                    print(get_cargo_error)
                    return Response(
                        data={
                            "status": "FAILED",
                            "message": "Vessel is not on database"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                cargoinfo = {
                    "Vessel Name": cargo.vessel_name,
                    "Vessel Type": cargo.vessel_type,
                    "Built": cargo.built,
                    "GT": cargo.gt,
                    "DWT": cargo.dwt,
                    "Size(m) L/B": cargo.size,
                    "Draft(m)": cargo.draft
                }
            

                return Response(
                    data={
                        "status": "SUCCESS",
                        "message": f"Incoming vessel is {serializer.validated_data.get('name')}, with a confidence value of {serializer.validated_data.get('confidence_value')}%. More details in the table below",
                        "data": cargoinfo
                    },
                    status=status.HTTP_200_OK
                )
            else:
                cinfo = self.queryset.all()
                cargoinfo = self.serializer_class(cinfo, many=True)
                return Response(
                    data={
                        "status": "SUCCESS",
                        "data": cargoinfo.data
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            print(e)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "error"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            

            






