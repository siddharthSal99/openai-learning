from gym.envs.registration import register

register(
    id='rlSeeker-v0',
    entry_point='rlSeeker.envs:rlSeeker',
)
