import json
from typing import Any

from celery import shared_task
from rest_framework import serializers

from modules import coderunner
from problems.models import Problem
from users.tasks import send_email_task
from .models import Submission, SubmissionAnalytics


class SubmissionRunResultSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    submission = serializers.IntegerField()
    error = serializers.BooleanField()
    time = serializers.FloatField()
    memory = serializers.IntegerField()
    status = serializers.CharField()
    message = serializers.CharField()


@shared_task
def task_after_submission(
    analytics_id: int,
    request: None = None,
    serialized: bool = True,
    email=True,
) -> Submission | None | Any:
    """
    Celery task to pass a submission to the coderunner service.
    :param serialized:
    :type serialized:
    :param request:
    :type request:
    :param submission:
    :type submission:
    """
    print(analytics_id)
    print(SubmissionAnalytics.objects.get(pk=analytics_id))
    # print(analytics, analytics.submission)
    analytics = SubmissionAnalytics.objects.get(pk=analytics_id)
    submission = analytics.submission

    print("context: ", submission, analytics)

    # set status to RUNNING
    analytics.status = SubmissionAnalytics.Status.RUNNING
    analytics.save()

    problem = Problem.objects.get(pk=submission.problem.pk)
    testcases = problem.testcases.filter(language=submission.language)

    total_testcases = testcases.count()
    try:
        outputs = coderunner.run(
            code=submission.code.open("r").read(),
            language=submission.language.name,
            testcases=[
                coderunner.CodeRunnerTestCase(
                    input=testcase.input,
                    runtime=testcase.runtime,
                    memory=testcase.memory,
                )
                for testcase in testcases
            ],
        )

        avg_time = 0
        passed_testcases = 0
        error = ""
        print("ALL: ", outputs)
        for output, testcase in zip(outputs, testcases):
            avg_time += float(output.duration)

            if output.is_timeout:
                analytics.status = SubmissionAnalytics.Status.TIME_LIMIT_EXCEEDED
                analytics.save()
                error = "Time Limit Exceeded"
                break

            if output.is_error:
                analytics.status = SubmissionAnalytics.Status.RUNTIME_ERROR
                analytics.save()
                error = output.stderr.decode("utf-8")
                break

            # if output.is_memory_limit:
            #     analytics.status = SubmissionAnalytics.Status.MEMORY_LIMIT_EXCEEDED
            #     analytics.save()
            #     error = "Memory Limit Exceeded"
            #     break
            if output.stdout.decode("utf-8").strip() != "\n".join(
                map(str, testcase.output)
            ):
                print("WRONG ANSWER")
                print("OUTPUT: ", output.stdout.decode("utf-8").strip())
                print("TESTCASE: ", "\n".join(map(str, testcase.output)))
                analytics.status = SubmissionAnalytics.Status.WRONG_ANSWER
                analytics.save()
                youroutput = output.stdout.decode("utf-8").strip()
                exptected = "\n".join(map(str, testcase.output))
                error = f"Wrong Answer: {youroutput}, Expected: {exptected}, Testcase: {testcase.id}"
            else:
                passed_testcases += 1

        is_accepted = passed_testcases == total_testcases
        if is_accepted:
            analytics.status = SubmissionAnalytics.Status.ACCEPTED

        analytics.save()
        analytics.runtime = avg_time / total_testcases
        analytics.result = json.dumps(
            {
                "passed": passed_testcases,
                "total": total_testcases,
                "error": error,
            }
        )
        analytics.save()

        print("submission: ", submission)
        print("error: ", error)
        print("status: ", analytics.status.name)
        print("runtime: ", avg_time)
        print(
            "message: ",
            len(error) > 0
            and error
            or f"{passed_testcases}/{total_testcases} testcases passed",
        )
        print("context: ", request)

        obj = SubmissionRunResultSerializer(
            data={
                "submission": submission.id,
                "error": len(error) > 0,
                "time": avg_time,
                "memory": 0,
                "status": analytics.status.name,
                "message": len(error) > 0
                and error
                or f"{passed_testcases}/{total_testcases} testcases passed",
            },
            context={"request": request},
        )
        obj.is_valid()
        obj = obj.data

        if email:
            send_email_task.delay(
                email=submission.user.email,
                subject=f"{analytics.status.name} - {submission.problem.title}",
                message=f"{obj['message']}\n\n{obj['status']}",
            )

        if request and serialized:
            return obj
        if request and not serialized:
            return submission

        print(obj)
        return obj
    except Exception as e:
        print(e)
        analytics.status = SubmissionAnalytics.Status.RUNTIME_ERROR
        analytics.save()
        analytics.result = json.dumps(
            {
                "error": str(e),
            }
        )
        analytics.save()
        if email:
            send_email_task.delay(
                email=submission.user.email,
                subject=f"{analytics.status.name} - {submission.problem.title}",
                message=f"{str(e)}",
            )
        return None
