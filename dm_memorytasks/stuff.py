import dm_memorytasks

settings = dm_memorytasks.EnvironmentSettings(seed=123, level_name='spot_diff_train')
env = dm_memorytasks.load_from_docker(settings)