"""주문 정정 TR 구조체 정의 (trio_ord.h c8103 기반)"""

from typing import ClassVar, Type
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field

from ..common import InBlock, OutBlock


# ==============================================================================
# C 구조체 정의 (trio_ord.h 기반)
# ==============================================================================

class CTc8103InBlock(Structure):
    """주문 정정 입력 블록 C 구조체"""
    _fields_ = [
        ("pswd_noz8", ctypes.c_char * 44),             # 계좌비밀번호 (해시 44자)
        ("_pswd_noz8", ctypes.c_char * 1),
        ("issue_codez6", ctypes.c_char * 6),            # 종목번호
        ("_issue_codez6", ctypes.c_char * 1),
        ("crctn_qtyz12", ctypes.c_char * 12),           # 정정수량
        ("_crctn_qtyz12", ctypes.c_char * 1),
        ("crctn_pricez10", ctypes.c_char * 10),         # 정정단가
        ("_crctn_pricez10", ctypes.c_char * 1),
        ("orgnl_order_noz10", ctypes.c_char * 10),      # 원주문번호
        ("_orgnl_order_noz10", ctypes.c_char * 1),
        ("all_part_typez1", ctypes.c_char * 1),          # 정정구분 (1:잔량전체, 2:일부수량)
        ("_all_part_typez1", ctypes.c_char * 1),
        ("trad_pswd_no_1z8", ctypes.c_char * 44),       # 거래비밀번호1 (해시 44자)
        ("_trad_pswd_no_1z8", ctypes.c_char * 1),
        ("trad_pswd_no_2z8", ctypes.c_char * 44),       # 거래비밀번호2 (해시 44자)
        ("_trad_pswd_no_2z8", ctypes.c_char * 1),
        ("sop_cnd_prz15", ctypes.c_char * 15),          # 정지조건가격
        ("_sop_cnd_prz15", ctypes.c_char * 1),
        ("rmt_mkt_cdz3", ctypes.c_char * 3),            # 요청시장코드
        ("_rmt_mkt_cdz3", ctypes.c_char * 1),
        ("sor_mkt_sli_ynz1", ctypes.c_char * 1),        # SOR시장분할여부
        ("_sor_mkt_sli_ynz1", ctypes.c_char * 1),
        ("sor_rule_cdz4", ctypes.c_char * 4),            # SOR룰코드
        ("_sor_rule_cdz4", ctypes.c_char * 1),
    ]


class CTc8103OutBlock(Structure):
    """주문 정정 출력 블록 C 구조체"""
    _fields_ = [
        ("orgnl_order_noz10", ctypes.c_char * 10),       # 원주문번호
        ("_orgnl_order_noz10", ctypes.c_char * 1),
        ("order_noz10", ctypes.c_char * 10),             # 주문번호
        ("_order_noz10", ctypes.c_char * 1),
        ("mom_order_noz10", ctypes.c_char * 10),         # 모주문번호
        ("_mom_order_noz10", ctypes.c_char * 1),
        ("issue_codez6", ctypes.c_char * 6),             # 후종목번호
        ("_issue_codez6", ctypes.c_char * 1),
        ("crctn_qtyz12", ctypes.c_char * 12),            # 정정수량
        ("_crctn_qtyz12", ctypes.c_char * 1),
        ("crctn_pricez10", ctypes.c_char * 10),          # 정정단가
        ("_crctn_pricez10", ctypes.c_char * 1),
        ("sor_fle_idz20", ctypes.c_char * 20),           # SOR파일ID
        ("_sor_fle_idz20", ctypes.c_char * 1),
        ("can_sor_ant_rt1z11", ctypes.c_char * 11),      # 취소KRX배분비율
        ("_can_sor_ant_rt1z11", ctypes.c_char * 1),
        ("can_sor_ant_rt2z11", ctypes.c_char * 11),      # 취소NXT배분비율
        ("_can_sor_ant_rt2z11", ctypes.c_char * 1),
        ("can_orr_qty1z18", ctypes.c_char * 18),         # KRX취소주문수량
        ("_can_orr_qty1z18", ctypes.c_char * 1),
        ("can_orr_qty2z18", ctypes.c_char * 18),         # NXT취소주문수량
        ("_can_orr_qty2z18", ctypes.c_char * 1),
        ("can_cld_mkt_orr_no1z10", ctypes.c_char * 10),  # KRX취소자시장주문번호
        ("_can_cld_mkt_orr_no1z10", ctypes.c_char * 1),
        ("can_cld_mkt_orr_no2z10", ctypes.c_char * 10),  # NXT취소자시장주문번호
        ("_can_cld_mkt_orr_no2z10", ctypes.c_char * 1),
    ]


