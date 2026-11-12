from validator import *
from pool import ALL_TRIPS

def ask_user(question, parser):
    while True:
        try:
            user_input = input(question)

        except(KeyboardInterrupt):
            raise        

        if user_input.strip().lower() == "cancel":
            return None

        try:
            valideted_value = parser(user_input)
            return valideted_value

        except ValueError as error:
            print(error)

def add_request_cli(pool):

    questions = [
        ("Name: ", parse_name),
        ("Destination: ", parse_destination),
        ("Time slot: ", parse_timeslot),
        ("Year (1-5): ", parse_year)
    ]

    answers = []
    
    for question, parser in questions:

        answer = ask_user(question, parser)

        if answer is None:
            print("Request cancelled.")
            return

        answers.append(answer)

    new_request = pool.add_new_request(
        answers[0],
        answers[1],
        answers[2],
        answers[3]
    )

    print(f"Added: {new_request}")

    if pool.first_open_cab(new_request.trip) is None:
        print("No open cab available for this trip. You have been added to the waiting list")

def show_everything(pool):
    print("\n-=-=-=-=- WAITING -=-=-=-=-")
    someone_waiting = False

    for trip in ALL_TRIPS:
        waiting_students = pool.waiting_list_copy(trip)

        if len(waiting_students) == 0:
            continue

        someone_waiting = True

        destination, time_slot = trip

        print(
            f"\n{destination} {time_slot}"
            f"({len(waiting_students)} waiting)."
        )

        for position, student in enumerate(waiting_students, start = 1):
            print(f"{position}. {student}")
    
    if not someone_waiting:
        print("Nobody is waiting.")

    print("\n-=-=-=-=- CABS -=-=-=-=-")
    if len(pool.cabs) == 0:
        print("No cabs right now.")

    for cab in pool.cabs:
        print(cab)

        if cab.has_left:
            print("Passengers:")

            for passenger in cab.passengers:
                print(f"-  {passenger.name}")

def ordinal(number):
    if 10 <= number%100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(number%10, "th")
    
def find_matches_cli(pool):
    preview_results, remaining_waiting = pool.preview_matches()

    print("\n-=-=-=-=- Match Preview -=-=-=-=-")

    if not preview_results:
        print("There are no open cabs.")

    else:
        for cab, students in preview_results:
            print(f"\n{cab.driver_name} | {cab.destination} {cab.time_slot}")

            if not students:
                print("No students waiting for this cab.")
                continue

            for position, student in enumerate(students, start=1):
                print(f"  {position}. {student.name} ({student.year}{ordinal(student.year)}) year")

            empty_seats = cab.seats - len(students)

            if empty_seats:
                print(f"{empty_seats} seats would remain empty.")

    print("\n-=-=-=-=- Still Waiting for cabs -=-=-=-=-")

    for trip in ALL_TRIPS:
        waiting_count = remaining_waiting[trip]
        if waiting_count == 0:
            continue

        destination, time_slot = trip

        if pool.first_open_cab is None:
            status="no open cab"

        else:
            status="open cabs exist, but are full (in preview)"

        print(f"{destination} {time_slot}: {waiting_count} students, {status}")

    print("\nThis is a preview only, no cabs were added or removed from the csv file")


def dispatch_cli(pool):
    destination = ask_user("Destination(Jaipur/Delhi) : ", parse_destination)
    if destination is None:
        print("Dispatch cancelled.")
        return

    time_slot = ask_user("Time slot (Morning/Afternoon/Evening/Night): ", parse_timeslot)
    if time_slot is None:
        print("Dispatch cancelled"); return

    trip = (destination, time_slot)
    cab = pool.first_open_cab(trip)

    if cab is None:
        print("No cabs available for this trip.")
        return

    waiting_count = pool.queue_size(trip)
    if waiting_count == 0:
        print("Nobody is waiting for this trip.")
        return

    boarding_count = min(cab.seats, waiting_count)

    if boarding_count < cab.seats:
        answer = input(
            f"Only {boarding_count} of {cab.seats} will be filled. "
            "Send this cab anyway? (y/n): "
        ).strip().casefold()

        if answer not in ("y", "yes"):
            print("Dispatched cancelled.")
            return

        dispatch_result = pool.dispatch(trip)
        if dispatch_result is None:
            print("Disptach could not be completed.")
            return

        departed_cab, boarded_students = dispatch_result

        print("\n Cab successfully dispatched.")
        print(departed_cab)
        print("Students who boarded:")
        for student in boarded_students:
            print(f"   -{student.name} (request #{student.request_id})")

        print(f"{pool.queue_size(trip)} students remain waiting for this trip.")

def run_menu(pool):
    
    while True:
        print("\n========== CAB POOL MATCHER ==========")
        print("1. Add request")
        print("2. View waiting students and cabs")
        print("3. Find Matches (read-only preview)")
        print("4. Dispatch Cab")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "5":
            print("Exiting. Goodbye!")
            return

        if choice == "1":
            add_request_cli(pool)

        if choice == "2":
            show_everything(pool)

        if choice == "3":
            find_matches_cli(pool)

        if choice == "4":
            dispatch_cli(pool)

        else:
            print("Please enter a number from 1 to 5.")
            continue
