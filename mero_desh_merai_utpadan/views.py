from rest_framework import generics
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    MeroDeshMeraiUtpadanSerializer
)
import fitz
import os
from rest_framework.response import Response


class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = NatureOfIndustrySubCategorySerializer
    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            return NatureOfIndustrySubCategory.objects.filter(category_id=category_id)
        return NatureOfIndustrySubCategory.objects.all()

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

    def create(self, request, *args, **kwargs):
    # Get serializer instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the instance
        instance = serializer.save()

        # Ensure the media directory exists
        output_dir = "media/"
        os.makedirs(output_dir, exist_ok=True)
        output_pdf = f"{output_dir}merodeshmeraiutpadan_{instance.id}.pdf"

        # Define paths for input and output PDFs
        input_pdf = "media/PDFSample.pdf"

        # Data to populate the form fields
        field_data = {
            'ChalanNo': f"2081/82 - {instance.id}",
            'Name': instance.contact_name or "N/A",
            'CompanyName': instance.name_of_company or "N/A",
            'Location': instance.address_street or "N/A",
            'Content': "Thank you for choosing Mero Desh Merai Utpadan.",
            'CreatedAt': instance.created_at.strftime('%Y-%m-%d') if instance.created_at else "N/A"
        }

        # Ensure all values are strings
        field_data = {key: str(value) for key, value in field_data.items()}

        # Fill the PDF
        pdf = fitz.open(input_pdf)
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    if widget.field_name in field_data:
                        widget.field_value = field_data[widget.field_name]  # Set the value
                        widget.update()
        pdf.save(output_pdf)
        pdf.close()

        # Build the file URL
        file_url = request.build_absolute_uri(f"/media/merodeshmeraiutpadan_{instance.id}.pdf")

        # Save the file URL to the instance
        instance.file_url = file_url
        instance.save()

        # Return a JSON response with the file URL
        return Response({
            "message": "PDF generated successfully.",
            "file_url": file_url
        }, status=201)


class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer
