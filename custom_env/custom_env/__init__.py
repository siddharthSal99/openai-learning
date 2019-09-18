from gym.envs.registration import register

register(
    id='sid_cartpole-v0',
    entry_point='custom_env.envs:SidCartpole',
)
