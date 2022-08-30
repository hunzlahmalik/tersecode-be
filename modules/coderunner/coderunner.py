from dataclasses import dataclass

import epicbox


@dataclass
class EpicboxResult:
    """
    Result of a run
    """

    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: float
    timeout: bool
    oom_killed: bool

    def __str__(self) -> str:
        if self.oom_killed:
            return "OOM killed"
        if self.stderr:
            return self.stderr.decode("utf-8")
        if self.stderr:
            self.stdout.decode("utf-8")
        return str(self.exit_code)

    @property
    def is_error(self) -> bool:
        return self.oom_killed or len(self.stderr) > 0

    @property
    def is_timeout(self) -> bool:
        return self.timeout


@dataclass
class CodeRunnerTestCase:
    """
    Testcase for the code runner
    """

    input: list[int | str]
    memory: int
    runtime: int


PROFILES = {
    "python": {
        "docker_image": "python:latest",
        "command": "python3 main.py",
        # "user": "sandbox",
    },
    "python2": {
        "docker_image": "python:2.7.14",
        "command": "python2 main.py",
        "user": "sandbox",
    },
    "python3": {
        "docker_image": "python:3.10",
        "command": "python3 main.py",
        "user": "sandbox",
    },
    "gcc_compile": {
        "docker_image": "gcc:latest",
        "command": "g++ -pipe -O2 -static -o main main.cpp",
        "user": "root",
    },
    "c++": {
        "docker_image": "gcc:latest",
        "command": "./main",
        "user": "sandbox",
        "read_only": True,
    },
}

epicbox.configure(profiles=PROFILES, docker_url="unix:///var/run/docker.sock")


def run(
    language: str,
    testcases: list[CodeRunnerTestCase],
    filepath: str | None = None,
    code: str | None = None,
) -> list[EpicboxResult]:
    """
    Runs the code and returns the output
    :param code: code to run
    :type code: str
    :param filepath: path to the file
    :type filepath: str
    :param language: language of the code
    :type language: str
    :param testcases: list of testcases
    :type testcases: list[tuple(list, int, int)]
    :return: List of results. Each output is a list.
    :rtype: list[list]
    :raise ValueError: if language is not supported
    :raise ValueError: if inputs is not a list of lists
    """

    if code is None and filepath is None:
        raise ValueError("filepath or code is required")
    if code is not None and filepath is not None:
        raise ValueError("filepath or code is required")
    if code is None and filepath is not None:
        code = open(filepath, "r").read()

    if language not in PROFILES.keys():
        raise ValueError("Language not supported")
    if not isinstance(testcases, list):
        raise ValueError("Inputs must be a list of lists")
    if len(testcases) == 0:
        raise ValueError("Inputs must be a list of lists")

    results = []
    with epicbox.working_directory() as workdir:
        if language == "c++":
            epicbox.run(
                profile_name="gcc_compile",
                files=[{"name": "main.cpp", "content": code}],
                workdir=workdir,
            )
        for testcase in testcases:
            result = epicbox.run(
                profile_name=language,
                limits={
                    "memory": testcase.memory,
                    "realtime": testcase.runtime,
                },
                files=[{"name": "main.py", "content": bytes(code, "utf-8")}],
                stdin="\n".join(map(str, testcase.input)),
                workdir=workdir,
            )
            results.append(
                EpicboxResult(
                    exit_code=result["exit_code"],
                    stdout=result["stdout"],
                    stderr=result["stderr"],
                    duration=result["duration"],
                    timeout=result["timeout"],
                    oom_killed=result["oom_killed"],
                )
            )

    return results


# outputs = run(
#     filepath="/Volumes/data/code/github/tersecode/modules/coderunner/main.py",
#     language="python",
#     testcases=[
#         ([1, 2], 10, 10),
#         ([2, 3], 10, 10),
#     ],
# )
# print(outputs)
