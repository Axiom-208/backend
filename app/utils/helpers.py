from typing import Optional, Type, Any, Tuple
from copy import deepcopy

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def make_optional_model(model: Type[BaseModel], name_suffix="Update") -> Type[BaseModel]:
    """Creates a new model where all fields are optional."""
    return create_model(
        f"{model.__name__}{name_suffix}",
        **{field: (Optional[typ], None) for field, typ in model.__annotations__.items()},
        __base__=model
    )