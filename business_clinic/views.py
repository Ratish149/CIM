from django.shortcuts import render
from rest_framework import generics, filters
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    IssueSerializer,
    IssueActionSerializer,
)
from .models import (
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
    Issue,
    IssueAction,
)
from django.conf import settings

from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django.db.models import Count
from django.core.mail import send_mail  # Import send_mail for sending emails

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

class IssueFilter(django_filters.FilterSet):
    class Meta:
        model = Issue
        fields = {
            'progress_status': ['exact'],
            'nature_of_industry_category': ['exact'],
            'nature_of_issue': ['exact'],
            'industry_size': ['exact'],
            'member_of_CIM': ['exact'],
            'industry_specific_or_common_issue': ['exact'],
            'policy_related_or_procedural_issue': ['exact'],
            'implementation_level': ['exact'],
            'share_contact_details': ['exact'],
            'forward_to_authority': ['exact'],
        }

    def filter_boolean_fields(self, queryset, name, value):
        if value.lower() == 'true':
            return queryset.filter(**{name: True})
        elif value.lower() == 'false':
            return queryset.filter(**{name: False})
        return queryset

class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = IssueFilter
    search_fields = ['title', 'name_of_company', 'contact_name']

class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_update(self, serializer):
        old_instance = self.get_object()
        user = self.request.user if self.request.user.is_authenticated else None
        comment = self.request.data.get('comment', '')
        
        # Save the issue
        issue = serializer.save()
        changes_made = False  # Track if any changes were made
        change_details = []  # List to hold details of changes
        
        # Handle category and subcategory changes together
        if 'nature_of_industry_category' in self.request.data:
            old_category = str(old_instance.nature_of_industry_category)
            new_category = str(issue.nature_of_industry_category)
            old_subcategory = str(old_instance.nature_of_industry_sub_category)
            new_subcategory = str(issue.nature_of_industry_sub_category)
            
            if old_category != new_category or old_subcategory != new_subcategory:
                change_details.append(f"Industry Category changed from '{old_category} → {old_subcategory}' to '{new_category} → {new_subcategory}'")
                changes_made = True  # Mark that changes were made

        if 'nature_of_industry_sub_category' in self.request.data:
            old_subcategory = str(old_instance.nature_of_industry_sub_category)
            new_subcategory = str(issue.nature_of_industry_sub_category)
            if old_subcategory != new_subcategory:
                change_details.append(f"Industry Subcategory changed from '{old_subcategory}' to '{new_subcategory}'")
                changes_made = True

        if 'implementation_level' in self.request.data:
            old_implementation_level = str(old_instance.implementation_level)
            new_implementation_level = str(issue.implementation_level)
            if old_implementation_level != new_implementation_level:
                change_details.append(f"Implementation Level changed from '{old_implementation_level}' to '{new_implementation_level}'")
                changes_made = True

        if 'progress_status' in self.request.data:
            old_progress_status = str(old_instance.progress_status)
            new_progress_status = str(issue.progress_status)
            if old_progress_status != new_progress_status:
                change_details.append(f"Progress Status changed from '{old_progress_status}' to '{new_progress_status}'")
                changes_made = True

        if 'nature_of_issue' in self.request.data:
            old_nature_of_issue = str(old_instance.nature_of_issue)
            new_nature_of_issue = str(issue.nature_of_issue)
            if old_nature_of_issue != new_nature_of_issue:
                change_details.append(f"Nature of Issue changed from '{old_nature_of_issue}' to '{new_nature_of_issue}'")
                changes_made = True

        if 'industry_specific_or_common_issue' in self.request.data:
            old_industry_specific_or_common_issue = str(old_instance.industry_specific_or_common_issue)
            new_industry_specific_or_common_issue = str(issue.industry_specific_or_common_issue)
            if old_industry_specific_or_common_issue != new_industry_specific_or_common_issue:
                change_details.append(f"Industry Specific or Common Issue changed from '{old_industry_specific_or_common_issue}' to '{new_industry_specific_or_common_issue}'")
                changes_made = True

        if 'policy_related_or_procedural_issue' in self.request.data:
            old_policy_related_or_procedural_issue = str(old_instance.policy_related_or_procedural_issue)
            new_policy_related_or_procedural_issue = str(issue.policy_related_or_procedural_issue)
            if old_policy_related_or_procedural_issue != new_policy_related_or_procedural_issue:
                change_details.append(f"Policy Related or Procedural Issue changed from '{old_policy_related_or_procedural_issue}' to '{new_policy_related_or_procedural_issue}'")
                changes_made = True

        if 'industry_size' in self.request.data:
            old_industry_size = str(old_instance.industry_size)
            new_industry_size = str(issue.industry_size)
            if old_industry_size != new_industry_size:
                change_details.append(f"Industry Size changed from '{old_industry_size}' to '{new_industry_size}'")
                changes_made = True

        # Send email if changes were made
        if changes_made and user:
            change_summary = "\n".join(change_details)  # Create a summary of changes
            send_mail(
                'Issue Updated',
                f'Your issue has been updated with the following changes:\n\n{change_summary}',
                settings.DEFAULT_FROM_EMAIL,  # Replace with your sender email
                [user.email],  # Send to the user's email
                fail_silently=False,
            )

        return issue

class IssueActionViewSet(generics.ListCreateAPIView):
    serializer_class = IssueActionSerializer
    
    def get_queryset(self):
        return IssueAction.objects.filter(issue_id=self.kwargs['issue_pk'])
    
    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            issue=issue,
            created_by=user
        )

@api_view(['GET'])
def issue_statistics(request):
    # Apply filters from query params
    queryset = Issue.objects.all()
    
    # Apply the same filters as the main list
    if 'progress_status' in request.GET:
        queryset = queryset.filter(progress_status=request.GET['progress_status'])
    if 'nature_of_industry_category' in request.GET:
        queryset = queryset.filter(nature_of_industry_category=request.GET['nature_of_industry_category'])
    if 'nature_of_issue' in request.GET:
        queryset = queryset.filter(nature_of_issue=request.GET['nature_of_issue'])
    
    # Get statistics
    status_stats = queryset.values('progress_status').annotate(count=Count('id'))
    industry_stats = queryset.values(
        'nature_of_industry_category__name'
    ).annotate(count=Count('id'))
    issue_type_stats = queryset.values('nature_of_issue').annotate(count=Count('id'))
    specificity_stats = queryset.values(
        'industry_specific_or_common_issue'
    ).annotate(count=Count('id'))
    policy_stats = queryset.values(
        'policy_related_or_procedural_issue'
    ).annotate(count=Count('id'))
    implementation_level_stats = queryset.values('implementation_level').annotate(count=Count('id'))

    return Response({
        'status_distribution': status_stats,
        'industry_distribution': industry_stats,
        'issue_type_distribution': issue_type_stats,
        'specificity_distribution': specificity_stats,
        'policy_distribution': policy_stats,
        'implementation_level_distribution': implementation_level_stats,
        'total_issues': queryset.count()
    })
