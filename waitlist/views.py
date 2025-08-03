from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from django.http import JsonResponse, HttpResponse
from .serializers import WaitlistEntrySerializer
from .models import WaitlistEntry
from .utils import send_welcome_email
import logging
import traceback

logger = logging.getLogger(__name__)

def welcome_message(request):
    return HttpResponse("Welcome to Turn2Law API - Your Legal Tech Solution")

def debug_database(request):
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        # Test model access
        count = WaitlistEntry.objects.count()
        
        return JsonResponse({
            'status': 'success',
            'database_connected': True,
            'waitlist_entries_count': count,
            'model_test': 'passed'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'database_connected': False
        }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class WaitlistSignupView(APIView):
    def post(self, request):
        try:
            logger.info("=== Waitlist Signup Request Started ===")
            logger.info(f"Request origin: {request.META.get('HTTP_ORIGIN')}")
            logger.info(f"Content type: {request.content_type}")
            logger.info(f"Request data: {request.data}")

            serializer = WaitlistEntrySerializer(data=request.data)
            
            if serializer.is_valid():
                logger.info("Serializer validation passed")
                
                # Save the entry
                instance = serializer.save()
                logger.info(f"New waitlist entry created: {instance.email}")

                # Send welcome email (don't fail if email fails)
                try:
                    email_sent = send_welcome_email(
                        full_name=instance.full_name,
                        email=instance.email
                    )
                    if email_sent:
                        logger.info(f"Welcome email sent to {instance.email}")
                    else:
                        logger.warning(f"Email not sent to {instance.email}")
                except Exception as e:
                    logger.error(f"Email sending failed: {str(e)}")
                    # Continue execution even if email fails

                return Response({
                    'message': 'Registration successful',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            else:
                logger.error(f"Validation failed: {serializer.errors}")
                return Response({
                    'error': 'Validation failed',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error in WaitlistSignupView: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response({
                'error': 'Internal server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Handle GET requests for testing"""
        return Response({
            'message': 'Waitlist signup endpoint is working',
            'method': 'POST required for signup'
        })
