import os


def env(key: str, required=True, default=None):
    if key not in os.environ:
        if required:
            raise RuntimeError(f'Please set the environment variable {key}.')
        else:
            return default
    else:
        return os.environ[key]
