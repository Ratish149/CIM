from datetime import date

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_job_application_emails(application):
    """
    Sends email notifications for a new job application.
    1. To the Company: Notification with applicant summary.
    2. To the Applicant: Confirmation of receipt.
    """
    job = application.job
    company = job.company
    user = application.applicant

    # Common Context
    current_year = date.today().year

    # --- 1. Email to Applicant ---
    subject_applicant = f"Application Received: {job.title} at {company.company_name}"
    context_applicant = {
        "applicant_name": f"{user.first_name} {user.last_name}".strip()
        or user.username,
        "company_name": company.company_name,
        "job_title": job.title,
        "applied_date": application.applied_date.strftime("%B %d, %Y"),
        "current_year": current_year,
    }

    html_content_applicant = render_to_string(
        "jobbriz/application_confirmation.html", context_applicant
    )
    text_content_applicant = strip_tags(html_content_applicant)

    msg_applicant = EmailMultiAlternatives(
        subject_applicant,
        text_content_applicant,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    msg_applicant.attach_alternative(html_content_applicant, "text/html")
    msg_applicant.send()

    # --- 2. Email to Company ---
    # Only send if company has an email
    if company.company_email:
        subject_company = (
            f"New Application: {job.title} - {context_applicant['applicant_name']}"
        )

        # Gather Applicant Data
        skills = []
        education = []
        locations = []
        work_experience = ""

        if hasattr(user, "jobseeker"):
            job_seeker = user.jobseeker
            skills = job_seeker.skills.all()
            education = job_seeker.education.all()
            locations = job_seeker.preferred_locations.all()
            work_experience = job_seeker.work_experience
        context_company = {
            "job_title": job.title,
            "applicant_name": context_applicant["applicant_name"],
            "applicant_email": user.email,
            "applicant_locations": locations,
            "applicant_experience": work_experience,
            "applicant_skills": skills,
            "applicant_education": education,
            "cover_letter": application.cover_letter,
            "current_year": current_year,
        }

        html_content_company = render_to_string(
            "jobbriz/application_notification.html", context_company
        )
        text_content_company = strip_tags(html_content_company)

        msg_company = EmailMultiAlternatives(
            subject_company,
            text_content_company,
            settings.DEFAULT_FROM_EMAIL,
            [company.company_email],
        )
        msg_company.attach_alternative(html_content_company, "text/html")
        msg_company.send()
