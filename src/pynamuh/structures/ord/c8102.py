"""주식 매수/매도 주문 TR 구조체 정의 (trio_ord.h c8102 기반)

Note:
    c8102는 샘플 코드에서 사용하는 주문 TR입니다.
    c8101과 거의 동일하나 shsll_pos_flagz1(공매도가능여부) 필드가 없습니다.
"""

from typing import ClassVar, Type
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field

from ..common import InBlock, OutBlock


# ==============================================================================
# C 구조체 정의 (trio_ord.h 기반)
# ==============================================================================

class CTc8102InBlock(Structure):
    """주식 매수/매도 주문 입력 블록 C 구조체 (c8102)"""
    _fields_ = [
        ("pswd_noz8", ctypes.c_char * 44),             # 계좌비밀번호 (해시 44자)
        ("_pswd_noz8", ctypes.c_char * 1),
        ("issue_codez6", ctypes.c_char * 6),            # 종목번호 (6자리)
        ("_issue_codez6", ctypes.c_char * 1),
        ("order_qtyz12", ctypes.c_char * 12),           # 주문수량
        ("_order_qtyz12", ctypes.c_char * 1),
        ("order_unit_pricez10", ctypes.c_char * 10),    # 주문단가
        ("_order_unit_pricez10", ctypes.c_char * 1),
        ("trade_typez2", ctypes.c_char * 2),            # 매매유형 (00:지정가, 03:시장가 등)
        ("_trade_typez2", ctypes.c_char * 1),
        ("trad_pswd_no_1z8", ctypes.c_char * 44),       # 거래비밀번호1 (해시 44자)
        ("_trad_pswd_no_1z8", ctypes.c_char * 1),
        ("trad_pswd_no_2z8", ctypes.c_char * 44),       # 거래비밀번호2 (해시 44자)
        ("_trad_pswd_no_2z8", ctypes.c_char * 1),
        ("sop_cnd_prz15", ctypes.c_char * 15),          # 정지조건가격
        ("_sop_cnd_prz15", ctypes.c_char * 1),
        ("rmt_mkt_cdz3", ctypes.c_char * 3),            # 요청시장코드 (SOR/KRX/NXT)
        ("_rmt_mkt_cdz3", ctypes.c_char * 1),
        ("sor_mkt_sli_ynz1", ctypes.c_char * 1),        # SOR시장분할여부
        ("_sor_mkt_sli_ynz1", ctypes.c_char * 1),
        ("sor_rule_cdz4", ctypes.c_char * 4),            # SOR룰코드
        ("_sor_rule_cdz4", ctypes.c_char * 1),
        ("mkt_insd_cor_req_ynz1", ctypes.c_char * 1),   # 시장내정정신청여부
        ("_mkt_insd_cor_req_ynz1", ctypes.c_char * 1),
    ]


class CTc8102OutBlock(Structure):
    """주식 매수/매도 주문 출력 블록 C 구조체 (c8102)"""
    _fields_ = [
        ("order_noz10", ctypes.c_char * 10),             # 주문번호
        ("_order_noz10", ctypes.c_char * 1),
        ("order_qtyz12", ctypes.c_char * 12),            # 주문수량
        ("_order_qtyz12", ctypes.c_char * 1),
        ("order_unit_pricez10", ctypes.c_char * 10),     # 주문단가
        ("_order_unit_pricez10", ctypes.c_char * 1),
        ("sor_fle_idz20", ctypes.c_char * 20),           # SOR파일ID
        ("_sor_fle_idz20", ctypes.c_char * 1),
        ("sor_ant_rt1z11", ctypes.c_char * 11),          # KRX배분비율
        ("_sor_ant_rt1z11", ctypes.c_char * 1),
        ("sor_ant_rt2z11", ctypes.c_char * 11),          # NXT배분비율
        ("_sor_ant_rt2z11", ctypes.c_char * 1),
        ("orr_qty1z18", ctypes.c_char * 18),             # KRX주문수량
        ("_orr_qty1z18", ctypes.c_char * 1),
        ("orr_qty2z18", ctypes.c_char * 18),             # NXT주문수량
        ("_orr_qty2z18", ctypes.c_char * 1),
        ("anw_cld_mkt_orr_no1z10", ctypes.c_char * 10),  # KRX시장주문번호
        ("_anw_cld_mkt_orr_no1z10", ctypes.c_char * 1),
        ("anw_cld_mkt_orr_no2z10", ctypes.c_char * 10),  # NXT시장주문번호
        ("_anw_cld_mkt_orr_no2z10", ctypes.c_char * 1),
    ]


