from dataclasses import dataclass

import epicbox

PRE_JS = """
const _prompt = require('synchro-prompt');

function prompt(message) {
    if (message)
        return _prompt(message);
    else 
        return _prompt("");
}
    
"""


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


DOCKER_IMAGE = "crackaf/tersecode:epicbox"

PROFILES = {
    "python": {
        "docker_image": DOCKER_IMAGE,
        "command": "python3 main",
        # "user": "sandbox",
    },
    "python2": {
        "docker_image": DOCKER_IMAGE,
        "command": "python2 main",
        "user": "sandbox",
    },
    "python3": {
        "docker_image": DOCKER_IMAGE,
        "command": "python3 main",
        "user": "sandbox",
    },
    "gcc_compile": {
        "docker_image": DOCKER_IMAGE,
        "command": "g++ -pipe -O2 -static main -o out",
        "user": "root",
    },
    "cpp": {
        "docker_image": DOCKER_IMAGE,
        "command": "./out",
        "user": "root",
        "read_only": True,
    },
    "javascript": {
        "docker_image": DOCKER_IMAGE,
        "command": "node main",
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

        if language == "javascript":
            code = PRE_JS + code

        for testcase in testcases:
            result = None
            if language == "cpp":
                result = epicbox.run(
                    profile_name="gcc_compile",
                    files=[{"name": "main", "content": bytes(code, "utf-8")}],
                    workdir=workdir,
                )
            result = epicbox.run(
                profile_name=language,
                limits={
                    "memory": testcase.memory,
                    "realtime": testcase.runtime,
                },
                files=[{"name": "main", "content": bytes(code, "utf-8")}],
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
