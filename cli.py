from validator import *

def add_request_flow(pool):

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

        new_request = pool.add_request(
            answers[0],
            answers[1],
            answers[2],
            answers[3]
        )

        print(f"Added: {new_request}")

        if pool.first_open_cab(new_request.trip) is None:
            print("No open cab available for this trip. You have been added to the waiting list")

def show_everythin(pool):
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

        for position, students in enumerate(waiting_students, start = 1):
            print(f"{position}. {student}")
    
    if not someone_waiting:
        print("Nobody is waiting.")

    print("\n========== CABS ==========")
    if len(pool.cabs) == 0:
        print("No cabs right now.")

    for cab in pool.cabs:
        print(cab)

        if cab.has_left:
            print("Passengers:")

            for passenger in cab.passengers:
                print(f"-  {passenger.name}")
    
    dispatch_result = pool.dispatch(trip)

    if dispatch_result is None:
        print("Dispatch could not be completed.")
        return

    departed_cab, boarded_students = dispatch_result

    print("\nCab dispatched!")
    print(departed_cab)

    print("Students who boarded:")

    for student in boarded_students:
        print(f"- {student.name}")

    print(f"{pool.queue_size{trip}} students are still waiting for this trip.")