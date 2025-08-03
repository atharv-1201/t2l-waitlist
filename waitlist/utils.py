from django.core.mail import send_mail
from django.template.loader import render_to_string, TemplateDoesNotExist
from django.conf import settings
import logging
import traceback

# Create a dedicated logger for email functionality
logger = logging.getLogger('waitlist.email')

def send_welcome_email(user_data):
    """
    Send welcome email to newly registered users with enhanced debugging
    """
    logger.debug(f"Starting email send process with data: {user_data}")
    
    # Validate input data
    if not all(key in user_data for key in ['full_name', 'email', 'role', 'location']):
        logger.error(f"Missing required fields. Received fields: {list(user_data.keys())}")
        return False

    # Verify email settings exist
    try:
        email_host = getattr(settings, 'EMAIL_HOST', None)
        default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', None)
        
        logger.debug(f"Email settings: HOST={email_host}, "
                    f"PORT={getattr(settings, 'EMAIL_PORT', 'NOT_SET')}, "
                    f"TLS={getattr(settings, 'EMAIL_USE_TLS', 'NOT_SET')}, "
                    f"FROM={default_from_email}, "
                    f"USER={email_host_user}")
        
        if not email_host or not default_from_email:
            logger.error("Email settings not properly configured")
            return False
            
    except Exception as e:
        logger.error(f"Error checking email settings: {str(e)}")
        return False

    try:
        # Create a plain text fallback message (REQUIRED)
        plain_text_message = f"""
Hi {user_data['full_name']},

Thank you for joining the Turn2Law waitlist!

We've received your registration with the following details:
• Role: {user_data['role']}
• Location: {user_data['location']}

We'll keep you updated on our progress and notify you as soon as Turn2Law is available.

Best regards,
The Turn2Law Team
        """.strip()

        # Attempt to render HTML template
        html_message = None
        logger.debug("Attempting to render email template")
        try:
            html_message = render_to_string('emails/welcome_email.html', {
                'full_name': user_data['full_name'],
                'role': user_data['role'],
                'location': user_data['location']
            })
            logger.info("HTML template rendered successfully")
        except TemplateDoesNotExist as te:
            logger.warning(f"Email template not found: {str(te)} - using plain text only")
            html_message = None
        except Exception as template_error:
            logger.warning(f"Template rendering error: {str(template_error)} - using plain text only")
            html_message = None

        # Get the from email address - FIXED
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'noreply@turn2law.com'))
        
        # Attempt to send email
        logger.info(f"Attempting to send email to {user_data['email']} from {from_email}")
        
        result = send_mail(
            subject="Welcome to Turn2Law Waitlist!",
            message=plain_text_message,
            html_message=html_message,
            from_email=from_email,  # ← FIXED: Use proper from_email
            recipient_list=[user_data['email']],
            fail_silently=False,
        )
        
        if result == 1:  # send_mail returns number of emails sent
            logger.info(f"Email successfully sent to {user_data['email']}")
            return True
        else:
            logger.error(f"Email send failed - send_mail returned {result}")
            return False
            
    except Exception as e:
        logger.error("Unexpected error during email send")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        
        # Log specific SMTP errors
        if hasattr(e, 'smtp_code'):
            logger.error(f"SMTP Code: {e.smtp_code}")
        if hasattr(e, 'smtp_error'):
            logger.error(f"SMTP Error: {e.smtp_error}")
            
        logger.debug(f"Full traceback:\n{traceback.format_exc()}")
        return False