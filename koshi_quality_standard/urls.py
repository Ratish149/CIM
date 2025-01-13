from django.urls import path
from .views import RequirementListView,CalculatePointsView,RequirementQuestionBulkUploadView

urlpatterns = [

    path('requirements/', RequirementListView.as_view(), name='requirement-list'),  # GET: Fetch all requirements and questions
    path('calculate-points/', CalculatePointsView.as_view(), name='calculate-points'),  # POST: Submit answers and calculate points
    path('upload-requirements/', RequirementQuestionBulkUploadView.as_view(), name='upload-requirements'),

]