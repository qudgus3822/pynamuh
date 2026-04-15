"""주문/체결 조회 TR 구조체 정의 (주문_SPEC_20251128.md 기반)"""

from typing import ClassVar, Type
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field

from ..common import InBlock, OutBlock


# ==============================================================================
# C 구조체 정의
# ==============================================================================

class CTs8180InBlock(Structure):
    """주문/체결 조회 입력 블록 C 구조체"""
    _fields_ = [
        ("qry_obj_cdz1", ctypes.c_char * 1),           # 조회주체구분 (3:계좌별조회)
        ("_qry_obj_cdz1", ctypes.c_char * 1),
        ("pswd_noz44", ctypes.c_char * 44),             # 비밀번호
        ("_pswd_noz44", ctypes.c_char * 1),
        ("grp_noz4", ctypes.c_char * 4),                # 그룹번호 (0000)
        ("_grp_noz4", ctypes.c_char * 1),
        ("mkt_slctz1", ctypes.c_char * 1),              # 시장구분 (0:전체)
        ("_mkt_slctz1", ctypes.c_char * 1),
        ("ordr_dtz8", ctypes.c_char * 8),               # 주문일자 (YYYYMMDD)
        ("_ordr_dtz8", ctypes.c_char * 1),
        ("issue_codez12", ctypes.c_char * 12),          # 종목번호
        ("_issue_codez12", ctypes.c_char * 1),
        ("media_cdz2", ctypes.c_char * 2),              # 매체구분 (CC:전체)
        ("_media_cdz2", ctypes.c_char * 1),
        ("exec_cdz1", ctypes.c_char * 1),               # 체결구분 (0:전체, 1:미체결, 2:체결)
        ("_exec_cdz1", ctypes.c_char * 1),
        ("qry_seqz1", ctypes.c_char * 1),               # 조회순서 (0:번호, 1:모주문번호)
        ("_qry_seqz1", ctypes.c_char * 1),
        ("sort_cdz1", ctypes.c_char * 1),               # 정렬구분 (0:주문번호순, 1:역순)
        ("_sort_cdz1", ctypes.c_char * 1),
        ("buy_sell_cdz1", ctypes.c_char * 1),           # 매수도구분 (0:전체, 1:매도, 2:매수)
        ("_buy_sell_cdz1", ctypes.c_char * 1),
        ("credit_cdz1", ctypes.c_char * 1),             # 신용구분 (0:보통)
        ("_credit_cdz1", ctypes.c_char * 1),
        ("acct_cdz1", ctypes.c_char * 1),               # 계좌구분 (0:전체)
        ("_acct_cdz1", ctypes.c_char * 1),
        ("ordr_noz10", ctypes.c_char * 10),             # 주문번호
        ("_ordr_noz10", ctypes.c_char * 1),
        ("ctsz56", ctypes.c_char * 56),                 # CTS (연속조회 키)
        ("_ctsz56", ctypes.c_char * 1),
        ("trad_pswd_no_1z44", ctypes.c_char * 44),      # 거래비밀번호1
        ("_trad_pswd_no_1z44", ctypes.c_char * 1),
        ("trad_pswd_no_2z44", ctypes.c_char * 44),      # 거래비밀번호2
        ("_trad_pswd_no_2z44", ctypes.c_char * 1),
        ("ispageupz1", ctypes.c_char * 1),              # ISPAGEUP (다음화면: N, 없음: " ")
        ("_ispageupz1", ctypes.c_char * 1),
    ]


class CTs8180OutBlock(Structure):
    """주문/체결 조회 출력 블록 C 구조체 (헤더 - 요약 정보)"""
    _fields_ = [
        ("empl_namez20", ctypes.c_char * 20),           # 한글사원성명
        ("_empl_namez20", ctypes.c_char * 1),
        ("brnc_namez30", ctypes.c_char * 30),           # 한글지점명
        ("_brnc_namez30", ctypes.c_char * 1),
        ("buy_exec_qtyz14", ctypes.c_char * 14),        # 매수체결수량
        ("_buy_exec_qtyz14", ctypes.c_char * 1),
        ("buy_exec_amtz19", ctypes.c_char * 19),        # 매수체결금액
        ("_buy_exec_amtz19", ctypes.c_char * 1),
        ("sell_exec_qtyz14", ctypes.c_char * 14),       # 매도체결수량
        ("_sell_exec_qtyz14", ctypes.c_char * 1),
        ("sell_exec_amtz19", ctypes.c_char * 19),       # 매도체결금액
        ("_sell_exec_amtz19", ctypes.c_char * 1),
    ]


