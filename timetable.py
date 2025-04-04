from prettytable import PrettyTable
import random

# Base class to represent a database relation/table
class Relation:
    def __init__(self, name, *fields):
        self.name = name        # Name of the relation (e.g., 'courses', 'batches')
        self.fields = fields    # Column names for the relation
        self.data = []          # List to store actual data records


# Container class to hold multiple relations, allowing attribute-style access
class Relations:
    def __init__(self, *relations):
        # For each relation passed, create an attribute with the relation's name
        # This allows accessing relations like: db.courses, db.batches, etc.
        for relation in relations:
            setattr(self, relation.name, relation)


# Initialize the database schema with four relations
db = Relations(
    Relation('courses', 'name', 'faculty', 'frequency'),    # Stores course details
    Relation('batches', 'name'),                           # Stores batch names
    Relation('time_slots', 'day', 'time'),                 # Stores available time slots
    Relation('schedule', 'batch', 'day', 'time', 'course') # Stores final timetable
)


def inputfunction():
    """
    Collects input from the user about courses, faculties, and batches.
    Validates faculty assignments and course frequencies.
    """
    # Get basic input data as comma-separated values
    course_names = input("Enter courses (comma separated): ").split(",")
    faculty_names = [faculty.strip() for faculty in input("Enter faculties (comma separated): ").split(",")]
    batch_names = input("Enter batches (comma separated): ").split(",")


    # For each course, collect and validate faculty assignment and weekly frequency
    print("\nAssign faculties and frequencies to courses:")
    for course_name in course_names:
        course_name = course_name.strip()
       
        # Ensure faculty exists in the provided faculty list
        faculty = input(f"Enter faculty for {course_name}: ").strip()
        while faculty not in faculty_names:
            print(f"Faculty '{faculty}' not found. Try again.")
            faculty = input(f"Enter faculty for {course_name}: ").strip()


        # Ensure frequency is between 1-5 classes per week
        frequency = int(input(f"How many times should {course_name} be scheduled per week (1-5)? ").strip())
        while frequency < 1 or frequency > 5:
            print("Frequency must be between 1 and 5.")
            frequency = int(input(f"How many times should {course_name} be scheduled per week (1-5)? ").strip())


        # Store course information
        db.courses.data.append({'name': course_name, 'faculty': faculty, 'frequency': frequency})


    # Store batch names
    for batch_name in batch_names:
        db.batches.data.append({'name': batch_name.strip()})


def generate_timetable():
    """
    Generates a weekly timetable by:
    1. Creating all possible time slots
    2. For each batch and course combination:
       - Randomly selects time slots
       - Ensures no scheduling conflicts
       - Meets the required course frequency
    """
    # Define available days and time slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM']


    # Generate all possible time slots combinations
    for day in days:
        for time in times:
            db.time_slots.data.append({'day': day, 'time': time})


    # Schedule courses for each batch
    for batch in db.batches.data:
        for course in db.courses.data:
            scheduled_slots = 0
            # Create a shuffled copy of time slots for random allocation
            time_slots = db.time_slots.data.copy()
            random.shuffle(time_slots)


            # Try to schedule the required number of classes
            for time_slot in time_slots:
                if scheduled_slots >= course['frequency']:
                    break


                # Check if the time slot is free for this batch
                if not any(s['batch'] == batch['name'] and
                         s['day'] == time_slot['day'] and
                         s['time'] == time_slot['time']
                         for s in db.schedule.data):
                    # Schedule the course
                    db.schedule.data.append({
                        'batch': batch['name'],
                        'day': time_slot['day'],
                        'time': time_slot['time'],
                        'course': course['name']
                    })
                    scheduled_slots += 1


def print_timetable():


    #Prints the generated timetable using PrettyTable for formatting.
    #This function will create a separate table for each batch displaying their weekly schedule.


    print("\nGenerated Weekly Timetable:")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM']


    # Generate timetable for each batch
    for batch in db.batches.data:
        print(f"\nBatch: {batch['name']}")
        table = PrettyTable()
        table.field_names = ["Time Slot"] + days


        # Fill in the timetable row by row
        for time in times:
            row = [time]
            for day in days:
                # Find if there's a scheduled course for this slot
                scheduled = next((s for s in db.schedule.data
                                if s['batch'] == batch['name']
                                and s['day'] == day
                                and s['time'] == time), None)
                if scheduled:
                    # If slot is scheduled, show course and faculty
                    course = next(c for c in db.courses.data if c['name'] == scheduled['course'])
                    cell_content = f"{course['name']}\n({course['faculty']})"
                else:
                    # If slot is free, mark it as "Free"
                    cell_content = "Free"
                row.append(cell_content)
            table.add_row(row)


        # Center-align all columns and print the table
        table.align = "c"
        print(table)


# Execution
inputfunction()
generate_timetable()
print_timetable()
