from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .views import ProblemList, ProblemDetail
from ..models import Problem, Tag, Language


class TestProblemAPI(APITestCase):
    tags = ["tag1", "tag2"]
    languages = ["C", "C++", "Java", "Python"]

    def setUp(self):
        self.client = APIClient()
        # Create tags
        for tag in self.tags:
            Tag.objects.create(name=tag)
        # Create languages
        for language in self.languages:
            Language.objects.create(name=language)
        # Create problems
        for i in range(1, 4):
            p = Problem.objects.create(
                title="test" + str(i),
                difficulty=["E", "M", "H"][i - 1],
                statement=SimpleUploadedFile(
                    name=f"test{str(i)}.txt", content=b"test content"
                ),
                slug=f"test{str(i)}",
            )
            p.tags.set(Tag.objects.all())

    def test_get_problem_list(self):
        response = self.client.get("/api/problems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        for problem in response.data:
            self.assertEqual(problem["title"], "test" + str(problem["id"]))
            self.assertEqual(problem["difficulty"], ["E", "M", "H"][problem["id"] - 1])
            self.assertEqual(problem["language"], self.languages[problem["id"] - 1])
            self.assertEqual(problem["tags"], [{"name": "tag1"}, {"name": "tag2"}])
            self.assertEqual(problem["statement"], "/problems/test.txt")
            self.assertEqual(problem["solution"], None)
            self.assertEqual(problem["test_cases"], [])
            self.assertEqual(problem["discussions"], [])
            self.assertEqual(problem["is_solved"], False)

    def test_url_resolves_to_correct_view(self):
        found = resolve("/api/problems/")
        self.assertEqual(found.func.view_class, ProblemList)
        found = resolve("/api/problems/1/")
        self.assertEqual(found.func.view_class, ProblemDetail)

    def test_get_problem_detail(self):
        response = self.client.get("/api/problems/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_problem(self):
        response = self.client.post(
            "/api/problems/",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_problem(self):
        response = self.client.put(
            "/api/problems/1/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED or status.HTTP_401_UNAUTHORIZED,
        )

    def test_delete_problem(self):
        response = self.client.delete(
            "/api/problems/1/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED or status.HTTP_401_UNAUTHORIZED,
        )