# ==============================================================================
# Pydantic 모델 (사용자 친화적 인터페이스)
# ==============================================================================

class Tc8103InBlock(InBlock):
    """주문 정정 입력 블록

    Attributes:
        pswd_noz8: 계좌비밀번호 해시 (44자)
        issue_codez6: 종목번호 (6자리)
        crctn_qtyz12: 정정수량
        crctn_pricez10: 정정단가
        orgnl_order_noz10: 원주문번호 (정정할 주문번호)
        all_part_typez1: 정정구분 ("1":잔량전체, "2":일부수량)
        trad_pswd_no_1z8: 거래비밀번호1 해시 (44자)
        trad_pswd_no_2z8: 거래비밀번호2 해시 (44자)
    """

    C_STRUCT: ClassVar[Type[ctypes.Structure]] = CTc8103InBlock

    pswd_noz8: str = Field(min_length=44, max_length=44, description="계좌비밀번호 해시")
    issue_codez6: str = Field(min_length=6, max_length=6, description="종목번호")
    crctn_qtyz12: str = Field(max_length=12, description="정정수량")
    crctn_pricez10: str = Field(max_length=10, description="정정단가")
    orgnl_order_noz10: str = Field(max_length=10, description="원주문번호")
    all_part_typez1: str = Field(max_length=1, description="정정구분", default="1")
    trad_pswd_no_1z8: str = Field(min_length=44, max_length=44, description="거래비밀번호1 해시")
    trad_pswd_no_2z8: str = Field(min_length=44, max_length=44, description="거래비밀번호2 해시")
    sop_cnd_prz15: str = Field(max_length=15, description="정지조건가격", default="")
    rmt_mkt_cdz3: str = Field(max_length=3, description="요청시장코드", default="")
    sor_mkt_sli_ynz1: str = Field(max_length=1, description="SOR시장분할여부", default="")
    sor_rule_cdz4: str = Field(max_length=4, description="SOR룰코드", default="")


# ==============================================================================
# Output 구조체
# ==============================================================================

@dataclass
class Tc8103OutBlock(OutBlock):
    """주문 정정 출력 블록"""
    orgnl_order_noz10: str       # 원주문번호
    order_noz10: str             # 주문번호
    mom_order_noz10: str         # 모주문번호
    issue_codez6: str            # 후종목번호
    crctn_qtyz12: str            # 정정수량
    crctn_pricez10: str          # 정정단가
    sor_fle_idz20: str           # SOR파일ID
    can_sor_ant_rt1z11: str      # 취소KRX배분비율
    can_sor_ant_rt2z11: str      # 취소NXT배분비율
    can_orr_qty1z18: str         # KRX취소주문수량
    can_orr_qty2z18: str         # NXT취소주문수량
    can_cld_mkt_orr_no1z10: str  # KRX취소자시장주문번호
    can_cld_mkt_orr_no2z10: str  # NXT취소자시장주문번호


__all__ = [
    "CTc8103InBlock",
    "Tc8103InBlock",
    "CTc8103OutBlock",
    "Tc8103OutBlock",
]
