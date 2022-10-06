def code_storage_path(instance: "Submission", filename: str) -> str:
    return "submissions/{}/{}_{}".format(
        instance.user.username, instance.problem.title, instance.timestamp
    )
