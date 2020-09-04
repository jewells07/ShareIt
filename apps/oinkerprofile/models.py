from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class OinkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    avatar = models.ImageField(upload_to='uploads/', blank=True, null=True)

    # Resize image
    def save(self, *args, **kwargs):
        super(OinkerProfile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

User.oinkerprofile = property(lambda u:OinkerProfile.objects.get_or_create(user=u)[0])