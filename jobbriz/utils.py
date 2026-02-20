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
    job_poster = job.user
    user = application.applicant
    company_name = job.company_name or "the company"

    # Common Context
    current_year = date.today().year

    # --- 1. Email to Applicant ---
    subject_applicant = f"Application Received: {job.title} at {company_name}"
    context_applicant = {
        "applicant_name": f"{user.first_name} {user.last_name}".strip()
        or user.username,
        "company_name": company_name,
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

    # --- 2. Email to Company or email_to (Priority: email_to > user.email) ---
    recipient_email = job.email_to or (job_poster.email if job_poster else None)

    if recipient_email:
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
            [recipient_email],
        )
        msg_company.attach_alternative(html_content_company, "text/html")
        msg_company.send()

    # --- 3. Separate Email to Admin ---
    if settings.ADMIN_EMAIL:
        subject_admin = f"ADMIN ALERT: New Job Application - {job.title} - {context_applicant['applicant_name']}"
        context_admin = (
            context_company.copy() if recipient_email else context_applicant.copy()
        )
        context_admin["is_admin_copy"] = True

        # Use company notification template as a base for admin if possible, else application confirmation
        template_admin = (
            "jobbriz/application_notification.html"
            if recipient_email
            else "jobbriz/application_confirmation.html"
        )

        html_content_admin = render_to_string(template_admin, context_admin)
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()


def send_internship_registration_emails(job_seeker):
    """
    Sends email notifications for a new internship registration.
    1. To the Job Seeker: Confirmation.
    2. To the Industry: Notification (if industry email exists).
    """
    industry = job_seeker.internship_industry
    current_year = date.today().year

    # --- 1. Email to Job Seeker ---
    if job_seeker.email:
        subject_seeker = "Internship Registration Confirmed"
        context_seeker = {
            "full_name": job_seeker.full_name or job_seeker.user.username,
            "industry_name": industry.name if industry else "the selected industry",
            "preferred_start_date": job_seeker.preferred_start_date,
            "internship_duration": job_seeker.internship_duration,
            "current_year": current_year,
        }

        html_content_seeker = render_to_string(
            "jobbriz/internship_registration_confirmation.html", context_seeker
        )
        text_content_seeker = strip_tags(html_content_seeker)

        msg_seeker = EmailMultiAlternatives(
            subject_seeker,
            text_content_seeker,
            settings.DEFAULT_FROM_EMAIL,
            [job_seeker.email],
        )
        msg_seeker.attach_alternative(html_content_seeker, "text/html")
        msg_seeker.send()

    # --- 2. Email to Industry ---
    if industry and industry.email:
        subject_industry = f"New Intern Interest: {job_seeker.full_name}"
        context_industry = {
            "job_seeker": job_seeker,
            "current_year": current_year,
        }

        html_content_industry = render_to_string(
            "jobbriz/internship_registration_industry_notification.html",
            context_industry,
        )
        text_content_industry = strip_tags(html_content_industry)

        msg_industry = EmailMultiAlternatives(
            subject_industry,
            text_content_industry,
            settings.DEFAULT_FROM_EMAIL,
            [industry.email],
        )
        msg_industry.attach_alternative(html_content_industry, "text/html")
        msg_industry.send()

    # --- 3. Separate Email to Admin ---
    if settings.ADMIN_EMAIL:
        subject_admin = f"ADMIN ALERT: Internship Registration - {job_seeker.full_name}"
        context_admin = {
            "job_seeker": job_seeker,
            "current_year": current_year,
            "is_admin_copy": True,
        }
        html_content_admin = render_to_string(
            "jobbriz/internship_registration_industry_notification.html",
            context_admin,
        )
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()