class CTs8180OutBlock1(Structure):
    """주문/체결 조회 출력 블록1 C 구조체 (상세 - 반복 최대 15건)"""
    _fields_ = [
        ("ordr_dtz8", ctypes.c_char * 8),               # 주문일자
        ("_ordr_dtz8", ctypes.c_char * 1),
        ("ordr_noz10", ctypes.c_char * 10),             # 주문번호
        ("_ordr_noz10", ctypes.c_char * 1),
        ("orig_ordr_noz10", ctypes.c_char * 10),        # 원주문번호
        ("_orig_ordr_noz10", ctypes.c_char * 1),
        ("acct_noz11", ctypes.c_char * 11),             # 계좌번호
        ("_acct_noz11", ctypes.c_char * 1),
        ("acct_namez20", ctypes.c_char * 20),           # 계좌명
        ("_acct_namez20", ctypes.c_char * 1),
        ("ordr_typez20", ctypes.c_char * 20),           # 주문구분 (현금매수, 현금매도 등)
        ("_ordr_typez20", ctypes.c_char * 1),
        ("trade_type_noz1", ctypes.c_char * 1),         # 매매구분번호
        ("_trade_type_noz1", ctypes.c_char * 1),
        ("trade_typez20", ctypes.c_char * 20),          # 매매구분 (보통, 시장가 등)
        ("_trade_typez20", ctypes.c_char * 1),
        ("trd_type_noz1", ctypes.c_char * 1),           # 거래구분번호
        ("_trd_type_noz1", ctypes.c_char * 1),
        ("trd_typez20", ctypes.c_char * 20),            # 거래구분
        ("_trd_typez20", ctypes.c_char * 1),
        ("issue_codez12", ctypes.c_char * 12),          # 종목번호
        ("_issue_codez12", ctypes.c_char * 1),
        ("issue_namez40", ctypes.c_char * 40),          # 종목명
        ("_issue_namez40", ctypes.c_char * 1),
        ("ordr_qtyz10", ctypes.c_char * 10),            # 주문수량
        ("_ordr_qtyz10", ctypes.c_char * 1),
        ("exec_qtyz10", ctypes.c_char * 10),            # 체결수량
        ("_exec_qtyz10", ctypes.c_char * 1),
        ("ordr_pricez12", ctypes.c_char * 12),          # 주문단가
        ("_ordr_pricez12", ctypes.c_char * 1),
        ("exec_avg_pricez12", ctypes.c_char * 12),      # 체결평균단가
        ("_exec_avg_pricez12", ctypes.c_char * 1),
        ("cncl_qtyz10", ctypes.c_char * 10),            # 정정취소수량
        ("_cncl_qtyz10", ctypes.c_char * 1),
        ("conf_qtyz10", ctypes.c_char * 10),            # 확인수량
        ("_conf_qtyz10", ctypes.c_char * 1),
        ("media_cdz12", ctypes.c_char * 12),            # 매체구분
        ("_media_cdz12", ctypes.c_char * 1),
        ("proc_emp_noz5", ctypes.c_char * 5),           # 처리사번
        ("_proc_emp_noz5", ctypes.c_char * 1),
        ("proc_tmz8", ctypes.c_char * 8),               # 처리시간
        ("_proc_tmz8", ctypes.c_char * 1),
        ("proc_trmz8", ctypes.c_char * 8),              # 처리단말
        ("_proc_trmz8", ctypes.c_char * 1),
        ("proc_typez12", ctypes.c_char * 12),           # 처리구분 (정상, 확인)
        ("_proc_typez12", ctypes.c_char * 1),
        ("rjct_cdz5", ctypes.c_char * 5),               # 거부코드
        ("_rjct_cdz5", ctypes.c_char * 1),
        ("cncl_pos_qtyz10", ctypes.c_char * 10),        # 정취가능수량
        ("_cncl_pos_qtyz10", ctypes.c_char * 1),
        ("mkt_cdz1", ctypes.c_char * 1),                # 시장구분
        ("_mkt_cdz1", ctypes.c_char * 1),
        ("shsll_typez20", ctypes.c_char * 20),          # 공매도구분
        ("_shsll_typez20", ctypes.c_char * 1),
        ("acct_pwdz8", ctypes.c_char * 8),              # 계좌비밀번호
        ("_acct_pwdz8", ctypes.c_char * 1),
        ("new_mkt_ordr_no1z10", ctypes.c_char * 10),    # 신규자시장주문번호1
        ("_new_mkt_ordr_no1z10", ctypes.c_char * 1),
        ("new_mkt_ordr_no2z10", ctypes.c_char * 10),    # 신규자시장주문번호2
        ("_new_mkt_ordr_no2z10", ctypes.c_char * 1),
        ("sor_mkt_ordr_noz10", ctypes.c_char * 10),     # SOR시장주문번호
        ("_sor_mkt_ordr_noz10", ctypes.c_char * 1),
        ("rmt_mkt_cdz3", ctypes.c_char * 3),            # 요청시장코드
        ("_rmt_mkt_cdz3", ctypes.c_char * 1),
        ("snd_mkt_cdz3", ctypes.c_char * 3),            # 전송시장코드
        ("_snd_mkt_cdz3", ctypes.c_char * 1),
        ("sor_mkt_sli_ynz1", ctypes.c_char * 1),        # SOR시장분할여부
        ("_sor_mkt_sli_ynz1", ctypes.c_char * 1),
        ("sop_cnd_prz15", ctypes.c_char * 15),          # 정지조건가격
        ("_sop_cnd_prz15", ctypes.c_char * 1),
        ("rjct_qtyz18", ctypes.c_char * 18),            # 거부수량
        ("_rjct_qtyz18", ctypes.c_char * 1),
        ("rmt_mkt_namez50", ctypes.c_char * 50),        # 요청시장명
        ("_rmt_mkt_namez50", ctypes.c_char * 1),
        ("sop_cnd_pr_reach_ynz1", ctypes.c_char * 1),   # 정지조건가격도달여부
        ("_sop_cnd_pr_reach_ynz1", ctypes.c_char * 1),
        ("ioc_cncl_qtyz8", ctypes.c_char * 8),          # 취소수량 (IOC시장가 자동취소)
        ("_ioc_cncl_qtyz8", ctypes.c_char * 1),
    ]


