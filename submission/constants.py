
def CODE_STORAGE_PATH(instance: 'Submission', filename: str) -> str:
    return 'submissions/{}/{}_{}'.format(instance.user.username, instance.problem.title, instance.id)


CODE_EXTENSIONS = ['py']
