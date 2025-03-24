import random
from faker import Faker
from models import Student, Group, Teacher, Subject, Grade
from db_session import Session

fake = Faker()


def seed_database():
    with Session() as session:
        session.query(Grade).delete()
        session.query(Subject).delete()
        session.query(Student).delete()
        session.query(Group).delete()
        session.query(Teacher).delete()
        session.commit()

        groups = [Group(name=f"Group {i+1}") for i in range(3)]
        session.add_all(groups)
        session.commit()
        groups_ids = [g.id for g in groups]  
        teachers = [Teacher(name=fake.name()) for _ in range(5)]
        session.add_all(teachers)
        session.commit()
        teachers_ids = [t.id for t in teachers]  

        subjects = [
            Subject(
                name=fake.word().capitalize(),
                teacher_id=teachers_ids[i % len(teachers_ids)],
            )
            for i in range(5)
        ]
        session.add_all(subjects)
        session.commit()
        subjects_ids = [s.id for s in subjects]  

        students = [
            Student(name=fake.name(), group_id=random.choice(groups_ids))
            for _ in range(42)
        ]
        session.add_all(students)
        session.commit()
        students_ids = [s.id for s in students]  
        grades = []
        for student_id in students_ids:
            for subject_id in subjects_ids:
                for _ in range(random.randint(5, 20)):
                    grades.append(
                        Grade(
                            student_id=student_id,
                            subject_id=subject_id,
                            grade=random.randint(60, 100),
                            date_received=fake.date_between(
                                start_date="-1y", end_date="today"
                            ),
                        )
                    )
        session.add_all(grades)
        session.commit()

        print("Database seeded successfully!")
        print(f"Teachers: {session.query(Teacher).count()}")
        print(f"Groups: {session.query(Group).count()}")
        print(f"Subjects: {session.query(Subject).count()}")
        print(f"Students: {session.query(Student).count()}")
        print(f"Grades: {session.query(Grade).count()}")


if __name__ == "__main__":
    seed_database()
