from .modules import loading_bar_handler
from .state import State
from .bfs import BreadthFirstSearch
from .dijkstra import DijkstraBestFirstSearch

UI = False

if UI:
    loading_bar_handler(False)
import julia

_ = julia.Julia(compiled_modules=False)

if UI:
    loading_bar_handler(True)

from julia import PDDL


class AutomatedPlanning:
    def __init__(self, domain_path, problem_path):
        self.domain = PDDL.load_domain(domain_path)
        self.problem = PDDL.load_problem(problem_path)
        self.initial_state = PDDL.initialize(self.problem)

    def __execute_action(self, action, state):
        return PDDL.execute(action, state)

    def transition(self, state, action):
        return PDDL.transition(self.domain, state, action, check=False)
        
    def available_actions(self, state):
        return PDDL.available(state, self.domain)

    def satisfies(self, asserted_state, state):
        return PDDL.satisfy(asserted_state, state, self.domain)[0]

    def __retrace_path(self, state):
        path = []
        while state.parent:
            path.append(state)
            state = state.parent
        path.reverse()
        return path

    def get_actions_from_path(self, path):
        if not path:
            print("Path is empty, can't operate...")
            return []
        actions = []
        for state in path:
            actions.append((state.parent_action, state.g_cost))

        cost = PDDL.get_value(path[-1].description, "total-cost")
        if not cost:
            return actions
        else:
            return (actions, cost)

    def get_state_def_from_path(self, path):
        if not path:
            print("Path is empty, can't operate...")
            return []
        trimmed_path = []
        for state in path:
            trimmed_path.append(state.description)
        return trimmed_path 

    def breadth_first_search(self):
        bfs = BreadthFirstSearch(self, PDDL)
        last_state = bfs.search()
        path = self.__retrace_path(last_state)
        return path


if __name__ == "__main__":
    ap = AutomatedPlanning("..data/domain.pddl", "..data/problem.pddl")
