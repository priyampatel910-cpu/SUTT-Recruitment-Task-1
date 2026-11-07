from .models import RideRequest, Cab

ALL_TRIPS = {
    ("Delhi", "Morning"),
    ("Delhi", "Afternoon"),
    ("Delhi", "Evening"),
    ("Delhi", "Night"),
    ("Jaipur", "Morning"),
    ("Jaipur", "Afternoon"),
    ("Jaipur", "Evening"),
    ("Jaipur", "Night")
}

class CabPool:
    def __init__(self, cabs):
        self.cabs = cabs
        self.queues = {
            trip: [] for trip in ALL_TRIPS
        }
        self.next_request_id = 1
        
    def add_new_request(self, name, destination, time_slot, year):
        new_request = RideRequest(self.next_request_id, name, destination, time_slot, year)
        self.next_request_id+=1
        trip = new_request.trip

        self.queues[trip].append(new_request)

        return new_request

    def waiting_list_copy(self, trip):
        return self.queues[trip].copy()

    def queue_size(self, trip):
        return len(self.queues[trip])

    def first_open_cab(self, trip):
        for cab in self.cabs:
            if cab.trip == trip and cab.is_open:
                return cab
        return None

    def take_from_queue(self, trip, number_of_students):
        waiting_students = self.queues[trip]
        students_to_board = waiting_students[:number_of_students]
        self.queues[trip] = waiting_students[number_of_students:]

        return students_to_board

    def send_off(self, cab):

        students = self.take_from_queue(cab.trip, cab.seats)

        cab.board_and_leave(students)

        return students