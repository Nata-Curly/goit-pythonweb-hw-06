import argparse
from db_session import Session
from models import Teacher, Group, Student, Grade, Subject


def create_teacher(name):
    session = Session()
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    session.close()
    print(f"Teacher '{name}' created successfully.")


def list_teachers():
    session = Session()
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.name}")
    session.close()


def update_teacher(teacher_id, name):
    session = Session()
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        teacher.name = name
        session.commit()
        print(f"Teacher ID {teacher_id} updated to '{name}'.")
    else:
        print(f"Teacher ID {teacher_id} not found.")
    session.close()


def delete_teacher(teacher_id):
    session = Session()
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Teacher ID {teacher_id} deleted.")
    else:
        print(f"Teacher ID {teacher_id} not found.")
    session.close()


def create_group(name):
    session = Session()
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()
    print(f"Group '{name}' created successfully.")


def list_groups():
    session = Session()
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")
    session.close()


def update_group(group_id, name):
    session = Session()
    group = session.query(Group).get(group_id)
    if group:
        group.name = name
        session.commit()
        print(f"Group ID {group_id} updated to '{name}'.")
    else:
        print(f"Group ID {group_id} not found.")
    session.close()


def delete_group(group_id):
    session = Session()
    group = session.query(Group).get(group_id)
    if group:
        session.delete(group)
        session.commit()
        print(f"Group ID {group_id} deleted.")
    else:
        print(f"Group ID {group_id} not found.")
    session.close()


def create_student(name, group_id):
    session = Session()
    student = Student(name=name, group_id=group_id)
    session.add(student)
    session.commit()
    session.close()
    print(f"Student '{name}' added to group ID {group_id}.")


def list_students():
    session = Session()
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Group ID: {student.group_id}")
    session.close()


def update_student(student_id, name, group_id):
    session = Session()
    student = session.query(Student).get(student_id)
    if student:
        student.name = name
        student.group_id = group_id
        session.commit()
        print(f"Student ID {student_id} updated to '{name}', Group ID {group_id}.")
    else:
        print(f"Student ID {student_id} not found.")
    session.close()


def delete_student(student_id):
    session = Session()
    student = session.query(Student).get(student_id)
    if student:
        session.delete(student)
        session.commit()
        print(f"Student ID {student_id} deleted.")
    else:
        print(f"Student ID {student_id} not found.")
    session.close()


def create_subject(name, teacher_id):
    session = Session()
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()
    session.close()
    print(f"Subject '{name}' assigned to teacher ID {teacher_id}.")


def list_subjects():
    session = Session()
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(
            f"ID: {subject.id}, Name: {subject.name}, Teacher ID: {subject.teacher_id}"
        )
    session.close()


def update_subject(subject_id, name, teacher_id):
    session = Session()
    subject = session.query(Subject).get(subject_id)
    if subject:
        subject.name = name
        subject.teacher_id = teacher_id
        session.commit()
        print(f"Subject ID {subject_id} updated to '{name}', Teacher ID {teacher_id}.")
    else:
        print(f"Subject ID {subject_id} not found.")
    session.close()


def delete_subject(subject_id):
    session = Session()
    subject = session.query(Subject).get(subject_id)
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject ID {subject_id} deleted.")
    else:
        print(f"Subject ID {subject_id} not found.")
    session.close()


def create_grade(student_id, subject_id, grade, date):
    session = Session()
    grade_entry = Grade(
        student_id=student_id, subject_id=subject_id, grade=grade, date_received=date
    )
    session.add(grade_entry)
    session.commit()
    session.close()
    print(
        f"Grade {grade} added for student ID {student_id} in subject ID {subject_id} on {date}."
    )


def list_grades():
    session = Session()
    grades = session.query(Grade).all()
    for grade in grades:
        print(
            f"Student ID: {grade.student_id}, Subject ID: {grade.subject_id}, Grade: {grade.grade}, Date: {grade.date_received}"
        )
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for database operations.")
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "delete"],
        required=True,
        help="CRUD action",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Student", "Subject", "Grade"],
        required=True,
        help="Model to operate on",
    )
    parser.add_argument("-n", "--name", help="Name for creation or update")
    parser.add_argument("-id", "--id", type=int, help="ID for update or delete")
    parser.add_argument(
        "-g", "--group_id", type=int, help="Group ID for student creation or update"
    )
    parser.add_argument(
        "-t", "--teacher_id", type=int, help="Teacher ID for subject creation or update"
    )
    parser.add_argument(
        "-s", "--subject_id", type=int, help="Subject ID for grade creation"
    )
    parser.add_argument(
        "-st", "--student_id", type=int, help="Student ID for grade creation"
    )
    parser.add_argument(
        "-gr", "--grade", type=float, help="Grade value for grade creation"
    )
    parser.add_argument("-d", "--date", help="Date for grade creation")

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create":
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update":
            update_teacher(args.id, args.name)
        elif args.action == "delete":
            delete_teacher(args.id)
    elif args.model == "Group":
        if args.action == "create":
            create_group(args.name)
        elif args.action == "list":
            list_groups()
        elif args.action == "update":
            update_group(args.id, args.name)
        elif args.action == "delete":
            delete_group(args.id)
    elif args.model == "Student":
        if args.action == "create":
            create_student(args.name, args.group_id)
        elif args.action == "list":
            list_students()
        elif args.action == "update":
            update_student(args.id, args.name, args.group_id)
        elif args.action == "delete":
            delete_student(args.id)
    elif args.model == "Subject":
        if args.action == "create":
            create_subject(args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects()
        elif args.action == "update":
            update_subject(args.id, args.name, args.teacher_id)
        elif args.action == "delete":
            delete_subject(args.id)
    elif args.model == "Grade":
        if args.action == "create":
            create_grade(args.student_id, args.subject_id, args.grade, args.date)
        elif args.action == "list":
            list_grades()
