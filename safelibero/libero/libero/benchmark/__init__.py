import abc
import os
import glob
import random
import torch

from typing import List, NamedTuple, Type
from libero.libero import get_libero_path

from libero.libero.benchmark.libero_suite_task_map import libero_task_map

BENCHMARK_MAPPING = {}


def register_benchmark(target_class):
    """We design the mapping to be case-INsensitive."""
    BENCHMARK_MAPPING[target_class.__name__.lower()] = target_class


def get_benchmark_dict(help=False):
    if help:
        print("Available benchmarks:")
        for benchmark_name in BENCHMARK_MAPPING.keys():
            print(f"\t{benchmark_name}")
    return BENCHMARK_MAPPING


def get_benchmark(benchmark_name):
    return BENCHMARK_MAPPING[benchmark_name.lower()]


def print_benchmark():
    print(BENCHMARK_MAPPING)


class Task(NamedTuple):
    name: str
    language: str
    problem: str
    problem_folder: str
    bddl_file: str
    init_states_file: str


def grab_language_from_filename(x):
    if x[0].isupper():  # LIBERO-100
        if "SCENE10" in x:
            language = " ".join(x[x.find("SCENE") + 8 :].split("_"))
        else:
            language = " ".join(x[x.find("SCENE") + 7 :].split("_"))
    else:
        language = " ".join(x.split("_"))
    en = language.find(".bddl")
    return language[:en]


libero_suites = [
    "safelibero_spatial",
    "safelibero_object",
    "safelibero_goal",
    "safelibero_long",
]
task_maps = {}
max_len = 0
for libero_suite in libero_suites:
    task_maps[libero_suite] = {}

    for task in libero_task_map[libero_suite]:
        language = grab_language_from_filename(task + ".bddl")
        task_maps[libero_suite][task] = Task(
            name=task,
            language=language,
            problem="Libero",
            problem_folder=libero_suite,
            bddl_file=f"{task}.bddl",
            init_states_file=f"{task}.pruned_init",
        )

        # print(language, "\n", f"{task}.bddl", "\n")
        # print("")

task_orders = [[0,1,2,3]]

class Benchmark(abc.ABC):
    """A Benchmark."""

    def __init__(self, task_order_index=0, safety_level="I"):
        self.task_embs = None
        self.task_order_index = task_order_index
        self.safety_level = safety_level
  

    def _make_benchmark(self):
        tasks = list(task_maps[self.name].values())
        print(f"[info] using task orders {task_orders[self.task_order_index]}")
        task_order = task_orders[self.task_order_index]
        if self.name == "safelibero_goal" and self.safety_level == "II":
            task_order = [4 if i == 3 else i for i in task_order]        
        self.tasks = [tasks[i] for i in task_order]
        self.n_tasks = len(self.tasks)

    def get_num_tasks(self):
        return self.n_tasks

    def get_task_names(self):
        return [task.name for task in self.tasks]

    def get_task_problems(self):
        return [task.problem for task in self.tasks]

    def get_task_bddl_files(self):
        return [task.bddl_file for task in self.tasks]

    def get_task_bddl_file_path(self, i):
        bddl_file_path = os.path.join(
            get_libero_path("bddl_files"),
            self.tasks[i].problem_folder,
            self.tasks[i].bddl_file,
        )
        return bddl_file_path

    def get_task_demonstration(self, i):
        assert (
            0 <= i and i < self.n_tasks
        ), f"[error] task number {i} is outer of range {self.n_tasks}"
        # this path is relative to the datasets folder
        demo_path = f"{self.tasks[i].problem_folder}/{self.tasks[i].name}_demo.hdf5"
        return demo_path

    def get_task(self, i):
        return self.tasks[i]

    def get_task_emb(self, i):
        return self.task_embs[i]

    def get_task_init_states(self, i):
        init_states_path = os.path.join(
            get_libero_path("init_states"),
            self.tasks[i].problem_folder,
            self.tasks[i].init_states_file
        )

        init_states_path = init_states_path.replace(".pruned_init", f"_level_{self.safety_level}.pruned_init")


        init_states = torch.load(init_states_path)
        
        return init_states

    def set_task_embs(self, task_embs):
        self.task_embs = task_embs


@register_benchmark
class SAFELIBERO_SPATIAL(Benchmark):
    def __init__(self, task_order_index=0, safety_level="I"):
        super().__init__(task_order_index=task_order_index, safety_level=safety_level)
        self.name = "safelibero_spatial"
        self._make_benchmark()


@register_benchmark
class SAFELIBERO_OBJECT(Benchmark):
    def __init__(self, task_order_index=0, safety_level="I"):
        super().__init__(task_order_index=task_order_index, safety_level=safety_level)
        self.name = "safelibero_object"
        self._make_benchmark()


@register_benchmark
class SAFELIBERO_GOAL(Benchmark):
    def __init__(self, task_order_index=0, safety_level="I"):
        super().__init__(task_order_index=task_order_index, safety_level=safety_level)
        self.name = "safelibero_goal"
        self._make_benchmark()

@register_benchmark
class SAFELIBERO_LONG(Benchmark):
    def __init__(self, task_order_index=0, safety_level="I"):
        super().__init__(task_order_index=task_order_index, safety_level=safety_level)
        self.name = "safelibero_long"
        self._make_benchmark()


