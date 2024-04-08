from adaptix import name_mapping, NameStyle, Retort

from aio_deribit.api.responses.base import Response

_RECIPE = [
    # convert camel case to snake case according to the PEP8
    name_mapping(Response, name_style=NameStyle.CAMEL),
]

_RETORT = Retort(recipe=_RECIPE)