class CTs8180OutBlock2(Structure):
    """주문/체결 조회 출력 블록2 C 구조체 (CTS 연속조회)"""
    _fields_ = [
        ("ctsz56", ctypes.c_char * 56),                 # CTS
        ("_ctsz56", ctypes.c_char * 1),
        ("next_ynz1", ctypes.c_char * 1),               # 다음버튼유무
        ("_next_ynz1", ctypes.c_char * 1),
    ]


# ==============================================================================
# Pydantic 모델 (사용자 친화적 인터페이스)
# ==============================================================================

class Ts8180InBlock(InBlock):
    """주문/체결 조회 입력 블록

    Attributes:
        qry_obj_cdz1: 조회주체구분 (3:계좌별조회)
        pswd_noz44: 비밀번호 (해시 44자)
        grp_noz4: 그룹번호 (0000)
        mkt_slctz1: 시장구분 (0:전체)
        ordr_dtz8: 주문일자 (YYYYMMDD)
        issue_codez12: 종목번호
        media_cdz2: 매체구분 (CC:전체)
        exec_cdz1: 체결구분 (0:전체, 1:미체결, 2:체결)
        qry_seqz1: 조회순서 (0:번호, 1:모주문번호)
        sort_cdz1: 정렬구분 (0:주문번호순, 1:역순)
        buy_sell_cdz1: 매수도구분 (0:전체, 1:매도, 2:매수)
        credit_cdz1: 신용구분 (0:보통)
        acct_cdz1: 계좌구분 (0:전체)
        ordr_noz10: 주문번호
        ctsz56: CTS 연속조회 키
        trad_pswd_no_1z44: 거래비밀번호1 (해시 44자)
        trad_pswd_no_2z44: 거래비밀번호2 (해시 44자)
        ispageupz1: ISPAGEUP (다음화면: N, 없음: " ")
    """

    C_STRUCT: ClassVar[Type[ctypes.Structure]] = CTs8180InBlock

    qry_obj_cdz1: str = Field(default="3", max_length=1, description="조회주체구분")
    pswd_noz44: str = Field(min_length=44, max_length=44, description="비밀번호 해시")
    grp_noz4: str = Field(default="0000", max_length=4, description="그룹번호")
    mkt_slctz1: str = Field(default="0", max_length=1, description="시장구분")
    ordr_dtz8: str = Field(min_length=8, max_length=8, description="주문일자 (YYYYMMDD)")
    issue_codez12: str = Field(default="", max_length=12, description="종목번호")
    media_cdz2: str = Field(default="CC", max_length=2, description="매체구분")
    exec_cdz1: str = Field(default="0", max_length=1, description="체결구분")
    qry_seqz1: str = Field(default="0", max_length=1, description="조회순서")
    sort_cdz1: str = Field(default="0", max_length=1, description="정렬구분")
    buy_sell_cdz1: str = Field(default="0", max_length=1, description="매수도구분")
    credit_cdz1: str = Field(default="0", max_length=1, description="신용구분")
    acct_cdz1: str = Field(default="0", max_length=1, description="계좌구분")
    ordr_noz10: str = Field(default="", max_length=10, description="주문번호")
    ctsz56: str = Field(default="", max_length=56, description="CTS 연속조회 키")
    trad_pswd_no_1z44: str = Field(min_length=44, max_length=44, description="거래비밀번호1 해시")
    trad_pswd_no_2z44: str = Field(min_length=44, max_length=44, description="거래비밀번호2 해시")
    ispageupz1: str = Field(default=" ", max_length=1, description="ISPAGEUP")


