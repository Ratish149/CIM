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
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django.db.models import Count

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
        
        # Save the issue first
        issue = serializer.save()
        
        # Track changes only for specific fields
        tracked_fields = {
            'progress_status': {
                'type': 'status_change',
                'old': old_instance.progress_status,
                'new': issue.progress_status,
                'use_status': True
            },
            'implementation_level': {
                'type': 'implementation_level_change',
                'old': old_instance.implementation_level,
                'new': issue.implementation_level,
            },
            'nature_of_industry_category': {
                'type': 'industry_category_change',
                'old': str(old_instance.nature_of_industry_category),
                'new': str(issue.nature_of_industry_category),
            },
            'nature_of_industry_sub_category': {
                'type': 'industry_subcategory_change',
                'old': str(old_instance.nature_of_industry_sub_category),
                'new': str(issue.nature_of_industry_sub_category),
            },
            'nature_of_issue': {
                'type': 'nature_of_issue_change',
                'old': old_instance.nature_of_issue,
                'new': issue.nature_of_issue,
            },
            'industry_size': {
                'type': 'industry_size_change',
                'old': old_instance.industry_size,
                'new': issue.industry_size,
            },
        }

        # Check each tracked field for changes
        for field, config in tracked_fields.items():
            old_value = config['old']
            new_value = config['new']
            
            if old_value != new_value:
                action_data = {
                    'issue': issue,
                    'action_type': config['type'],
                    'created_by': user,
                    'comment': comment,
                }
                
                if config.get('use_status', False):
                    action_data.update({
                        'old_status': old_value,
                        'new_status': new_value
                    })
                else:
                    action_data.update({
                        'old_value': old_value,
                        'new_value': new_value
                    })
                
                IssueAction.objects.create(**action_data)

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
