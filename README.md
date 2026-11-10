
# Cab Pool Matcher

  

A cli made in Python that groups student ride requests by destination and time slot, prioritizes senior students, and assigns waiting students to available cabs.

  

## Requirements

  

- Python 3.10 or newer

- No third-party packages are required. The application uses Python's standard library.

  

## Run the application

  

Clone or download the repository, open a terminal in the project directory, and run:

  

```bash

python main.py

```

  

The application loads its initial cab list from `data/cabs.csv`.

  

## How it works

  

A trip is identified by the pair `(destination, time_slot)`. The supported destinations are Delhi and Jaipur. The supported time slots are Morning, Afternoon, Evening, and Night, giving eight possible trip queues.

  

The application separates three operations:

  

1.  **Add request:** validates the student's details and adds the request to the waiting queue for that trip. A request is accepted even when no open cab currently exists.

2.  **Find Matches:** performs a read-only preview of which waiting students would fit into each open cab if the cabs left now. It does not remove requests or change cab status.

3.  **Dispatch Cab:** performs the real assignment. It selects the first open cab for the trip in CSV order, boards the highest-priority waiting students up to the cab's capacity, and marks the cab as departed.

  

## Student priority

  

Each trip has its own priority queue, implemented with Python's `heapq`.

  

A request is stored as:

  

```python

(-year, request_id, request)

```

  

Python's heap sorts in ascending order, so the negative academic year makes a 5th-year student rank ahead of a 4th-year student, and so on. When two students are in the same year, the smaller request ID wins. Request IDs are assigned by an increasing counter (*No two applicants will have same request IDs*), so they provide a reliable tie breaker even if two timestamps are identical.

  

## Cab CSV format

  

`data/cabs.csv` must contain these columns:

  

| Column | Meaning | Accepted values |

|---|---|---|

| `driver_name` | Driver's name | Non-empty text |

| `seats` | Cab capacity | Integer from 1 to 4 |

| `destination` | Trip destination | `Delhi` or `Jaipur` |

| `time_slot` | Departure time slot | `Morning`, `Afternoon`, `Evening`, or `Night` |

  

Invalid rows are skipped with a warning. The cab list remains a list, rather than a set, so cabs are always processed in their original CSV order.

  

## Menu

  

| Option | Action |

|---|---|

| 1 | Add a student request |

| 2 | View waiting students and cab status |

| 3 | Preview matches without changing data |

| 4 | Dispatch the first available cab for a trip |

| 5 | Save and quit |

  

At prompts, type `cancel` to cancel the current add-request or dispatch flow.

  

## Code design decisions

  

-  **Tuple trip keys:**  `(destination, time_slot)` is a tuple that can't be changed in the entire runtime and can be used as a dictionary key. This keeps one queue per trip.

-  **Priority queue:**  `heapq` provides efficient insertion and removal of the highest-priority request.

-  **Request counter:** request IDs define arrival order. A timestamp is also stored for display, but timestamps are not used to break ties.

-  **CSV order:** cabs are kept in a list and scanned in file order. This makes the selected cab deterministic.

-  **Read only preview:** Find Matches sorts copies of waiting queues and tracks preview allocations separately. The actual queues and cabs are untouched.

-  **Separation of responsibilities:**  `pool.py` contains matching and dispatch logic; `cli.py` handles terminal input and output; `storage.py` handles files (*This separation of different responsibilities was suggested by Claude, more on that in AI usage section*).

  

  

CSV is used for the initial flat cab table.

  

## Tricky situations

  

-  **Partially filled cab:** if fewer students are waiting than the cab has seats, the application asks for confirmation. If confirmed, the waiting students board and the cab is permanently marked as departed. Unused seats remain empty. If declined, nothing changes.

-  **No open cab:** a new request is still accepted and remains in its trip's waiting queue. Dispatch reports that no open cab is available and changes nothing.

-  **Same academic year:** the smaller request ID boards first, preserving request arrival order.



## Complexity

  

Let `n` be the number of waiting students for a trip and `C` be the total number of cabs.

  

| Operation | Complexity | Explanation |

|---|---:|---|

| Add request | `O(log n)` | One heap insertion |

| Find first open cab | `O(C)` | Scan cabs in CSV order |

| Dispatch | `O(C + log n)` | Find a cab and remove at most four requests |

| Find Matches | `O(n log n)` per relevant trip | Sort a copy of a waiting queue for preview |

  

The cab capacity is at most four, so dispatch removes at most four heap entries. Treating four as a constant keeps the removal work `O(log n)`.

  

## Project structure

  

```

cab-pool-matcher/

   main.py  (Entry point and startup)

   models.py   (RideRequest and Cab classes)

   pool.py   (Priority queues, preview, and dispatch, main algorithmic part of the project)

   validation.py   (Input data validation)

   storage.py   (CSV loading and, in future, JSON persistance)

   cli.py  (Menu, answer handling, and display)

   cabs.csv  (cab data)

   requirements.txt

   README.md

```

## A Note about AI usage

I used Claude, in order to learn how to make an efficient CLI interface, with Claude recommending me validation checks, as every input would be plain text. Claude also helped me generate the structure of the project, also explaining how different files can be used for their tasks, which helps in debugging a single code file without modifying others. 

I also used Claude to understand and implement CSV into my project, as I had very little knowledge of what CSV was.

I used Claude to determine and validate the time complexity of the program in tricky cases (like time complexity of finding matches program or dispatch method)

Lastly, I used Gemini to help me debug some of the complicated part of `pool.py`,  where I found out one of the errors was due to indentation error.

 
  

## Possible future improvements

  

- Add more destinations and time slots through configuration.


- Add data persistance by using JSON

- Add a feature for a request to be cancelled by the student.


(*Note: There may still be some underlying errors or bugs in my code, so if you find something like that, do let me know.*)