# ==============================================================================
# Pydantic 모델 (사용자 친화적 인터페이스)
# ==============================================================================

class Tc8102InBlock(InBlock):
    """주식 매수/매도 주문 입력 블록 (c8102)

    Attributes:
        pswd_noz8: 계좌비밀번호 해시 (44자, get_account_hash_password()로 생성)
        issue_codez6: 종목번호 (6자리, 예: "005930")
        order_qtyz12: 주문수량
        order_unit_pricez10: 주문단가 (시장가 주문 시 "0")
        trade_typez2: 매매유형 ("00":지정가, "03":시장가)
        trad_pswd_no_1z8: 거래비밀번호1 해시 (44자, get_order_hash_password()로 생성)
        trad_pswd_no_2z8: 거래비밀번호2 해시 (44자, get_order_hash_password()로 생성)
        sop_cnd_prz15: 정지조건가격 (스톱지정가 주문 시만 사용)
        rmt_mkt_cdz3: 요청시장코드 ("SOR":SOR, "KRX":KRX, "NXT":NXT)
        sor_mkt_sli_ynz1: SOR시장분할여부 ("Y"/"N")
        sor_rule_cdz4: SOR룰코드 ("A"/"B"/"_":미사용)
        mkt_insd_cor_req_ynz1: 시장내정정신청여부 ("N"/"Y")
    """

    C_STRUCT: ClassVar[Type[ctypes.Structure]] = CTc8102InBlock

    pswd_noz8: str = Field(min_length=44, max_length=44, description="계좌비밀번호 해시")
    issue_codez6: str = Field(min_length=6, max_length=6, description="종목번호")
    order_qtyz12: str = Field(max_length=12, description="주문수량")
    order_unit_pricez10: str = Field(max_length=10, description="주문단가")
    trade_typez2: str = Field(max_length=2, description="매매유형", default="00")
    trad_pswd_no_1z8: str = Field(min_length=44, max_length=44, description="거래비밀번호1 해시")
    trad_pswd_no_2z8: str = Field(min_length=44, max_length=44, description="거래비밀번호2 해시")
    sop_cnd_prz15: str = Field(max_length=15, description="정지조건가격", default="")
    rmt_mkt_cdz3: str = Field(max_length=3, description="요청시장코드", default="KRX")
    sor_mkt_sli_ynz1: str = Field(max_length=1, description="SOR시장분할여부", default="")
    sor_rule_cdz4: str = Field(max_length=4, description="SOR룰코드", default="")
    mkt_insd_cor_req_ynz1: str = Field(max_length=1, description="시장내정정신청여부", default="N")


# ==============================================================================
# Output 구조체
# ==============================================================================

@dataclass
class Tc8102OutBlock(OutBlock):
    """주식 매수/매도 주문 출력 블록 (c8102)"""
    order_noz10: str             # 주문번호
    order_qtyz12: str            # 주문수량
    order_unit_pricez10: str     # 주문단가
    sor_fle_idz20: str           # SOR파일ID
    sor_ant_rt1z11: str          # KRX배분비율
    sor_ant_rt2z11: str          # NXT배분비율
    orr_qty1z18: str             # KRX주문수량
    orr_qty2z18: str             # NXT주문수량
    anw_cld_mkt_orr_no1z10: str  # KRX시장주문번호
    anw_cld_mkt_orr_no2z10: str  # NXT시장주문번호


__all__ = [
    "CTc8102InBlock",
    "Tc8102InBlock",
    "CTc8102OutBlock",
    "Tc8102OutBlock",
]
