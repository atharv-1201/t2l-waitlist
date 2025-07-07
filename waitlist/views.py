from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import WaitlistEntrySerializer
from .models import WaitlistEntry
from .utils import send_welcome_email
import logging
import traceback


logger = logging.getLogger(__name__)


def welcome_message(request):
    return HttpResponse("Welcome to Turn2Law API - Your Legal Tech Solution")


class WaitlistSignupView(APIView):
    def post(self, request):
        logger.info("Received waitlist signup request.")
        logger.info(f"Incoming content type: {request.content_type}")
        logger.info(f"Raw request data: {request.body}")
        logger.info(f"Parsed request.data: {request.data}")


        serializer = WaitlistEntrySerializer(data=request.data)
        if serializer.is_valid():
            try:

                instance = serializer.save()
                logger.info(f"New waitlist entry created: {instance.email}")


                user_data = {
                    'full_name': instance.full_name,
                    'email': instance.email,
                    'role': instance.get_role_display(),
                    'location': instance.location
                }


                try:
                    email_sent = send_welcome_email(user_data)
                    if not email_sent:
                        logger.warning(f"Email not sent to {instance.email}. Possibly a mail server issue.")
                except Exception as e:
                    logger.error(f"Exception during sending welcome email: {str(e)}")
                    logger.debug(traceback.format_exc())


                return Response({
                    'message': 'Registration successful',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error saving waitlist entry: {str(e)}")
                logger.debug(traceback.format_exc())
                return Response({
                    'error': 'An unexpected error occurred while processing your request.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:

            logger.warning(f"Validation failed: {serializer.errors}")
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
