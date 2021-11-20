from django.db import models

# Create your models here.

def validate_number_plate(number_plate) -> bool:
    parts = number_plate.split('-')
    return True if parts[0].isalpha() and parts[1].isnumeric() and parts[2].isnumeric() else False

class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    def get_distribution(self):
        total_rows = (self.vehicle_type.max_capacity + 1) // 2
        standard_distribution_matrix = [[True]*2 for _ in range(total_rows)]
        standard_distribution_matrix[len(standard_distribution_matrix)-1][-1] = False
        return standard_distribution_matrix


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self) -> bool:
        return self.end
