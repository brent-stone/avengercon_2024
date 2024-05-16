"""
Demo pydantic schemas
"""
from pydantic import BaseModel
from pydantic.types import confloat
from pydantic.types import conint
from typing import Final

# Maximum value integers should reasonably take. This is the PostgreSQL max value
MAX_INT: Final[int] = 2147483647


class AISettingsCreateSchema(BaseModel):
    """
    Default AI Settings Pydantic Schema which should be kept in sync with the SQLAlchemy
    model.
    """

    subset_selection_size: conint(ge=1, le=MAX_INT) = 1
    max_intra_cluster_distance: confloat(ge=0.0, le=1.0) = 0.25
    kfold_n: conint(ge=1, le=10) = 4
    tang_inversion_distance: confloat(ge=0.0, le=1.0) = 0.25
    minimum_token_length: conint(ge=1, le=MAX_INT) = 1
    minimum_signal_resolution: conint(ge=1, le=MAX_INT) = 1
    use_padding: bool = False
    precision: conint(ge=1, le=6) = 3
    assume_partial_diag: bool = False
    ingest_chunk_n: conint(ge=1, le=MAX_INT) = 100000
