class Car:
      """一次模拟汽车的简单尝试。"""

      def __init__(self,make,model,year):
          self.make = make
          self.model = model
          self.year = year
          self.odometer_reading = 0

      def get_descriptive_name(self):
          long_name = f"{self.year} {self.make} {self.model}"
          return long_name.title()

      def read_odometer(self):
          print(f"This car has {self.odometer_reading} miles on it.")

      def update_odometer(self,mileage):
          if mileage >= self.odometer_reading:
              self.odometer_reading = mileage
          else:
              print("You can't roll back an odometer!")

      def increment_odometer(self,miles):
          self.odometer_reading += miles
class Battery:
    """一次模拟电动汽车电瓶的简单尝试"""
    def __init__(self,battery_size=75):
        self.battery_size = battery_size

    def describe_battery(self):
        """打印一条描述电瓶容量的消息"""
        print(f"This car has a {self.battery_size}-kwh battery .")

    def get_range(self):
        """打印一条消息，指出电瓶的续航里程"""
        if self.battery_size == 75:
            range = 260
        elif self.battery_size == 100:
            range = 315

        print(f"This car can go about {range} miles on a full charge.")

class ElectricCar(Car):
    """电动汽车的独特之处。"""

    def __init__(self,make,model,year):
        """
        初始化父类的属性。
        再初始化电动车特有属性
        """

        super().__init__(make,model,year)
        self.battery=Battery()

    # def describe_battery(self):
    #     """打印一条描述电瓶容量的消息"""
    #     print(f"This car has a {self.battery_size}-kWh battery.")

    def fill_gas_tank(self):
        """电动汽车没有油箱"""
        print(f"This car doesn't need a gas tank to fill it.")

my_tesla = ElectricCar('tesla','model s',2019)
print(my_tesla.get_descriptive_name())
# my_tesla.describe_battery()
my_tesla.battery.describe_battery()
my_tesla.battery.get_range()