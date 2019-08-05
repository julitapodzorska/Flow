from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# DATABASE MODELS

BLEEDING = (

        (0, 'brak'),
        (1, 'słabe'),
        (2, 'umiarkowane'),
        (3, 'obfite'),

)

PAIN = (

        (1, 'słaby'),
        (2, 'umiarkowany'),
        (3, 'silny'),
)


MOOD = (

        (1, 'radosny'),
        (2, 'wrażliwy'),
        (3, 'smutny'),
        (4, 'PMS'),
)

SEX = (

        (1, 'z zabezpieczeniem'),
        (2, 'bez zabezpieczenia'),
)

ENERGY = (
        (1, 'niski'),
        (2, 'wysoki'),
        (3, 'wyczerany'),

)

class MyUserManager(BaseUserManager):
    def create_user(self,username, email, first_name, last_name, password, last_cycle, avg_cycle):
        user = self.model(email = email, username = username,
                          first_name = first_name, last_name = last_name,
                          last_cycle = last_cycle, avg_cycle = avg_cycle)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, last_cycle, avg_cycle, password):
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          last_cycle=last_cycle, avg_cycle=avg_cycle)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    last_cycle = models.DateField()
    avg_cycle = models.IntegerField()
    objects = MyUserManager()
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name','last_cycle', 'avg_cycle']


class HealthData(models.Model):
    bleeding = models.IntegerField(choices=BLEEDING)
    pain = models.IntegerField(choices=PAIN)
    mood = models.IntegerField(choices=MOOD)
    sex = models.IntegerField(choices=SEX)
    energy = models.IntegerField(choices=ENERGY)
    notes = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

