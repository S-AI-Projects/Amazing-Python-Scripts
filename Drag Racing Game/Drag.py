import time


# Car simulation model
# Representative race result for Car with top speed 200 and acceleration 20:
# The car accelerates by 20 in gear 1 until speed reaches 160 at step 8.
# At 160 speed it shifts to gear 2. In step 9 speed reaches 200 and the race finishes.


class Car:
    def __init__(self, name, top_speed, acceleration):
        self.name = name
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.current_speed = 0
        self.gear = 1

    def accelerate(self):
        if self.gear == 1:
            rpm = self.current_speed / self.top_speed
        else:
            rpm = self.current_speed / (self.top_speed * (self.gear - 1))
        self.current_speed += self.acceleration * self.gear
        print(
            f"{self.name}: {self.current_speed:.2f} km/h (Gear: {self.gear}, RPM: {rpm:.2f})")

    def shift_gear(self):
        if self.gear < 5:
            self.gear += 1

    def race(self):
        print(f"{self.name} is racing!")
        while self.current_speed < self.top_speed:
            time.sleep(0.5)
            self.accelerate()
            if self.current_speed >= self.top_speed * 0.8:
                self.shift_gear()


if __name__ == "__main__":
    car1 = Car("Player Car", top_speed=200, acceleration=20)
    car2 = Car("AI Car", top_speed=180, acceleration=18)

    car1.race()
    print("\n")
    car2.race()
