from typing import Type

from pytest import mark, raises

from datek_async_fsm.errors import (
    FSMError,
    InitialStateNotProvidedError,
    MultipleInitialStatesProvidedError,
    EndStateNotProvidedError,
)
from tests.example import FSM, Start, S1, S2, S3, End, BaseState


class TestFSM:
    @mark.asyncio
    async def test_run(self):
        fsm = FSM(
            [Start, S1, S2, S3, End],
            transitions=["4", "1", "3", "1", "3", "3", "2", "4"],
        )

        await fsm.run()

        assert fsm.current_state is End

    @mark.parametrize(
        ["states", "error_type"],
        [
            ([S1, S2, End], InitialStateNotProvidedError),
            ([Start, Start, End], MultipleInitialStatesProvidedError),
            ([Start, S1], EndStateNotProvidedError),
        ],
    )
    def test_init_raises_proper_error(
        self, states: list[Type[BaseState]], error_type: Type[FSMError]
    ):
        with raises(error_type):
            FSM(states)
