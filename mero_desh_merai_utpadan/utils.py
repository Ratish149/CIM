import os

import fitz
import nepali_datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def process_mdmu_approval(instance, new_status="Approved"):
    """
    Processes the MDMU approval: generates PDF, sends email, and updates status.
    """
    try:
        if new_status == "Approved":
            # Create pdf directory inside media if it doesn't exist
            output_dir = "media/pdf/mdmu/"
            os.makedirs(output_dir, exist_ok=True)
            output_pdf = f"{output_dir}merodeshmeraiutpadan_{instance.id}.pdf"

            # Define the path to the input PDF
            input_pdf = "static/pdf/mdmu_final.pdf"

            # Convert English date to Nepali date
            english_date = instance.created_at
            if english_date:
                english_date_only = english_date.date()
                nepali_date = nepali_datetime.date.from_datetime_date(
                    english_date_only
                ).strftime("%B %d, %Y")
            else:
                nepali_date = "N/A"

            # Data to populate the form fields
            field_data = {
                "ChalanNo": f"2081/82 - {instance.id}",
                "CompanyName": instance.name_of_company or "N/A",
                "Location": instance.address_street or "N/A",
                "CreatedAt": nepali_date,
            }

            # Fill the PDF
            pdf = fitz.open(input_pdf)
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                widgets = page.widgets()
                if widgets:
                    for widget in widgets:
                        if widget.field_name in field_data:
                            widget.field_value = field_data[widget.field_name]
                            widget.update()

            # Save the updated PDF
            pdf.save(output_pdf)
            pdf.close()

            # Build the file URL
            file_url = f"/media/pdf/mdmu/merodeshmeraiutpadan_{instance.id}.pdf"
            instance.file_url = file_url

            # Send email if contact_email exists
            if instance.contact_email:
                subject = 'Thank You for Participating in the "Mero Desh Merai Utpadan" Campaign'

                # Load the HTML template
                context = {
                    "issue": instance,
                    "name": instance.contact_name,
                    "logo_url": os.path.join(
                        settings.STATIC_ROOT, "logo", "mdmu-logo.png"
                    ),
                }
                html_message = render_to_string(
                    "email_template/mdmu_email_template.html", context
                )

                # Create email message
                email = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[instance.contact_email],
                )

                # Attach the generated PDF
                with open(output_pdf, "rb") as pdf_file:
                    email.attach(
                        f"merodeshmeraiutpadan_{instance.id}.pdf",
                        pdf_file.read(),
                        "application/pdf",
                    )

                # Attach the logo
                logo_path = os.path.join(settings.STATIC_ROOT, "logo", "mdmu-logo.png")
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as logo_file:
                        email.attach("mdmu-logo.png", logo_file.read(), "image/png")

                email.content_subtype = "html"
                email.send(fail_silently=False)

        elif new_status == "Rejected" and instance.contact_email:
            # Send rejection email
            subject = 'Update on Your "Mero Desh Merai Utpadan" Campaign Application'

            context = {
                "name": instance.contact_name,
                "company_name": instance.name_of_company,
            }
            html_message = render_to_string(
                "email_template/mdmu_rejection_email.html", context
            )

            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[instance.contact_email],
            )

            email.content_subtype = "html"
            email.send(fail_silently=False)

        # Update the status
        instance.status = new_status
        instance.save()
        return True, None

    except Exception as e:
        return False, str(e)
