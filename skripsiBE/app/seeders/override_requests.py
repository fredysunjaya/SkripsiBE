from faker import Faker
from skripsiBE.app.models.override_requests import OverrideRequest
from datetime import timedelta


def OverrideRequestSeeder():
    fake = Faker("id_ID")
    status = {
        "requested": "Requested",
        "approved": "Approved",
        "rejected": "Rejected",
        "cancelled": "Cancelled",
    }

    for i in range(60):
        initial_date_time = fake.unique.date_time_between(
            start_date="-60d", end_date="now"
        )

        OverrideRequest.objects.create(
            user_id=1,
            group_id=1,
            supervisor_id=fake.random_int(min=1, max=20),
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
