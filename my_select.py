from decimal import Decimal
import logging
from sqlalchemy import func
from db_session import Session
from models import Student, Grade, Subject, Group, Teacher


logging.basicConfig(level=logging.WARNING)


def start_session():
    try:
        return Session()
    except Exception as e:
        logging.error("Failed to start session: %s", e)
        raise


def round_results(results):
    return [
        (
            (group, round(float(grade), 2))
            if isinstance(grade, Decimal)
            else (group, grade)
        )
        for group, grade in results
    ]


def select_1():
    session = start_session()
    res = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    session.close()
    return round_results(res)


def select_2(subject_id):
    session = start_session()
    res = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    session.close()
    return round_results([res])


def select_3(subject_id):
    session = start_session()
    res = (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(func.avg(Grade.grade).desc())
        .all()
    )
    session.close()
    return round_results(res)


def select_4():
    session = start_session()
    res = session.query(func.avg(Grade.grade).label("overall_average")).all()
    session.close()
    return res


def select_5(teacher_id):
    session = start_session()
    res = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    session.close()
    return res


def select_6(group_id):
    session = start_session()
    res = session.query(Student.name).join(Group).filter(Group.id == group_id).all()
    session.close()
    return res


def select_7(group_id, subject_id):
    session = start_session()
    res = (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .filter(Group.id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    session.close()
    return round_results(res)


def select_8(teacher_id):
    session = start_session()
    res = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    session.close()
    return res


def select_9(student_id):
    session = start_session()
    res = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .all()
    )
    session.close()
    return res


def select_10(student_id, teacher_id):
    session = start_session()
    res = (
        session.query(Subject.name)
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
        .all()
    )
    session.close()
    return res


def average_grade_for_student_by_teacher(student_id, teacher_id):
    session = start_session()
    res = (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Teacher.id == teacher_id)
        .all()
    )
    session.close()
    return res


def grades_last_class_for_group_and_subject(group_id, subject_id):
    session = start_session()

    last_class = (
        session.query(func.max(Grade.date_received))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )

    if not last_class:
        session.close()
        return []
    res = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == last_class,
        )
        .all()
    )
    session.close()
    return res


def print_results(title, results):
    print(f"\n{'*'*3} {title} {'*'*3}")
    if not results:
        print("No results found.")
    else:
        for idx, result in enumerate(results, 1):
            if len(result) > 1:
                print(f"{idx}. {result[0]}: {result[1]}")
            else:
                print(f"{idx}. {result[0]}")


if __name__ == "__main__":
    print_results("Top 5 Students with Highest Average Grade", select_1())
    print_results("Top Student with Highest Average Grade in Subject", select_2(2))
    print_results("Average Grades by Group for Subject", select_3(3))
    result = select_4()
    print(f"\n{'*'*3} Overall Average Grade {'*'*3}")
    print(f"Overall Average Grade: {round(float(result[0][0]), 2)}")
    print_results("Courses Taught by Teacher", select_5(3))
    print_results("Students in Group", select_6(2))
    print_results("Grades of Students in Group for Subject", select_7(2, 3))
    result = select_8(1)
    print(f"\n{'*'*3} Average Grade Given by Teacher {'*'*3}")
    print(f"Average Grade: {round(float(result[0][0]), 2)}")
    print_results("Courses Taken by Student", select_9(5))
    print_results("Courses Taken by Student with Teacher", select_10(5, 1))

    result = average_grade_for_student_by_teacher(2, 3)
    print(f"\n{'*'*3} Average Grade for Student by Teacher {'*'*3}")
    print(f"Average Grade: {round(float(result[0][0]), 2)}")

    print_results(
        "Grades in last class for Group", grades_last_class_for_group_and_subject(1, 3)
    )
