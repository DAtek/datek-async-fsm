from abc import ABC, ABCMeta
from asyncio import run
from functools import wraps
from typing import Optional, Type, AsyncGenerator

from datek_async_fsm.fsm import BaseFSM
from datek_async_fsm.state import BaseState as _BaseState, StateType, StateCollection


class StateMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace):
        class_ = super().__new__(mcs, name, bases, namespace)
        class_.transit = _print_successful_transition(class_.transit)
        return class_


def _print_successful_transition(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        result: Optional[BaseState] = await func(self, *args, **kwargs)

        if result:
            print(f"{self.__class__.__name__} -> {result.__name__}")

        return result

    return wrapper


class BaseState(_BaseState, ABC, metaclass=StateMeta):
    pass


class Start(BaseState):
    value: str

    _transition_map = {
        "1": "S1",
    }

    @staticmethod
    def type() -> StateType:
        return StateType.INITIAL

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        class_name = self._transition_map.get(self.value)
        return states.get(class_name)


class S1(BaseState):
    value: str

    _transition_map = {
        "3": "S3",
        "2": "S2",
    }

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        class_name = self._transition_map.get(self.value)
        return states.get(class_name)


class S2(BaseState):
    value: str

    _transition_map = {
        "4": "End",
    }

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        class_name = self._transition_map.get(self.value)
        return states.get(class_name)


class S3(BaseState):
    value: str

    _transition_map = {
        "3": "S3",
        "2": "S2",
        "1": "S1",
    }

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        class_name = self._transition_map.get(self.value)
        return states.get(class_name)


class End(BaseState):
    value: str

    @staticmethod
    def type() -> StateType:
        return StateType.END

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        pass


class FSM(BaseFSM):
    transitions: list[str]

    async def _input_generator(self) -> AsyncGenerator[dict, None]:
        for transition in self.transitions:
            yield {"value": transition}


if __name__ == "__main__":
    fsm = FSM([Start, S1, S2, S3, End], transitions=["1", "3", "1", "3", "3", "2", "4"])

    run(fsm.run())
