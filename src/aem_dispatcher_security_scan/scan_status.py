from enum import Enum


class ScanStatus(Enum):
    FAILED = "FAILED"
    SAFE = "SAFE"
    VULNERABLE = "VULNERABLE"
