from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For FontAwesome icons
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20, 
        choices=[
            ('sports', 'Sports'),
            ('esports', 'Esports'),
            ('cultural', 'Cultural'),
            ('academic', 'Academic'),
            ('technology', 'Technology'),
            ('other', 'Other'),
        ]
    )
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TournamentImage(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='tournament_images')
    image = models.ImageField(upload_to='tournament_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.tournament.title}"

class Upis(models.Model):
    upi_id = models.CharField(max_length=100, unique=True, help_text="UPI ID for payment collection")
    nickname = models.CharField(max_length=100,blank=True,null=True, unique=True, help_text="Nickname for the UPI ID")
    name = models.CharField(max_length=100, help_text="Name associated with the UPI ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tournaments')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_tournaments', default=None, null=True)
    # Event Details
    start_date = models.DateField()
    end_date = models.DateField()
    tournament_time = models.TimeField(default=timezone.datetime.strptime('10:00', '%H:%M').time())
    # time = models.TimeField() #default should be 10am
    registration_deadline = models.DateTimeField()
    venue = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Tournament Specifics
    max_participants = models.PositiveIntegerField()
    min_participants = models.PositiveIntegerField(default=2)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    tournament_format = models.CharField(max_length=100)  # e.g., "Single Elimination", "Double Elimination", "Round Robin"
    rules = models.TextField()
    
    # Media
    banner_image = models.ImageField(upload_to='tournament_banners/')
    additional_images = models.ManyToManyField(TournamentImage, blank=True, related_name='additional_tournaments')
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Social Media
    facebook_event = models.URLField(blank=True)
    instagram_post = models.URLField(blank=True)
    
    upi_id = models.ForeignKey(
        Upis,
        max_length=100, 
        blank=True, 
        help_text="UPI ID for payment collection",
        on_delete=models.SET_NULL,
        null=True,
        related_name='tournaments'
    )
    
    
    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS, 
        default='pending'
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Transaction ID or UPI reference number"
    )
    payment_screenshot = models.ImageField(
        upload_to='payment_proofs/', 
        blank=True,
        help_text="Screenshot of payment confirmation"
    )
    
    # Ticket Information
    ticket_count = models.PositiveIntegerField(default=1)
    ticket_numbers = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Comma-separated ticket numbers"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        # Update payment date when status changes to completed
        if self.payment_status == 'completed' and not self.payment_date:
            self.payment_date = timezone.now()
            self.participant.payment_status = True
            self.participant.save()
            
        super().save(*args, **kwargs)

    @property
    def is_verified(self):
        return self.payment_status == 'completed'

class Participant(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('eliminated', 'Eliminated'),
        ('winner', 'Winner'),
        ('disqualified', 'Disqualified'),
        ('rejected', 'Rejected')
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament')
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(blank=True, null=True, unique=False, help_text="Email address for updates and notifications")
    phone = models.CharField(max_length=20)
    wp = models.CharField(max_length=10, blank=True, help_text="WhatsApp number for updates")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    
    # Registration Details
    registration_date = models.DateTimeField(auto_now_add=True)
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    check_in_time = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    special_requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='participant')

    optinWhatsapp = models.BooleanField(default=True)

    class Meta:
        unique_together = ['tournament', 'email']

    def __str__(self):
        return f"{self.full_name} - {self.tournament.title}"

class TournamentPrize(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='prizes')
    position = models.PositiveIntegerField()
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    winner = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name='prizes_won')

    class Meta:
        ordering = ['position']
        unique_together = ['tournament', 'position']

    def __str__(self):
        return f"{self.position} Place - {self.tournament.title}"

class TournamentSponsor(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='sponsors')
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/')
    website = models.URLField(blank=True)
    sponsorship_level = models.CharField(max_length=50)  # e.g., "Gold", "Silver", "Bronze"
    contribution = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.tournament.title}"

class TournamentAnnouncement(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.tournament.title}" 
    

class ChessPlayer(models.Model):
    TITLE_CHOICES = [
        ('', 'No Title'),
        ('GM', 'Grandmaster (GM)'),
        ('IM', 'International Master (IM)'),
        ('FM', 'FIDE Master (FM)'),
        ('CM', 'Candidate Master (CM)'),
        ('WGM', 'Woman Grandmaster (WGM)'),
        ('WIM', 'Woman International Master (WIM)'),
        ('WFM', 'Woman FIDE Master (WFM)'),
        ('WCM', 'Woman Candidate Master (WCM)'),
    ]

    SECTION_CHOICES = [
        ('open', 'Open'),
        ('u1600', 'Under 1600'),
        ('u1400', 'Under 1400'),
        ('u1200', 'Under 1200'),
        ('u1000', 'Under 1000'),
    ]

    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='chess_profile',
        primary_key=True
    )
    
    # Chess Identification
    fide_id = models.CharField(max_length=20, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, blank=True)
    
    # Ratings
    fide_rating = models.PositiveIntegerField(null=True, blank=True)
    national_rating = models.PositiveIntegerField(null=True, blank=True)
    rapid_rating = models.PositiveIntegerField(null=True, blank=True)
    blitz_rating = models.PositiveIntegerField(null=True, blank=True)
    
    # Tournament Information
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    federation = models.CharField(max_length=100)
    club_academy = models.CharField(max_length=200, blank=True)
    is_arbiter = models.BooleanField(default=False)
    
    # Historical Data
    previous_tournaments = models.TextField(blank=True)
    achievements = models.TextField(blank=True)

    class Meta:
        verbose_name = "Chess Player"
        verbose_name_plural = "Chess Players"

    def __str__(self):
        return f"{self.participant.full_name} ({self.fide_id or 'No FIDE ID'}) - {self.get_section_display()}"

class logModal(models.Model):
    sec = models.CharField(max_length=100, blank=True, null=True)
    key = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=500, blank=True, null=True)
    sec_id = models.IntegerField(blank=True)

class EventData(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    wp = models.CharField(max_length=15, blank=True, null=True)
    add = models.CharField(max_length=150, blank=True, null=True)


class ApiData(models.Model):
    sid = models.CharField(max_length=150, blank=True, null=True)
    token = models.EmailField(max_length=150, blank=True, null=True)
    wp = models.CharField(max_length=15, blank=True, null=True)
    active = models.BooleanField(default=True)


