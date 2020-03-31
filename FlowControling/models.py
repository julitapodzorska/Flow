from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from multiselectfield import MultiSelectField


# DATABASE MODELS

BLEEDING = (

        (0, 'wybierz'),
        (1, 'Słabe'),
        (2, 'Umiarkowane'),
        (3, 'Obfite'),
        (4, 'Plamienie'),

)

PAIN = (
        (0, 'wybierz'),
        (1, 'Słaby'),
        (2, 'Umiarkowany'),
        (3, 'Silny'),
)


MOOD = (
        (0, 'wybierz'),
        (1, 'Radosny'),
        (2, 'Wrażliwy'),
        (3, 'Smutny'),
        (4, 'PMS'),
        (5, 'Płaczliwość'),
        (6, 'Niepokój'),
)

SEX = (
        (0, 'wybierz'),
        (1, 'Z zabezpieczeniem'),
        (2, 'Bez zabezpieczenia'),
)

ENERGY = (
        (0, 'wybierz'),
        (1, 'Niski'),
        (2, 'Wysoki'),
        (3, 'Wyczerpany'),
)

DIFFERENT = (

    (1, 'Bóle mięśni'),
    (2, 'Bezsenność'),
    (3, 'Ból głowy'),
    (4, 'Libido podniesione'),
    (5, 'Libido obniżone'),
    (6, 'Bolesne piersi'),
    (7, 'Obrzęk piersi'),

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
    different = MultiSelectField(choices=DIFFERENT)
    notes = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()


class CycleLength(models.Model):
    length = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