def send_apprenticeship_application_emails(application):
    """
    Sends email notifications for a new apprenticeship application.
    1. To the Applicant: Confirmation.
    2. To the Preferred Industries: Notification.
    """
    current_year = date.today().year

    # --- 1. Email to Applicant ---
    if application.email_address:
        subject_applicant = "Apprenticeship Application Received"
        context_applicant = {
            "full_name": application.full_name,
            "trade": application.trade,
            "preferred_provider": application.preferred_training_provider,
            "applied_date": application.created_at.strftime("%B %d, %Y"),
            "current_year": current_year,
        }

        html_content_applicant = render_to_string(
            "jobbriz/apprenticeship_confirmation.html", context_applicant
        )
        text_content_applicant = strip_tags(html_content_applicant)

        msg_applicant = EmailMultiAlternatives(
            subject_applicant,
            text_content_applicant,
            settings.DEFAULT_FROM_EMAIL,
            [application.email_address],
        )
        msg_applicant.attach_alternative(html_content_applicant, "text/html")
        msg_applicant.send()

    # --- 2. Email to Industries ---
    pref_industries = [
        application.industry_preference_1,
        application.industry_preference_2,
        application.industry_preference_3,
    ]

    # Filter out None and get unique emails
    industry_emails = set()
    for industry in pref_industries:
        if industry and industry.email:
            industry_emails.add(industry.email)

    if industry_emails:
        subject_industry = f"New Apprenticeship Interest: {application.full_name}"
        context_industry = {
            "application": application,
            "current_year": current_year,
        }

        html_content_industry = render_to_string(
            "jobbriz/apprenticeship_industry_notification.html",
            context_industry,
        )
        text_content_industry = strip_tags(html_content_industry)

        msg_industry = EmailMultiAlternatives(
            subject_industry,
            text_content_industry,
            settings.DEFAULT_FROM_EMAIL,
            list(industry_emails),
        )
        msg_industry.attach_alternative(html_content_industry, "text/html")
        msg_industry.send()

    # --- 3. Separate Email to Admin ---
    if settings.ADMIN_EMAIL:
        subject_admin = (
            f"ADMIN ALERT: Apprenticeship Interest - {application.full_name}"
        )
        context_admin = {
            "application": application,
            "current_year": current_year,
            "is_admin_copy": True,
        }
        html_content_admin = render_to_string(
            "jobbriz/apprenticeship_industry_notification.html",
            context_admin,
        )
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()


def send_work_interest_hire_emails(hire_request):
    """
    Sends email notifications for a new work interest hire request.
    1. To the Professional: Notification.
    2. To the Hirer: Confirmation.
    """
    work_interest = hire_request.work_interest
    professional_user = work_interest.user
    current_year = date.today().year

    # --- 1. Email to Professional ---
    professional_email = work_interest.email or (
        professional_user.email if professional_user else None
    )

    if professional_email:
        subject_prof = f"New Hire Request: {work_interest.title}"
        context_prof = {
            "professional_name": work_interest.name
            or (
                f"{professional_user.first_name} {professional_user.last_name}".strip()
                if professional_user
                else "Professional"
            ),
            "hirer_name": hire_request.name
            or (
                f"{hire_request.user.first_name} {hire_request.user.last_name}".strip()
                if hire_request.user
                else "Someone"
            ),
            "hirer_email": hire_request.email
            or (hire_request.user.email if hire_request.user else None),
            "hirer_phone": hire_request.phone,
            "message": hire_request.message,
            "work_interest_title": work_interest.title,
            "current_year": current_year,
        }

        html_content_prof = render_to_string(
            "jobbriz/work_interest_hire_notification.html", context_prof
        )
        text_content_prof = strip_tags(html_content_prof)

        msg_prof = EmailMultiAlternatives(
            subject_prof,
            text_content_prof,
            settings.DEFAULT_FROM_EMAIL,
            [professional_email],
        )
        msg_prof.attach_alternative(html_content_prof, "text/html")
        msg_prof.send()

    # --- 3. Separate Email to Admin ---
    if settings.ADMIN_EMAIL:
        subject_admin = f"ADMIN ALERT: Work Interest Hire - {work_interest.title}"
        context_admin = {
            "professional_name": work_interest.name or professional_user.username
            if professional_user
            else "Professional",
            "hirer_name": hire_request.name or hire_request.user.username
            if hire_request.user
            else "Someone",
            "hirer_email": hire_request.email or hire_request.user.email
            if hire_request.user
            else None,
            "hirer_phone": hire_request.phone,
            "message": hire_request.message,
            "work_interest_title": work_interest.title,
            "current_year": current_year,
            "is_admin_copy": True,
        }
        html_content_admin = render_to_string(
            "jobbriz/work_interest_hire_notification.html", context_admin
        )
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()

    # --- 2. Email to Hirer ---
    hirer_email = hire_request.email or (
        hire_request.user.email if hire_request.user else None
    )

    if hirer_email:
        # Use existing professional_name and context for consistency
        subject_hirer = f"Hire Request Sent: {work_interest.title}"
        prof_name = work_interest.name or (
            f"{professional_user.first_name} {professional_user.last_name}".strip()
            if professional_user
            else "Professional"
        )

        context_hirer = {
            "hirer_name": hire_request.name
            or (
                f"{hire_request.user.first_name} {hire_request.user.last_name}".strip()
                if hire_request.user
                else "Someone"
            ),
            "professional_name": prof_name,
            "professional_email": professional_email,
            "work_interest_title": work_interest.title,
            "current_year": current_year,
        }

        html_content_hirer = render_to_string(
            "jobbriz/work_interest_hire_confirmation.html", context_hirer
        )
        text_content_hirer = strip_tags(html_content_hirer)

        msg_hirer = EmailMultiAlternatives(
            subject_hirer,
            text_content_hirer,
            settings.DEFAULT_FROM_EMAIL,
            [hirer_email],
        )
        msg_hirer.attach_alternative(html_content_hirer, "text/html")
        msg_hirer.send()
