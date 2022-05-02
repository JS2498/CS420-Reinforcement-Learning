# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:06:48 2022

@author: IIT
"""


import ray

ray.shutdown()    # shutdown the Ray it was started previously
ray.init(ignore_reinit_error=True)  # initialize the ray by ignoring the reinitilization error



# %%

from ray import tune

config = {
    # PPO specific settings:
    "lr_schedule" : None,
    "use_critic" : True,
    "use_gae" : True,
    "lambda" : 1.0,
    "kl_coeff" : 0.2,
    "sgd_minibatch_size" :  128,
    "num_sgd_iter" : 30,
    "shuffle_sequences" : True,
    "vf_loss_coeff" : 1.0,
    "entropy_coeff" : 0.0,
    "entropy_coeff_schedule" : None,
    "clip_param" : 0.3,
    "vf_clip_param" : 10.0,
    "grad_clip" : None,
    "kl_target" : 0.01,

     # Override some of TrainerConfig's default values with PPO-specific values.
    "rollout_fragment_length" : 200,
    "train_batch_size" : 4000,
    "lr" : 5e-5,
    "_disable_execution_plan_api" : True,
    # Environment (RLlib understands openAI gym registered strings).
    "env": "BreakoutNoFrameskip-v4",
    # Use 2 environment workers (aka "rollout workers") that parallelly
    # collect samples from their own environment clone(s).
    "num_workers":16,
    "num_gpus" : 1,
    # Change this to "framework: torch", if you are using PyTorch.
    # Also, use "framework: tf2" for tf2.x eager execution.
    "framework": "torch",
    # Tweak the default model provided automatically by RLlib,
    # given the environment's observation- and action spaces.
    #"model": {
    #    "fcnet_hiddens": [64, 64],
    #    "fcnet_activation": "relu",
    #},
    # Set up a separate evaluation worker set for the
    # `trainer.evaluate()` call after training (see below).
    "evaluation_num_workers": 1,
    # Only for evaluation runs, render the env.
    "evaluation_config": {
        "render_env": True,
    },
}
# %%

tune.run("PPO", 
         config = config,
         local_dir = './breakout/',
         checkpoint_freq = 100,
         verbose=1,
         checkpoint_at_end=True
         )
