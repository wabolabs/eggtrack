from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Hen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, blank=True, related_name='hens')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='hens')
    date_added = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='hens/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class EggLog(models.Model):
    hen = models.ForeignKey(Hen, on_delete=models.CASCADE, related_name='egg_logs')
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'hen']
        unique_together = ['hen', 'date']

    def __str__(self):
        return f"{self.hen.name} - {self.date} ({self.quantity} eggs)"
