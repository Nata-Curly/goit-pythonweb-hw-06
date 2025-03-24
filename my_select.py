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


if __name__ == "__main__":
    print(select_1(), '\n------')
    print(
        select_2(2), "\n------"
    )
    print(select_3(3), "\n------")
    print(select_4(), "\n------")
    print(select_5(3), "\n------")
    print(
        select_10(5, 1), "\n------"
    )
    print(select_6(2), "\n------")
    print(select_7(2, 3), "\n------")
    print(select_8(1), "\n------")
    print(select_9(5), "\n------")
    print(select_10(5, 1), "\n------")

