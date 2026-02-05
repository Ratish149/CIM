from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser

from .models import (
    MajorGroup,
    MinorGroup,
    Skill,
    SubMajorGroup,
    UnitGroup,
    WorkInterest,
)


class WorkInterestTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)

        # Create necessary ISCO groups
        self.major_group = MajorGroup.objects.create(code="1", title="Managers")
        self.sub_major_group = SubMajorGroup.objects.create(
            major_group=self.major_group, code="11", title="Chief Executives"
        )
        self.minor_group = MinorGroup.objects.create(
            sub_major_group=self.sub_major_group, code="111", title="Legislators"
        )
        self.unit_group = UnitGroup.objects.create(
            minor_group=self.minor_group, code="1111", title="Legislators"
        )

    def test_create_work_interest(self):
        url = reverse("job:work-interest-list")
        data = {
            "unit_group": self.unit_group.id,
            "title": "Software Developer",
            "proficiency_level": "Intermediate",
            "availability": "Full Time",
            "summary": "Experienced software developer interested in web dev.",
        }
        response = self.client.post(url, data, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkInterest.objects.count(), 1)
        self.assertEqual(WorkInterest.objects.get().title, "Software Developer")

    def test_get_work_interest_list(self):
        WorkInterest.objects.create(
            user=self.user,
            unit_group=self.unit_group,
            title="Software Developer",
            proficiency_level="Intermediate",
        )
        url = reverse("job:work-interest-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if results key is present if pagination is used
        if "results" in response.data:
            self.assertEqual(len(response.data["results"]), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_update_work_interest(self):
        interest = WorkInterest.objects.create(
            user=self.user,
            unit_group=self.unit_group,
            title="Software Developer",
            proficiency_level="Intermediate",
        )
        url = reverse("job:work-interest-detail", args=[interest.id])
        data = {"title": "Senior Software Developer"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        interest.refresh_from_db()
        self.assertEqual(interest.title, "Senior Software Developer")

    def test_delete_work_interest(self):
        interest = WorkInterest.objects.create(
            user=self.user,
            unit_group=self.unit_group,
            title="Software Developer",
            proficiency_level="Intermediate",
        )
        url = reverse("job:work-interest-detail", args=[interest.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkInterest.objects.count(), 0)


class SkillTests(APITestCase):
    def test_anonymous_create_skill(self):
        url = reverse("job:skill-list")
        data = {"name": "Python"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 1)
