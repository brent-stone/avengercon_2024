"""
MinIO related schemas
"""

from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class BucketCreationResult:
    """
    Class for reporting status of bucket creation requests
    """

    success: List[str] = field(default_factory=list)
    failure: List[str] = field(default_factory=list)
    preexisting: List[str] = field(default_factory=list)
