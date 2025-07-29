from rest_framework import serializers
from .models import WaitlistEntry

class WaitlistEntrySerializer(serializers.ModelSerializer):
    interests = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = WaitlistEntry
        fields = ['full_name', 'email', 'location', 'role', 'interests']

    def validate_email(self, value):
        if WaitlistEntry.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value