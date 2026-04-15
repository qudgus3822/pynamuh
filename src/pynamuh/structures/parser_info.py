"""주문 관련 TR 구조체 정의 (trio_ord.h 기반)"""

from typing import ClassVar, Type, TYPE_CHECKING
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field, field_validator

if TYPE_CHECKING:
    from .common import OutBlock


def get_parser_info(block_name: str) -> tuple[Type[Structure], Type["OutBlock"], bool]:
    """파서 정보 조회

    Args:
        block_name: 블록명

    Returns:
        (OutBlock C구조체, OutBlock Python Class, is_array) 튜플
    """
    match block_name:
        case "j8":
            from .inv.j8 import CTj8OutBlock, Tj8OutBlock
            return (CTj8OutBlock, Tj8OutBlock, False)
        case "c8201OutBlock":
            from .ord.c8201 import CTc8201OutBlock, Tc8201OutBlock
            return (CTc8201OutBlock, Tc8201OutBlock, False)
        case "c8201OutBlock1":
            from .ord.c8201 import CTc8201OutBlock1, Tc8201OutBlock1
            return (CTc8201OutBlock1, Tc8201OutBlock1, True)
        case "c8201":
            return None
        case "c8101OutBlock":
            from .ord.c8101 import CTc8101OutBlock, Tc8101OutBlock
            return (CTc8101OutBlock, Tc8101OutBlock, False)
        case "c8101":
            return None
        case "c8102OutBlock":
            from .ord.c8102 import CTc8102OutBlock, Tc8102OutBlock
            return (CTc8102OutBlock, Tc8102OutBlock, False)
        case "c8102":
            return None
        case "c8103OutBlock":
            from .ord.c8103 import CTc8103OutBlock, Tc8103OutBlock
            return (CTc8103OutBlock, Tc8103OutBlock, False)
        case "c8103":
            return None
        case "c8104OutBlock":
            from .ord.c8104 import CTc8104OutBlock, Tc8104OutBlock
            return (CTc8104OutBlock, Tc8104OutBlock, False)
        case "c8104":
            return None
        # [변경: 2026-04-15 00:00, 김병현 수정] s8180 주문/체결 조회 파서 등록
        case "s8180OutBlock":
            from .ord.s8180 import CTs8180OutBlock, Ts8180OutBlock
            return (CTs8180OutBlock, Ts8180OutBlock, False)
        case "s8180OutBlock1":
            from .ord.s8180 import CTs8180OutBlock1, Ts8180OutBlock1
            return (CTs8180OutBlock1, Ts8180OutBlock1, True)
        case "s8180OutBlock2":
            from .ord.s8180 import CTs8180OutBlock2, Ts8180OutBlock2
            return (CTs8180OutBlock2, Ts8180OutBlock2, False)
        case "s8180":
            return None
        case _:
            raise ValueError(f"아직 Block이 구현되지 않음! : {block_name}")

