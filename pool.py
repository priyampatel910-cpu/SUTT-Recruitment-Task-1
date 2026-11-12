from models import RideRequest, Cab
import heapq
from validator import DESTINATIONS, TIME_SLOTS

ALL_TRIPS = {
    (destination, time_slot)
    for destination in  DESTINATIONS
    for time_slot in TIME_SLOTS
}

class CabPool:
    def __init__(self, cabs):
        self.cabs = list(cabs)
        self.queues = {
            trip: [] for trip in ALL_TRIPS
        }
        self.next_request_id = 1
        
    def add_new_request(self, name, destination, time_slot, year):
        new_request = RideRequest(self.next_request_id, name, destination, time_slot, year)
        self.next_request_id+=1
        trip = new_request.trip

        priority_entry = (
            -new_request.year,
            new_request.request_id,
            new_request
        )

        heapq.heappush(
            self.queues[trip],
            priority_entry
        )

        return new_request

    def waiting_list_copy(self, trip):   
        sorted_entries = sorted(self.queues[trip])
        ordered_students = [entry[2] for entry in sorted_entries]
        return ordered_students

    def queue_size(self, trip):
        return len(self.queues[trip])

    def first_open_cab(self, trip):
        for cab in self.cabs:
            if cab.trip == trip and cab.is_open:
                return cab
        return None

    def take_from_queue(self, trip, number_of_students):
        students_to_board = []

        while(len(students_to_board) < number_of_students and len(self.queues[trip]) > 0):
            highest_priority_entry = heapq.heappop(self.queues[trip])

            student_request = highest_priority_entry[2]

            students_to_board.append(student_request)

        return students_to_board

    def send_off(self, cab):

        students = self.take_from_queue(cab.trip, cab.seats)
        if not students:
            return []

        cab.board_and_leave(students)

        return students

    def dispatch(self, trip):
        cab = self.first_open_cab(trip)

        if cab is None or self.queue_size(trip) == 0:
            return None
        
        students = self.send_off(cab)
        if not students:
            return None

        return cab, students
        


    def preview_matches(self):
        claimed_count = {}
        preview_results = []

        for cab in self.cabs:
            if not cab.is_open:
                continue

            trip = cab.trip

            ordered_student_list = self.waiting_list_copy(trip)

            start_idx = claimed_count.get(trip, 0)
            end_idx = start_idx + cab.seats

            cab_passengers = ordered_student_list[start_idx:end_idx]

            claimed_count[trip] = (start_idx + len(cab_passengers))

            preview_results.append(
                (cab, cab_passengers)
            )
        
        waitlist_by_trip = {}

        for trip in ALL_TRIPS:
            actual_waiting_count = self.queue_size(trip)
            preview_passenger_count = claimed_count.get(trip, 0)
            waitlist_by_trip[trip] = actual_waiting_count - preview_passenger_count

        return preview_results, waitlist_by_trip

