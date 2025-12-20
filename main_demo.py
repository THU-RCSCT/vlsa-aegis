import collections
import dataclasses
import logging
import pathlib

import imageio
from libero.libero import benchmark
from libero.libero import get_libero_path
from libero.libero.envs import OffScreenRenderEnv
import numpy as np
import tqdm
import tyro
from typing import List

LIBERO_DUMMY_ACTION = [0.0] * 6 + [-1.0]
LIBERO_ENV_RESOLUTION = 256  # resolution used to render training data


@dataclasses.dataclass
class Args:
    #################################################################################################################
    # LIBERO environment-specific parameters
    #################################################################################################################
    task_suite_name: str = (
        "safelibero_goal"  # Task suite. Options: safelibero_spatial, safelibero_object, safelibero_goal, safelibero_long
    )
    safety_level: str = "I" # Task level. Options: I, II
    # task_index: int = 0 # Task_id. Options: 0, 1, 2, 3
    task_index: List[int] = dataclasses.field(default_factory=lambda: [0]) # Options: [0, 1, 2, 3]
    # episode_index: int = 0 # Episode_id. Options: 0~49
    episode_index: List[int] = dataclasses.field(default_factory=lambda: [0]) # Options: [0, 1, 2, 3, 4, ..., 49]
    num_steps_wait: int = 10  # Number of steps to wait for objects to stabilize i n sim
    num_trials_per_task: int = 50  # Number of rollouts per task

    #################################################################################################################
    # Utils
    #################################################################################################################
    video_out_path: str = "data/libero/videos"  # Path to save videos

    seed: int = 7  # Random Seed (for reproducibility)


def eval_libero(args: Args) -> None:
    # Set random seed
    np.random.seed(args.seed)
    safety_level = args.safety_level
    task_index = args.task_index
    episode_index = args.episode_index
    # Initialize LIBERO task suite
    benchmark_dict = benchmark.get_benchmark_dict()

    task_suite = benchmark_dict[args.task_suite_name](safety_level=safety_level)
    

    num_tasks_in_suite = task_suite.n_tasks

    logging.info(f"Task suite: {args.task_suite_name}, safety level: {safety_level}")

    pathlib.Path(args.video_out_path).mkdir(parents=True, exist_ok=True)

    # Set to 10 for a quick view
    if args.task_suite_name == "safelibero_spatial":
        max_steps = 10  
    elif args.task_suite_name == "safelibero_object":
        max_steps = 10  
    elif args.task_suite_name == "safelibero_goal":
        max_steps = 10  
    elif args.task_suite_name == "safelibero_long":
        max_steps = 10  
    else:
        raise ValueError(f"Unknown task suite: {args.task_suite_name}")

    # Start evaluation
    total_episodes, total_successes = 0, 0
    # only run for the firsrst task
    for task_id in tqdm.tqdm(task_index): # All tasks: range(num_tasks_in_suite) 
        # Get task
        task = task_suite.get_task(task_id)

        # Get default LIBERO initial states
        initial_states = task_suite.get_task_init_states(task_id)

        # Initialize LIBERO environment and task description
        env, task_description = _get_libero_env(task, safety_level, LIBERO_ENV_RESOLUTION, args.seed)

        # Start episodes
        task_episodes, task_successes = 0, 0
        #Only run for the first episode
        for episode_idx in tqdm.tqdm(episode_index): # All episodes: range(args.num_trials_per_task)
            logging.info(f"\nTask: {task_description}")

            # Reset environment
            env.reset()

            # Set initial states
            obs = env.set_init_state(initial_states[episode_idx])

            # Setup
            t = 0
            replay_images = []

            logging.info(f"Starting episode {task_episodes+1}...")
            while t < max_steps + args.num_steps_wait:
                try:
                    # IMPORTANT: Do nothing for the first few timesteps because the simulator drops objects
                    # and we need to wait for them to fall
                    if t < args.num_steps_wait:
                        obs, reward, done, info = env.step(LIBERO_DUMMY_ACTION)
                        t += 1
                        continue

                    # Get preprocessed image
                    # IMPORTANT: rotate 180 degrees to match train preprocessing
                    img = np.ascontiguousarray(obs["agentview_image"][::-1, ::-1])
                    
                    # Save preprocessed image for replay video
                    replay_images.append(img)

                    action = LIBERO_DUMMY_ACTION

                    # Execute action in environment
                    obs, reward, done, info = env.step(action)
                    if done:
                        task_successes += 1
                        total_successes += 1
                        break
                    t += 1

                except Exception as e:
                    logging.error(f"Caught exception: {e}")
                    break

            task_episodes += 1
            total_episodes += 1

            # Save a replay video of the episode
            suffix = "success" if done else "failure"
            task_segment = task_description.replace(" ", "_")
            imageio.mimwrite(
                pathlib.Path(args.video_out_path) / f"rollout_{task_segment}_{safety_level}_{episode_idx}_{suffix}.mp4",
                [np.asarray(x) for x in replay_images],
                fps=10,
            )
            logging.info(f"Saved replay video to {pathlib.Path(args.video_out_path) / f'rollout_{task_segment}_{safety_level}_{episode_idx}_{suffix}.mp4'}")
            
            # Log current results
            logging.info(f"Success: {done}")
            logging.info(f"# episodes completed so far: {total_episodes}")
            logging.info(f"# successes: {total_successes} ({total_successes / total_episodes * 100:.1f}%)")

        # Log final results
        logging.info(f"Current task success rate: {float(task_successes) / float(task_episodes)}")
        logging.info(f"Current total success rate: {float(total_successes) / float(total_episodes)}")

    logging.info(f"Total success rate: {float(total_successes) / float(total_episodes)}")
    logging.info(f"Total episodes: {total_episodes}")


def _get_libero_env(task, level, resolution, seed):
    """Initializes and returns the LIBERO environment, along with the task description."""
    task_description = task.language
    task_bddl_file = pathlib.Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env_args = {"bddl_file_name": task_bddl_file, "camera_heights": resolution, "camera_widths": resolution}
    env = OffScreenRenderEnv(**env_args)
    env.seed(seed)  # IMPORTANT: seed seems to affect object positions even when using fixed initial state
    return env, task_description


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = tyro.cli(Args)
    eval_libero(args)