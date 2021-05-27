from django.db import models

from ..login_register.models import User

from datetime import datetime

# Create your models here.

class TripManager(models.Manager):
    def validate_trip(self, post_data, user_id):
        errors = []
        #no empty entries
        #travel dates should be future-dated
        #travel date to should not be before the travel date from

        #chrome's date format is yyyy-mm-dd
        today = datetime.today().strftime("%Y-%m-%d")

        date_from = post_data['date_from']
        date_to = post_data['date_to']

        if len(post_data['destination']) < 1 or len(post_data['description']) < 1:
            errors.append('destination/description fields are required')

        # NEED TO VALIDATE DATE
        date_from2 = date_from.replace("-", "")
        date_to2 = date_to.replace("-", "")
        today2 = today.replace("-", "")
        if date_to2 < date_from2:
            errors.append('date to should not be before date from')
        if date_from2 < today2:
            errors.append('dates should be after today')

        

        if not errors:
            new_trip = self.create(
                destination = post_data['destination'],
                description = post_data['description'],
                date_from = post_data['date_from'],
                date_to = post_data['date_to'],

                planner = User.objects.get(id=user_id),
                
            )
            return new_trip

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField()
    date_from = models.CharField(max_length=10)
    date_to = models.CharField(max_length=10)

    travelers = models.ManyToManyField(User, related_name='trips')
    planner = models.ForeignKey(User, related_name='planned_trips', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    def __str__(self):
        return self.destination