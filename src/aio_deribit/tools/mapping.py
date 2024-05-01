from typing import Any, TypeVar

from adaptix import Retort

from aio_deribit.exceptions import MappingError

T = TypeVar("T")


class Mapper:
    def __init__(self, retort: Retort) -> None:
        """
        Class provides mapper for JSON response parsing.

        :param retort:
        :return None:
        """
        self._retort = retort

    def load(self, data: Any, class_: type[T]) -> T:  # noqa: ANN401
        """
        Create model from mapping.

        :param data: Any data.
        :param class_: Class to creation.
        :return:
        """
        try:
            return self._retort.load(data, class_)
        except Exception as err:
            raise MappingError from err

    def dump(self, data: Any) -> Any:  # noqa: ANN401
        """
        Create mapping from the model.

        :param data: Any data.
        :return:
        """
        try:
            return self._retort.dump(data)
        except Exception as err:
            raise MappingError from err