# ==============================================================================
# Output 구조체
# ==============================================================================

@dataclass
class Ts8180OutBlock(OutBlock):
    """주문/체결 조회 OutBlock (요약 정보)"""
    empl_namez20: str           # 한글사원성명
    brnc_namez30: str           # 한글지점명
    buy_exec_qtyz14: str        # 매수체결수량
    buy_exec_amtz19: str        # 매수체결금액
    sell_exec_qtyz14: str       # 매도체결수량
    sell_exec_amtz19: str       # 매도체결금액


@dataclass
class Ts8180OutBlock1(OutBlock):
    """주문/체결 조회 OutBlock1 (상세 체결 내역 - 반복 최대 15건)"""
    ordr_dtz8: str              # 주문일자
    ordr_noz10: str             # 주문번호
    orig_ordr_noz10: str        # 원주문번호
    acct_noz11: str             # 계좌번호
    acct_namez20: str           # 계좌명
    ordr_typez20: str           # 주문구분 (현금매수, 현금매도 등)
    trade_type_noz1: str        # 매매구분번호
    trade_typez20: str          # 매매구분 (보통, 시장가 등)
    trd_type_noz1: str          # 거래구분번호
    trd_typez20: str            # 거래구분
    issue_codez12: str          # 종목번호
    issue_namez40: str          # 종목명
    ordr_qtyz10: str            # 주문수량
    exec_qtyz10: str            # 체결수량
    ordr_pricez12: str          # 주문단가
    exec_avg_pricez12: str      # 체결평균단가
    cncl_qtyz10: str            # 정정취소수량
    conf_qtyz10: str            # 확인수량
    media_cdz12: str            # 매체구분
    proc_emp_noz5: str          # 처리사번
    proc_tmz8: str              # 처리시간
    proc_trmz8: str             # 처리단말
    proc_typez12: str           # 처리구분 (정상, 확인)
    rjct_cdz5: str              # 거부코드
    cncl_pos_qtyz10: str        # 정취가능수량
    mkt_cdz1: str               # 시장구분
    shsll_typez20: str          # 공매도구분
    acct_pwdz8: str             # 계좌비밀번호
    new_mkt_ordr_no1z10: str    # 신규자시장주문번호1
    new_mkt_ordr_no2z10: str    # 신규자시장주문번호2
    sor_mkt_ordr_noz10: str     # SOR시장주문번호
    rmt_mkt_cdz3: str           # 요청시장코드
    snd_mkt_cdz3: str           # 전송시장코드
    sor_mkt_sli_ynz1: str       # SOR시장분할여부
    sop_cnd_prz15: str          # 정지조건가격
    rjct_qtyz18: str            # 거부수량
    rmt_mkt_namez50: str        # 요청시장명
    sop_cnd_pr_reach_ynz1: str  # 정지조건가격도달여부
    ioc_cncl_qtyz8: str         # 취소수량


@dataclass
class Ts8180OutBlock2(OutBlock):
    """주문/체결 조회 OutBlock2 (CTS 연속조회)"""
    ctsz56: str                 # CTS
    next_ynz1: str              # 다음버튼유무


__all__ = [
    "CTs8180InBlock",
    "Ts8180InBlock",
    "CTs8180OutBlock",
    "Ts8180OutBlock",
    "CTs8180OutBlock1",
    "Ts8180OutBlock1",
    "CTs8180OutBlock2",
    "Ts8180OutBlock2",
]
