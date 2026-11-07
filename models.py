from datetime import datetime

class RideRequest:
    def __init__(self, request_id, name, destination, time_slot, year, submitted_at = None):

        self.request_id = request_id
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year

        self.submitted_at = datetime.now()

    @property
    def trip(self):
        return (self.destination, self.time_slot)

    def __str__(self):
        return(
            f"#{self.request_id} {self.name}"
            f"({self.year}th year)"
            f"{self.destination}, {self.time_slot}"
        )

class Cab:
    def __init__(self, driver_name, seats, destination, time_slot):
        self.driver_name = driver_name
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []

        @property
        def is_open(self):
            return not self.has_left

        @property
        def trip(self):
            return (self.destination, self.time_slot)

        @property
        def seats_taken(self):
            return len(self.passengers)

        def board_and_leave(self, students):
            if self.has_left:
                raise ValueError("This cab is already left.")

            if len(students) > self.seats:
                raise ValueError("More students assigned than available seats.")

            self.passengers = students
            self.has_left = True

        def __str__():
            status = "LEFT" if self.has_left else "OPEN"

            return (
                f"{self.driver_name} | {self.destination} {self.time_slot} | {self.seats_taken}/{self.seats} | {status}"
            )
