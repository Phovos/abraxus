from src.kernel import SymbolicKernel
import asyncio
import datetime
import json
import os
import sys
from typing import Any, Dict, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class Experiment:
    def __init__(self, name: str, hypothesis: str, procedure: str):
        self.name = name
        self.hypothesis = hypothesis
        self.procedure = procedure
        self.results = []

    async def run(self, kernel: SymbolicKernel) -> Dict[str, Any]:
        result = await kernel.process_task(self.procedure)
        self.results.append(result)
        return result


class ContrapositiveDualExperiment:
    def __init__(self, experiment: Experiment):
        self.original = experiment
        self.negation = self._create_negation(experiment)

    def _create_negation(self, experiment: Experiment) -> Experiment:
        return Experiment(
            name=f"Not-{experiment.name}",
            hypothesis=f"The opposite of: {experiment.hypothesis}",
            procedure=f"Attempt to disprove: {experiment.procedure}",
        )

    async def run(self, kernel: SymbolicKernel) -> Dict[str, Any]:
        original_result = await self.original.run(kernel)
        negation_result = await self.negation.run(kernel)
        return {"original": original_result, "negation": negation_result}


class AdaptiveMorphologicalSystem:
    def __init__(self, kb_dir: str, output_dir: str, max_memory: int):
        self.symbolic_kernel = SymbolicKernel(kb_dir, output_dir, max_memory)
        self.evolution_history = []
        self.experiments = []

    async def initialize(self):
        await self.symbolic_kernel.initialize()
        self.commit_changes("System initialized")

    async def add_experiment(self, name: str, hypothesis: str, procedure: str):
        experiment = Experiment(name, hypothesis, procedure)
        dual_experiment = ContrapositiveDualExperiment(experiment)
        self.experiments.append(dual_experiment)
        self.commit_changes(f"Added experiment: {name}")

    async def run_experiments(self):
        for dual_experiment in self.experiments:
            results = await dual_experiment.run(self.symbolic_kernel)
            await self.evolve_based_on_results(results)
            yield results

    async def evolve_based_on_results(self, results: Dict[str, Any]):
        original_concepts = await self.symbolic_kernel.llama.extract_concepts(
            str(results["original"])
        )
        negation_concepts = await self.symbolic_kernel.llama.extract_concepts(
            str(results["negation"])
        )

        self.symbolic_kernel.knowledge_base.update(
            original_concepts + negation_concepts
        )

        self.commit_changes(f"Evolved based on experiment results")

    def commit_changes(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.evolution_history.append({"timestamp": timestamp, "message": message})

    def get_evolution_history(self) -> List[Dict[str, str]]:
        return self.evolution_history


async def main():
    system = AdaptiveMorphologicalSystem("kb_dir", "output_dir", 1000000)
    await system.initialize()

    await system.add_experiment(
        name="Bicycle Balance",
        hypothesis="A moving bicycle is naturally stable due to gyroscopic effects",
        procedure="Analyze the physics of a moving bicycle and its stability factors",
    )

    await system.add_experiment(
        name="Bicycle Frame Materials",
        hypothesis="Carbon fiber frames provide the best strength-to-weight ratio for bicycles",
        procedure="Compare different bicycle frame materials and their properties",
    )

    async for results in system.run_experiments():
        print(f"Experiment results:")
        print(json.dumps(results, indent=2))

    print("\nEvolution History:")
    for entry in system.get_evolution_history():
        print(f"{entry['timestamp']}: {entry['message']}")

    await system.symbolic_kernel.stop()


if __name__ == "__main__":
    asyncio.run(main())
