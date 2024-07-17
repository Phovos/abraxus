# main.py

from src.bicycle_exp import AdaptiveMorphologicalSystem
from src.kernel import SymbolicKernel
from src.llama_interface import LlamaInterface

import asyncio
import subprocess
import sys
import argparse
import os
import shutil
import platform
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, TypeVar, Generic, Optional, List
import logging
import json
import struct


T = TypeVar('T')  # Type Variable to allow type-checking, linting,.. of Generic "T" and "V"
V = TypeVar('V')

class ContrapositiveData(Generic[T, V]):
    def __init__(self, t_value: T, v_value: V):
        self.t_value = t_value
        self.v_value = v_value

async def usermain():
    system = AdaptiveMorphologicalSystem("kb_dir", "output_dir", 1000000)
    await system.initialize()
    
    await system.add_experiment(
        name="Bicycle Balance",
        hypothesis="A moving bicycle is naturally stable due to gyroscopic effects",
        procedure="Analyze the physics of a moving bicycle and its stability factors"
    )
    
    await system.add_experiment(
        name="Bicycle Frame Materials",
        hypothesis="Carbon fiber frames provide the best strength-to-weight ratio for bicycles",
        procedure="Compare different bicycle frame materials and their properties"
    )
    
    async for results in system.run_experiments():
        print(f"Experiment results:")
        print(results)
    
    print("\nEvolution History:")
    for entry in system.get_evolution_history():
        print(f"{entry['timestamp']}: {entry['message']}")

    await system.symbolic_kernel.stop()

if __name__ == "__main__":
    asyncio.run(usermain())