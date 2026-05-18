from faker import Faker
from skripsiBE.app.models.leave_requests import LeaveRequest
from datetime import timedelta


def LeaveRequestSeeder():
    fake = Faker("id_ID")
    status = {
        "requested": "Requested",
        "approved": "Approved",
        "rejected": "Rejected",
        "cancelled": "Cancelled",
    }

    # for i in range(60):
    #     initial_date_time = fake.unique.date_time_between(
    #         start_date="-60d", end_date="now"
    #     )

    #     LeaveRequest.objects.create(
    #         user_id=1,
    #         group_id=1,
    #         supervisor_id=fake.random_int(min=1, max=20),
    #         attendance_type_id=fake.random_element(
    #             elements=(
    #                 1,
    #                 2,
    #                 3,
    #                 4,
    #                 5,
    #                 16,
    #                 17,
    #                 18,
    #                 19,
    #                 20,
    #                 31,
    #                 32,
    #                 33,
    #                 34,
    #                 35,
    #                 131,
    #                 132,
    #                 133,
    #                 134,
    #                 135,
    #             )
    #         ),
    #         start_date_time=initial_date_time,
    #         end_date_time=initial_date_time
    #         + timedelta(hours=fake.random_int(min=1, max=6)),
    #         status=fake.random_element(
    #             elements=("requested", "approved", "rejected", "cancelled")
    #         ),
    #         reason=fake.sentence(nb_words=10),
    #         created_at=initial_date_time
    #         + timedelta(days=fake.random_int(min=1, max=7)),
    #     )

    for i in range(60):
        initial_date_time = fake.unique.date_time_between(
            start_date="-60d", end_date="now"
        )

        LeaveRequest.objects.create(
            user_id=fake.random_int(min=1, max=20),
            group_id=1,
            supervisor_id=1,
            attendance_type_id=fake.random_element(
                elements=(
                    1,
                    2,
                    3,
                    4,
                    5,
                    16,
                    17,
                    18,
                    19,
                    20,
                    31,
                    32,
                    33,
                    34,
                    35,
                    131,
                    132,
                    133,
                    134,
                    135,
                )
            ),
            start_date_time=initial_date_time,
            end_date_time=initial_date_time
            + timedelta(hours=fake.random_int(min=1, max=6)),
            status=fake.random_element(
                elements=("requested", "approved", "rejected", "cancelled")
            ),
            reason=fake.sentence(nb_words=10),
            created_at=initial_date_time
            + timedelta(days=fake.random_int(min=1, max=7)),
        )
