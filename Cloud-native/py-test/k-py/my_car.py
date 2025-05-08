from car import ElectricCar

my_new_car=ElectricCar('audi','a8',2020)

print(my_new_car.get_descriptive_name())

my_new_car.battery.describe_battery()
my_new_car.battery.get_range()