"""주문 취소 TR 구조체 정의 (trio_ord.h c8104 기반)"""

from typing import ClassVar, Type
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field

from ..common import InBlock, OutBlock


# ==============================================================================
# C 구조체 정의 (trio_ord.h 기반)
# ==============================================================================

class CTc8104InBlock(Structure):
    """주문 취소 입력 블록 C 구조체"""
    _fields_ = [
        ("pswd_noz8", ctypes.c_char * 44),             # 계좌비밀번호 (해시 44자)
        ("_pswd_noz8", ctypes.c_char * 1),
        ("issue_codez6", ctypes.c_char * 6),            # 종목번호
        ("_issue_codez6", ctypes.c_char * 1),
        ("canc_qtyz12", ctypes.c_char * 12),            # 취소수량
        ("_canc_qtyz12", ctypes.c_char * 1),
        ("orgnl_order_noz10", ctypes.c_char * 10),      # 원주문번호
        ("_orgnl_order_noz10", ctypes.c_char * 1),
        ("all_part_typez1", ctypes.c_char * 1),          # 취소구분 (1:잔량전체, 2:일부수량)
        ("_all_part_typez1", ctypes.c_char * 1),
        ("trad_pswd_no_1z8", ctypes.c_char * 44),       # 거래비밀번호1 (해시 44자)
        ("_trad_pswd_no_1z8", ctypes.c_char * 1),
        ("trad_pswd_no_2z8", ctypes.c_char * 44),       # 거래비밀번호2 (해시 44자)
        ("_trad_pswd_no_2z8", ctypes.c_char * 1),
    ]


class CTc8104OutBlock(Structure):
    """주문 취소 출력 블록 C 구조체"""
    _fields_ = [
        ("orgnl_order_noz10", ctypes.c_char * 10),       # 원주문번호
        ("_orgnl_order_noz10", ctypes.c_char * 1),
        ("order_noz10", ctypes.c_char * 10),             # 주문번호
        ("_order_noz10", ctypes.c_char * 1),
        ("mom_order_noz10", ctypes.c_char * 10),         # 모주문번호
        ("_mom_order_noz10", ctypes.c_char * 1),
        ("issue_codez6", ctypes.c_char * 6),             # 후종목번호
        ("_issue_codez6", ctypes.c_char * 1),
        ("canc_qtyz12", ctypes.c_char * 12),             # 취소수량
        ("_canc_qtyz12", ctypes.c_char * 1),
        ("sor_fle_idz20", ctypes.c_char * 20),           # SOR파일ID
        ("_sor_fle_idz20", ctypes.c_char * 1),
        ("can_sor_ant_rt1z11", ctypes.c_char * 11),      # 취소SOR배분비율KRX
        ("_can_sor_ant_rt1z11", ctypes.c_char * 1),
        ("can_sor_ant_rt2z11", ctypes.c_char * 11),      # 취소SOR배분비율NXT
        ("_can_sor_ant_rt2z11", ctypes.c_char * 1),
        ("can_orr_qty1z18", ctypes.c_char * 18),         # 취소주문수량KRX
        ("_can_orr_qty1z18", ctypes.c_char * 1),
        ("can_orr_qty2z18", ctypes.c_char * 18),         # 취소주문수량NXT
        ("_can_orr_qty2z18", ctypes.c_char * 1),
        ("can_cld_mkt_orr_no1z10", ctypes.c_char * 10),  # 취소자시장주문번호KRX
        ("_can_cld_mkt_orr_no1z10", ctypes.c_char * 1),
        ("can_cld_mkt_orr_no2z10", ctypes.c_char * 10),  # 취소자시장주문번호NXT
        ("_can_cld_mkt_orr_no2z10", ctypes.c_char * 1),
    ]


# ==============================================================================
# Pydantic 모델 (사용자 친화적 인터페이스)
# ==============================================================================

class Tc8104InBlock(InBlock):
    """주문 취소 입력 블록

    Attributes:
        pswd_noz8: 계좌비밀번호 해시 (44자)
        issue_codez6: 종목번호 (6자리)
        canc_qtyz12: 취소수량
        orgnl_order_noz10: 원주문번호 (취소할 주문번호)
        all_part_typez1: 취소구분 ("1":잔량전체, "2":일부수량)
        trad_pswd_no_1z8: 거래비밀번호1 해시 (44자)
        trad_pswd_no_2z8: 거래비밀번호2 해시 (44자)
    """

    C_STRUCT: ClassVar[Type[ctypes.Structure]] = CTc8104InBlock

    pswd_noz8: str = Field(min_length=44, max_length=44, description="계좌비밀번호 해시")
    issue_codez6: str = Field(min_length=6, max_length=6, description="종목번호")
    canc_qtyz12: str = Field(max_length=12, description="취소수량")
    orgnl_order_noz10: str = Field(max_length=10, description="원주문번호")
    all_part_typez1: str = Field(max_length=1, description="취소구분", default="1")
    trad_pswd_no_1z8: str = Field(min_length=44, max_length=44, description="거래비밀번호1 해시")
    trad_pswd_no_2z8: str = Field(min_length=44, max_length=44, description="거래비밀번호2 해시")


# ==============================================================================
# Output 구조체
# ==============================================================================

@dataclass
class Tc8104OutBlock(OutBlock):
    """주문 취소 출력 블록"""
    orgnl_order_noz10: str       # 원주문번호
    order_noz10: str             # 주문번호
    mom_order_noz10: str         # 모주문번호
    issue_codez6: str            # 후종목번호
    canc_qtyz12: str             # 취소수량
    sor_fle_idz20: str           # SOR파일ID
    can_sor_ant_rt1z11: str      # 취소SOR배분비율KRX
    can_sor_ant_rt2z11: str      # 취소SOR배분비율NXT
    can_orr_qty1z18: str         # 취소주문수량KRX
    can_orr_qty2z18: str         # 취소주문수량NXT
    can_cld_mkt_orr_no1z10: str  # 취소자시장주문번호KRX
    can_cld_mkt_orr_no2z10: str  # 취소자시장주문번호NXT


__all__ = [
    "CTc8104InBlock",
    "Tc8104InBlock",
    "CTc8104OutBlock",
    "Tc8104OutBlock",
]
