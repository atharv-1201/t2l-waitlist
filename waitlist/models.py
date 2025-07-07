from django.db import models
from django.utils import timezone

class WaitlistEntry(models.Model):
    
    id = models.AutoField(primary_key=True)

    
    ROLE_CHOICES = [
        ('individual', 'Individual needing legal help'),
        ('business_owner', 'Business Owner/Manager'),
        ('lawyer', 'Lawyer/Legal Professional'),
        ('law_student', 'Law Student'),
        ('investor', 'Investor/Partner'),
        ('other', 'Other'),
    ]

    
    full_name = models.CharField(
        max_length=255, 
        null=False, 
        blank=False,
        db_index=True
    )
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )
    location = models.CharField(
        max_length=255, 
        null=False,    
        blank=False,   
        db_index=True  
    )
    role = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES,
        null=False,
        blank=False
    )
    interests = models.TextField(
        blank=True, 
        null=True
    )
    
    # Metadata fields
    created_at = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        default=True,
        null=False
    )

    class Meta:
        verbose_name = 'Waitlist Entry'
        verbose_name_plural = 'Waitlist Entries'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['email'], 
                name='unique_email'
            )
        ]

    def __str__(self):
        return f"{self.full_name} - {self.email}"