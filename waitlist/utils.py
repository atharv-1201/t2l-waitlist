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

    # Verify email settings
    logger.debug(f"Email settings: HOST={settings.EMAIL_HOST}, "
                f"PORT={settings.EMAIL_PORT}, "
                f"TLS={settings.EMAIL_USE_TLS}, "
                f"FROM={settings.DEFAULT_FROM_EMAIL}")

    try:
        # Attempt to render template
        logger.debug("Attempting to render email template")
        try:
            html_message = render_to_string('emails/welcome_email.html', {
                'full_name': user_data['full_name'],
                'role': user_data['role'],
                'location': user_data['location']
            })
            logger.debug("Template rendered successfully")
        except TemplateDoesNotExist as te:
            logger.error(f"Email template not found: {str(te)}")
            logger.error(f"Template dirs: {settings.TEMPLATES[0]['DIRS']}")
            return False
        except Exception as template_error:
            logger.error(f"Template rendering error: {str(template_error)}")
            return False

        # Attempt to send email
        logger.debug(f"Attempting to send email to {user_data['email']}")
        result = send_mail(
            subject="Welcome to Turn2Law Waitlist!",
            message='',  
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_data['email']],
            fail_silently=False,
        )
        
        if result:
            logger.info(f"Email successfully sent to {user_data['email']}")
            return True
        else:
            logger.error("Email send failed - returned 0")
            return False
            
    except ConnectionRefusedError as e:
        logger.error(f"Connection refused: Check email server settings: {str(e)}")
        return False
    except Exception as e:
        logger.error("Unexpected error during email send")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return False