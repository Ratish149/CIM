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
        
        # Track if any changes were made
        changes_made = False  
        
        # Handle category and subcategory changes together
        if 'nature_of_industry_category' in self.request.data:
            old_category = str(old_instance.nature_of_industry_category)
            new_category = str(issue.nature_of_industry_category)
            old_subcategory = str(old_instance.nature_of_industry_sub_category)
            new_subcategory = str(issue.nature_of_industry_sub_category)
            
            if old_category != new_category or old_subcategory != new_subcategory:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='industry_category_change',
                    old_value=f"{old_category} → {old_subcategory}",
                    new_value=f"{new_category} → {new_subcategory}",
                    comment=comment
                )
                changes_made = True  # Mark that changes were made
                self.send_change_email(user, action)

        if 'nature_of_industry_sub_category' in self.request.data:
            old_subcategory = str(old_instance.nature_of_industry_sub_category)
            new_subcategory = str(issue.nature_of_industry_sub_category)
            if old_subcategory != new_subcategory:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='industry_subcategory_change',
                    old_value=old_subcategory,
                    new_value=new_subcategory,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        
        if 'implementation_level' in self.request.data:
            old_implementation_level = str(old_instance.implementation_level)
            new_implementation_level = str(issue.implementation_level)
            if old_implementation_level != new_implementation_level:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='implementation_level_change',
                    old_value=old_implementation_level,
                    new_value=new_implementation_level,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        
        if 'progress_status' in self.request.data:
            old_progress_status = str(old_instance.progress_status)
            new_progress_status = str(issue.progress_status)
            if old_progress_status != new_progress_status:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='progress_status_change',
                    old_value=old_progress_status,
                    new_value=new_progress_status,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        
        if 'nature_of_issue' in self.request.data:
            old_nature_of_issue = str(old_instance.nature_of_issue)
            new_nature_of_issue = str(issue.nature_of_issue)
            if old_nature_of_issue != new_nature_of_issue:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='nature_of_issue_change',
                    old_value=old_nature_of_issue,
                    new_value=new_nature_of_issue,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        
        if 'industry_specific_or_common_issue' in self.request.data:
            old_industry_specific_or_common_issue = str(old_instance.industry_specific_or_common_issue)
            new_industry_specific_or_common_issue = str(issue.industry_specific_or_common_issue)
            if old_industry_specific_or_common_issue != new_industry_specific_or_common_issue:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='industry_specific_or_common_issue_change',
                    old_value=old_industry_specific_or_common_issue,
                    new_value=new_industry_specific_or_common_issue,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        
        if 'policy_related_or_procedural_issue' in self.request.data:
            old_policy_related_or_procedural_issue = str(old_instance.policy_related_or_procedural_issue)
            new_policy_related_or_procedural_issue = str(issue.policy_related_or_procedural_issue)
            if old_policy_related_or_procedural_issue != new_policy_related_or_procedural_issue:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='policy_related_or_procedural_issue_change',
                    old_value=old_policy_related_or_procedural_issue,
                    new_value=new_policy_related_or_procedural_issue,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)
        if 'industry_size' in self.request.data:
            old_industry_size = str(old_instance.industry_size)
            new_industry_size = str(issue.industry_size)
            if old_industry_size != new_industry_size:
                action = IssueAction.objects.create(
                    issue=issue,
                    action_type='industry_size_change',
                    old_value=old_industry_size,
                    new_value=new_industry_size,
                    comment=comment
                )
                changes_made = True
                self.send_change_email(user, action)

        return issue

    def send_change_email(self, user, action):
        if user:
            send_mail(
                'Issue Updated',
                f'Your issue has been updated with the following change:\n\n'
                f'Action Type: {action.action_type}\n'
                f'Old Value: {action.old_value}\n'
                f'New Value: {action.new_value}\n'
                f'Comment: {action.comment}',
                settings.DEFAULT_FROM_EMAIL,  # Replace with your sender email
                [user.email],  # Send to the user's email
                fail_silently=False,
            )

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
