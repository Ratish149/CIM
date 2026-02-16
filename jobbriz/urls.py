from django.urls import path

from . import views

app_name = "job"

urlpatterns = [
    path("user/profile/", views.UserDetailView.as_view(), name="user-detail"),
    # ISCO Classification URLs
    path(
        "major-groups/",
        views.MajorGroupListCreateView.as_view(),
        name="major-group-list",
    ),
    path(
        "major-groups/<slug:slug>/",
        views.MajorGroupDetailView.as_view(),
        name="major-group-detail",
    ),
    path(
        "sub-major-groups/",
        views.SubMajorGroupListCreateView.as_view(),
        name="sub-major-group-list",
    ),
    path(
        "sub-major-groups/<slug:slug>/",
        views.SubMajorGroupDetailView.as_view(),
        name="sub-major-group-detail",
    ),
    path(
        "minor-groups/",
        views.MinorGroupListCreateView.as_view(),
        name="minor-group-list",
    ),
    path(
        "minor-groups/<slug:slug>/",
        views.MinorGroupDetailView.as_view(),
        name="minor-group-detail",
    ),
    path(
        "unit-groups/", views.UnitGroupListCreateView.as_view(), name="unit-group-list"
    ),
    path(
        "unit-groups/<slug:slug>/",
        views.UnitGroupDetailView.as_view(),
        name="unit-group-detail",
    ),
    # Job Posts
    path("jobs/", views.JobPostListCreateView.as_view(), name="job-list"),
    path("my-jobs/", views.MyJobListView.as_view(), name="my-jobs"),
    path("jobs/<slug:slug>/", views.JobPostDetailView.as_view(), name="job-detail"),
    path(
        "jobs/<slug:slug>/view/", views.JobPostViewCountView.as_view(), name="job-view"
    ),
    path("applied-jobs/", views.AppliedJobsView.as_view(), name="applied-jobs"),
    # Job Applications
    path(
        "jobs/<slug:job_slug>/apply/",
        views.JobApplicationCreateView.as_view(),
        name="job-apply",
    ),
    path(
        "applications/", views.JobApplicationListView.as_view(), name="application-list"
    ),
    path(
        "applications/<int:pk>/",
        views.JobApplicationDetailView.as_view(),
        name="application-detail",
    ),
    path(
        "applications/<int:pk>/status/",
        views.UpdateApplicationStatusView.as_view(),
        name="update-application-status",
    ),
    # Saved Jobs
    path(
        "jobs/<slug:job_slug>/save/",
        views.SavedJobToggleView.as_view(),
        name="save-job-toggle",
    ),
    path("saved-jobs/", views.SavedJobListView.as_view(), name="saved-job-list"),
    # Hire Requests
    path(
        "jobs/<slug:job_slug>/hire/<slug:jobseeker_slug>/",
        views.HireRequestCreateView.as_view(),
        name="hire-request-create",
    ),
    path(
        "hire-requests/", views.HireRequestListView.as_view(), name="hire-request-list"
    ),
    path(
        "hire-requests/<int:pk>/",
        views.HireRequestDetailView.as_view(),
        name="hire-request-detail",
    ),
    path(
        "hire-requests/<int:pk>/update-status/",
        views.HireRequestStatusUpdateView.as_view(),
        name="hire-request-status-update",
    ),
    path(
        "upload-isco-data/", views.UploadISCODataView.as_view(), name="upload_isco_data"
    ),
    path("search-groups/", views.AllGroupsSearchView.as_view(), name="groups-search"),
    # JobSeeker URLs
    path(
        "has-profile/",
        views.HasJobseekerProfileView.as_view(),
        name="has-jobseeker-profile",
    ),
    path("jobseekers/", views.JobSeekerListCreateView.as_view(), name="jobseeker-list"),
    path(
        "internship/register/",
        views.InternshipRegistrationView.as_view(),
        name="internship-register",
    ),
    path(
        "internship/register/<int:pk>/",
        views.InternshipDetailView.as_view(),
        name="internship-detail",
    ),
    path(
        "apprenticeship/apply/",
        views.ApprenticeshipApplicationCreateView.as_view(),
        name="apprenticeship-apply",
    ),
    path(
        "apprenticeship/applications/",
        views.ApprenticeshipApplicationListView.as_view(),
        name="apprenticeship-applications",
    ),
    path(
        "apprenticeship/applications/<int:pk>/",
        views.ApprenticeshipApplicationDetailView.as_view(),
        name="apprenticeship-application-detail",
    ),
    path(
        "jobseekers/detail/",
        views.JobSeekerDetailView.as_view(),
        name="jobseeker-detail",
    ),
    # Work Interest URLs
    path(
        "work-interests/",
        views.WorkInterestListCreateView.as_view(),
        name="work-interest-list",
    ),
    path(
        "work-interests/<int:pk>/",
        views.WorkInterestDetailView.as_view(),
        name="work-interest-detail",
    ),
    path(
        "work-interests/<int:pk>/hire/",
        views.WorkInterestHireCreateView.as_view(),
        name="work-interest-hire",
    ),
    # Location URLs
    path("locations/", views.LocationListCreateView.as_view(), name="location-list"),
    # Industry URLs
    path("industries/", views.IndustryListCreateView.as_view(), name="industry-list"),
    # Additional Model URLs
    path("languages/", views.LanguageListCreateView.as_view(), name="language-list"),
    path("skills/", views.SkillListCreateView.as_view(), name="skill-list"),
    path("skills/<int:pk>/", views.SkillDetailView.as_view(), name="skill-detail"),
    path(
        "certifications/",
        views.CertificationListCreateView.as_view(),
        name="certification-list",
    ),
    path(
        "certifications/<int:pk>/",
        views.CertificationDetailView.as_view(),
        name="certification-detail",
    ),
    path("education/", views.EducationListCreateView.as_view(), name="education-list"),
    path(
        "education/<int:pk>/",
        views.EducationDetailView.as_view(),
        name="education-detail",
    ),
    path(
        "career-history/",
        views.CareerHistoryListCreateView.as_view(),
        name="career-history-list",
    ),
    path(
        "career-history/<int:pk>/",
        views.CareerHistoryDetailView.as_view(),
        name="career-history-detail",
    ),
]
