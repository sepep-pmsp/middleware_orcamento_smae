class MissingEnvironmentVariable(Exception):
    pass

def get_my_env_var(var_name):
    try:
        envvar = os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"ENV '{var_name}' must be set")

SOF_API_TOKEN = get_my_env_var('SOF_API_TOKEN')