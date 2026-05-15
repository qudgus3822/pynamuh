"""주식 현재가 조회 TR 구조체 정의 (trio_inv.h IVWUTKMST04 기반)

주식 단일종목 현재가/호가/투자정보 조회 서비스.
계좌번호와 무관하므로 nAccountIndex=0으로 호출한다.

서비스 코드(TR):
    - IVWUTKMST04           : KRX 기본
    - IVWUTKMST04.UNT       : 통합시세
    - IVWUTKMST04.KRX       : 한국거래소(KRX)
    - IVWUTKMST04.NXT       : 대체거래소(NXT)

Reference:
    - pynamuh/sample/VC++/trio_inv.h (1317-1545줄): C 구조체 원본 정의
    - pynamuh/sample/VC++/WMCALOADERDlg.cpp (413-471, 698-744줄): 호출/응답 처리 예시
"""

from typing import ClassVar, Type
from dataclasses import dataclass
import ctypes
from ctypes import Structure

from pydantic import Field

from ..common import InBlock, OutBlock


# ==============================================================================
# C 구조체 정의 (trio_inv.h 기반)
# ==============================================================================

class CTIVWUTKMST04InBlock(Structure):
    """주식 현재가 조회 입력 블록 C 구조체"""
    _fields_ = [
        ("form_lang", ctypes.c_char * 1),       # 한영구분 (k:KOREAN, e:ENGLISH)
        ("_form_lang", ctypes.c_char * 1),
        ("shrn_iscd", ctypes.c_char * 6),       # 종목코드 (6자리)
        ("_shrn_iscd", ctypes.c_char * 1),
    ]


class CTIVWUTKMST04OutBlock1(Structure):
    """주식 현재가 조회 출력 블록1 C 구조체 (종목마스터 기본자료, 단일출력)"""
    _fields_ = [
        ("shrn_iscd", ctypes.c_char * 6),                ("_shrn_iscd", ctypes.c_char * 1),                # 종목코드
        ("hts_isnm", ctypes.c_char * 41),                ("_hts_isnm", ctypes.c_char * 1),                 # 종목명
        ("stck_prpr", ctypes.c_char * 10),               ("_stck_prpr", ctypes.c_char * 1),                # 현재가
        ("prdy_vrss_sign", ctypes.c_char * 1),           ("_prdy_vrss_sign", ctypes.c_char * 1),           # 전일대비부호
        ("prdy_vrss", ctypes.c_char * 10),               ("_prdy_vrss", ctypes.c_char * 1),                # 전일대비
        ("prdy_ctrt", ctypes.c_char * 5),                ("_prdy_ctrt", ctypes.c_char * 1),                # 등락률
        ("askp", ctypes.c_char * 10),                    ("_askp", ctypes.c_char * 1),                     # 매도호가
        ("bidp", ctypes.c_char * 10),                    ("_bidp", ctypes.c_char * 1),                     # 매수호가
        ("acml_vol", ctypes.c_char * 12),                ("_acml_vol", ctypes.c_char * 1),                 # 누적거래량
        ("vol_rate", ctypes.c_char * 6),                 ("_vol_rate", ctypes.c_char * 1),                 # 거래량비율
        ("move_rate", ctypes.c_char * 6),                ("_move_rate", ctypes.c_char * 1),                # 회전율
        ("acml_tr_pbmn", ctypes.c_char * 18),            ("_acml_tr_pbmn", ctypes.c_char * 1),             # 누적거래대금
        ("stck_mxpr", ctypes.c_char * 10),               ("_stck_mxpr", ctypes.c_char * 1),                # 상한가
        ("stck_hgpr", ctypes.c_char * 10),               ("_stck_hgpr", ctypes.c_char * 1),                # 고가
        ("stck_oprc", ctypes.c_char * 10),               ("_stck_oprc", ctypes.c_char * 1),                # 시가
        ("stck_oprc_sign", ctypes.c_char * 1),           ("_stck_oprc_sign", ctypes.c_char * 1),           # 시가전일대비부호
        ("stck_oprc_vrss", ctypes.c_char * 10),          ("_stck_oprc_vrss", ctypes.c_char * 1),           # 시가전일대비
        ("stck_lwpr", ctypes.c_char * 10),               ("_stck_lwpr", ctypes.c_char * 1),                # 저가
        ("stck_llam", ctypes.c_char * 10),               ("_stck_llam", ctypes.c_char * 1),                # 하한가
        ("hoga_bsop_hour", ctypes.c_char * 8),           ("_hoga_bsop_hour", ctypes.c_char * 1),           # 호가시간
        ("askp1", ctypes.c_char * 10),                   ("_askp1", ctypes.c_char * 1),                    # 매도호가1
        ("askp2", ctypes.c_char * 10),                   ("_askp2", ctypes.c_char * 1),                    # 매도호가2
        ("askp3", ctypes.c_char * 10),                   ("_askp3", ctypes.c_char * 1),                    # 매도호가3
        ("askp4", ctypes.c_char * 10),                   ("_askp4", ctypes.c_char * 1),                    # 매도호가4
        ("askp5", ctypes.c_char * 10),                   ("_askp5", ctypes.c_char * 1),                    # 매도호가5
        ("askp6", ctypes.c_char * 10),                   ("_askp6", ctypes.c_char * 1),                    # 매도호가6
        ("askp7", ctypes.c_char * 10),                   ("_askp7", ctypes.c_char * 1),                    # 매도호가7
        ("askp8", ctypes.c_char * 10),                   ("_askp8", ctypes.c_char * 1),                    # 매도호가8
        ("askp9", ctypes.c_char * 10),                   ("_askp9", ctypes.c_char * 1),                    # 매도호가9
        ("askp10", ctypes.c_char * 10),                  ("_askp10", ctypes.c_char * 1),                   # 매도호가10
        ("bidp1", ctypes.c_char * 10),                   ("_bidp1", ctypes.c_char * 1),                    # 매수호가1
        ("bidp2", ctypes.c_char * 10),                   ("_bidp2", ctypes.c_char * 1),                    # 매수호가2
        ("bidp3", ctypes.c_char * 10),                   ("_bidp3", ctypes.c_char * 1),                    # 매수호가3
        ("bidp4", ctypes.c_char * 10),                   ("_bidp4", ctypes.c_char * 1),                    # 매수호가4
        ("bidp5", ctypes.c_char * 10),                   ("_bidp5", ctypes.c_char * 1),                    # 매수호가5
        ("bidp6", ctypes.c_char * 10),                   ("_bidp6", ctypes.c_char * 1),                    # 매수호가6
        ("bidp7", ctypes.c_char * 10),                   ("_bidp7", ctypes.c_char * 1),                    # 매수호가7
        ("bidp8", ctypes.c_char * 10),                   ("_bidp8", ctypes.c_char * 1),                    # 매수호가8
        ("bidp9", ctypes.c_char * 10),                   ("_bidp9", ctypes.c_char * 1),                    # 매수호가9
        ("bidp10", ctypes.c_char * 10),                  ("_bidp10", ctypes.c_char * 1),                   # 매수호가10
        ("askp_rsqn1", ctypes.c_char * 12),              ("_askp_rsqn1", ctypes.c_char * 1),               # 매도호가잔량1
        ("askp_rsqn2", ctypes.c_char * 12),              ("_askp_rsqn2", ctypes.c_char * 1),               # 매도호가잔량2
        ("askp_rsqn3", ctypes.c_char * 12),              ("_askp_rsqn3", ctypes.c_char * 1),               # 매도호가잔량3
        ("askp_rsqn4", ctypes.c_char * 12),              ("_askp_rsqn4", ctypes.c_char * 1),               # 매도호가잔량4
        ("askp_rsqn5", ctypes.c_char * 12),              ("_askp_rsqn5", ctypes.c_char * 1),               # 매도호가잔량5
        ("askp_rsqn6", ctypes.c_char * 12),              ("_askp_rsqn6", ctypes.c_char * 1),               # 매도호가잔량6
        ("askp_rsqn7", ctypes.c_char * 12),              ("_askp_rsqn7", ctypes.c_char * 1),               # 매도호가잔량7
        ("askp_rsqn8", ctypes.c_char * 12),              ("_askp_rsqn8", ctypes.c_char * 1),               # 매도호가잔량8
        ("askp_rsqn9", ctypes.c_char * 12),              ("_askp_rsqn9", ctypes.c_char * 1),               # 매도호가잔량9
        ("askp_rsqn10", ctypes.c_char * 12),             ("_askp_rsqn10", ctypes.c_char * 1),              # 매도호가잔량10
        ("bidp_rsqn1", ctypes.c_char * 12),              ("_bidp_rsqn1", ctypes.c_char * 1),               # 매수호가잔량1
        ("bidp_rsqn2", ctypes.c_char * 12),              ("_bidp_rsqn2", ctypes.c_char * 1),               # 매수호가잔량2
        ("bidp_rsqn3", ctypes.c_char * 12),              ("_bidp_rsqn3", ctypes.c_char * 1),               # 매수호가잔량3
        ("bidp_rsqn4", ctypes.c_char * 12),              ("_bidp_rsqn4", ctypes.c_char * 1),               # 매수호가잔량4
        ("bidp_rsqn5", ctypes.c_char * 12),              ("_bidp_rsqn5", ctypes.c_char * 1),               # 매수호가잔량5
        ("bidp_rsqn6", ctypes.c_char * 12),              ("_bidp_rsqn6", ctypes.c_char * 1),               # 매수호가잔량6
        ("bidp_rsqn7", ctypes.c_char * 12),              ("_bidp_rsqn7", ctypes.c_char * 1),               # 매수호가잔량7
        ("bidp_rsqn8", ctypes.c_char * 12),              ("_bidp_rsqn8", ctypes.c_char * 1),               # 매수호가잔량8
        ("bidp_rsqn9", ctypes.c_char * 12),              ("_bidp_rsqn9", ctypes.c_char * 1),               # 매수호가잔량9
        ("bidp_rsqn10", ctypes.c_char * 12),             ("_bidp_rsqn10", ctypes.c_char * 1),              # 매수호가잔량10
        ("total_askp_rsqn", ctypes.c_char * 12),         ("_total_askp_rsqn", ctypes.c_char * 1),          # 총매도잔량
        ("total_bidp_rsqn", ctypes.c_char * 12),         ("_total_bidp_rsqn", ctypes.c_char * 1),          # 총매수잔량
        ("ovtm_askp_rsqn", ctypes.c_char * 12),          ("_ovtm_askp_rsqn", ctypes.c_char * 1),           # 시간외매도잔량
        ("ovtm_bidp_rsqn", ctypes.c_char * 12),          ("_ovtm_bidp_rsqn", ctypes.c_char * 1),           # 시간외매수잔량
        ("pvt_scnd_dmrs", ctypes.c_char * 10),           ("_pvt_scnd_dmrs", ctypes.c_char * 1),            # 피봇2차저항선
        ("pvt_frst_dmrs", ctypes.c_char * 10),           ("_pvt_frst_dmrs", ctypes.c_char * 1),            # 피봇1차저항선
        ("pvt_pont_val", ctypes.c_char * 10),            ("_pvt_pont_val", ctypes.c_char * 1),             # 피봇값
        ("pvt_frst_dmsp", ctypes.c_char * 10),           ("_pvt_frst_dmsp", ctypes.c_char * 1),            # 피봇1차지지선
        ("pvt_scnd_dmsp", ctypes.c_char * 10),           ("_pvt_scnd_dmsp", ctypes.c_char * 1),            # 피봇2차지지선
        ("mrkt_div_isnm", ctypes.c_char * 6),            ("_mrkt_div_isnm", ctypes.c_char * 1),            # 코스피/코스닥구분
        ("bstp_kor_isnm", ctypes.c_char * 40),           ("_bstp_kor_isnm", ctypes.c_char * 1),            # 업종명
        ("bstp_cls_code", ctypes.c_char * 6),            ("_bstp_cls_code", ctypes.c_char * 1),            # 업종코드
        ("avls_scal_isnm", ctypes.c_char * 6),           ("_avls_scal_isnm", ctypes.c_char * 1),           # 자본금규모
        ("stac_month", ctypes.c_char * 16),              ("_stac_month", ctypes.c_char * 1),               # 결산월
        ("marcket1z16", ctypes.c_char * 16),             ("_marcket1z16", ctypes.c_char * 1),              # 시장가치1
        ("marcket2z16", ctypes.c_char * 16),             ("_marcket2z16", ctypes.c_char * 1),              # 시장가치2
        ("marcket3z16", ctypes.c_char * 16),             ("_marcket3z16", ctypes.c_char * 1),              # 시장가치3
        ("marcket4z16", ctypes.c_char * 16),             ("_marcket4z16", ctypes.c_char * 1),              # 시장가치4
        ("marcket5z16", ctypes.c_char * 16),             ("_marcket5z16", ctypes.c_char * 1),              # 시장가치5
        ("marcket6z16", ctypes.c_char * 16),             ("_marcket6z16", ctypes.c_char * 1),              # 시장가치6
        ("cb_text", ctypes.c_char * 6),                  ("_cb_text", ctypes.c_char * 1),                  # CB발동
        ("stck_fcam", ctypes.c_char * 10),               ("_stck_fcam", ctypes.c_char * 1),                # 액면가
        ("prdy_clpr_title", ctypes.c_char * 12),         ("_prdy_clpr_title", ctypes.c_char * 1),          # 전일종가타이틀
        ("stck_prdy_clpr", ctypes.c_char * 10),          ("_stck_prdy_clpr", ctypes.c_char * 1),           # 전일종가
        ("stck_sspr", ctypes.c_char * 10),               ("_stck_sspr", ctypes.c_char * 1),                # 대용가
        ("gongpricez7", ctypes.c_char * 7),              ("_gongpricez7", ctypes.c_char * 1),              # 공모가
        ("d5_hgpr", ctypes.c_char * 10),                 ("_d5_hgpr", ctypes.c_char * 1),                  # 5일고가
        ("d5_lwpr", ctypes.c_char * 10),                 ("_d5_lwpr", ctypes.c_char * 1),                  # 5일저가
        ("d20_hgpr", ctypes.c_char * 10),                ("_d20_hgpr", ctypes.c_char * 1),                 # 20일고가
        ("d20_lwpr", ctypes.c_char * 10),                ("_d20_lwpr", ctypes.c_char * 1),                 # 20일저가
        ("w52_hgpr", ctypes.c_char * 10),                ("_w52_hgpr", ctypes.c_char * 1),                 # 52주최고가
        ("w52_hgpr_date", ctypes.c_char * 4),            ("_w52_hgpr_date", ctypes.c_char * 1),            # 52주최고가일자
        ("w52_lwpr", ctypes.c_char * 10),                ("_w52_lwpr", ctypes.c_char * 1),                 # 52주최저가
        ("w52_lwpr_date", ctypes.c_char * 4),            ("_w52_lwpr_date", ctypes.c_char * 1),            # 52주최저가일자
        ("move_stcn", ctypes.c_char * 12),               ("_move_stcn", ctypes.c_char * 1),                # 유통주식수
        ("lstn_stcn_unit3", ctypes.c_char * 12),         ("_lstn_stcn_unit3", ctypes.c_char * 1),          # 상장주식수
        ("hts_avls", ctypes.c_char * 12),                ("_hts_avls", ctypes.c_char * 1),                 # 시가총액
        ("memb_bsop_hour", ctypes.c_char * 5),           ("_memb_bsop_hour", ctypes.c_char * 1),           # 시간
        ("seln_mbcr_name1", ctypes.c_char * 6),          ("_seln_mbcr_name1", ctypes.c_char * 1),          # 매도거래원1
        ("shnu_mbcr_name1", ctypes.c_char * 6),          ("_shnu_mbcr_name1", ctypes.c_char * 1),          # 매수거래원1
        ("seln_qty1", ctypes.c_char * 12),               ("_seln_qty1", ctypes.c_char * 1),                # 매도거래원수량1
        ("shnu_qty1", ctypes.c_char * 12),               ("_shnu_qty1", ctypes.c_char * 1),                # 매수거래원수량1
        ("seln_mbcr_name2", ctypes.c_char * 6),          ("_seln_mbcr_name2", ctypes.c_char * 1),          # 매도거래원2
        ("shnu_mbcr_name2", ctypes.c_char * 6),          ("_shnu_mbcr_name2", ctypes.c_char * 1),          # 매수거래원2
        ("seln_qty2", ctypes.c_char * 12),               ("_seln_qty2", ctypes.c_char * 1),                # 매도거래원수량2
        ("shnu_qty2", ctypes.c_char * 12),               ("_shnu_qty2", ctypes.c_char * 1),                # 매수거래원수량2
        ("seln_mbcr_name3", ctypes.c_char * 6),          ("_seln_mbcr_name3", ctypes.c_char * 1),          # 매도거래원3
        ("shnu_mbcr_name3", ctypes.c_char * 6),          ("_shnu_mbcr_name3", ctypes.c_char * 1),          # 매수거래원3
        ("seln_qty3", ctypes.c_char * 12),               ("_seln_qty3", ctypes.c_char * 1),                # 매도거래원수량3
        ("shnu_qty3", ctypes.c_char * 12),               ("_shnu_qty3", ctypes.c_char * 1),                # 매수거래원수량3
        ("seln_mbcr_name4", ctypes.c_char * 6),          ("_seln_mbcr_name4", ctypes.c_char * 1),          # 매도거래원4
        ("shnu_mbcr_name4", ctypes.c_char * 6),          ("_shnu_mbcr_name4", ctypes.c_char * 1),          # 매수거래원4
        ("seln_qty4", ctypes.c_char * 12),               ("_seln_qty4", ctypes.c_char * 1),                # 매도거래원수량4
        ("shnu_qty4", ctypes.c_char * 12),               ("_shnu_qty4", ctypes.c_char * 1),                # 매수거래원수량4
        ("seln_mbcr_name5", ctypes.c_char * 6),          ("_seln_mbcr_name5", ctypes.c_char * 1),          # 매도거래원5
        ("shnu_mbcr_name5", ctypes.c_char * 6),          ("_shnu_mbcr_name5", ctypes.c_char * 1),          # 매수거래원5
        ("seln_qty5", ctypes.c_char * 12),               ("_seln_qty5", ctypes.c_char * 1),                # 매도거래원수량5
        ("shnu_qty5", ctypes.c_char * 12),               ("_shnu_qty5", ctypes.c_char * 1),                # 매수거래원수량5
        ("glob_seln_qty", ctypes.c_char * 12),           ("_glob_seln_qty", ctypes.c_char * 1),            # 매도외국인거래량
        ("glob_shnu_qty", ctypes.c_char * 12),           ("_glob_shnu_qty", ctypes.c_char * 1),            # 매수외국인거래량
        ("for_hour", ctypes.c_char * 6),                 ("_for_hour", ctypes.c_char * 1),                 # 외국인시간
        ("for_rate", ctypes.c_char * 5),                 ("_for_rate", ctypes.c_char * 1),                 # 외국인소진율
        ("crdt_stlm_date", ctypes.c_char * 4),           ("_crdt_stlm_date", ctypes.c_char * 1),           # 신용결제일
        ("crdt_rmnd_rate", ctypes.c_char * 5),           ("_crdt_rmnd_rate", ctypes.c_char * 1),           # 잔고비율(%)
        ("yu_date", ctypes.c_char * 4),                  ("_yu_date", ctypes.c_char * 1),                  # 유상증자일
        ("mu_date", ctypes.c_char * 4),                  ("_mu_date", ctypes.c_char * 1),                  # 무상증자일
        ("yu_rate", ctypes.c_char * 5),                  ("_yu_rate", ctypes.c_char * 1),                  # 유상증자비율
        ("mu_rate", ctypes.c_char * 5),                  ("_mu_rate", ctypes.c_char * 1),                  # 무상증자비율
        ("frgn_ntby_vol", ctypes.c_char * 10),           ("_frgn_ntby_vol", ctypes.c_char * 1),            # 외국인순매수수량
        ("jasa", ctypes.c_char * 1),                     ("_jasa", ctypes.c_char * 1),                     # 자사주
        ("stck_lstn_date", ctypes.c_char * 8),           ("_stck_lstn_date", ctypes.c_char * 1),           # 상장일
        ("dae_rate", ctypes.c_char * 5),                 ("_dae_rate", ctypes.c_char * 1),                 # 대차잔고비율
        ("dae_date", ctypes.c_char * 6),                 ("_dae_date", ctypes.c_char * 1),                 # 대차잔고일자
        ("filler", ctypes.c_char * 1),                   ("_filler", ctypes.c_char * 1),                   # FILLER
        ("deposit_gb", ctypes.c_char * 1),               ("_deposit_gb", ctypes.c_char * 1),               # 증거금구분
        ("cpfn", ctypes.c_char * 12),                    ("_cpfn", ctypes.c_char * 1),                     # 자본금
        ("total_seln_qty", ctypes.c_char * 12),          ("_total_seln_qty", ctypes.c_char * 1),           # 전체거래원매도수량
        ("total_shnu_qty", ctypes.c_char * 12),          ("_total_shnu_qty", ctypes.c_char * 1),           # 전체거래원매수수량
        ("detour_gb", ctypes.c_char * 1),                ("_detour_gb", ctypes.c_char * 1),                # 우회상장여부
        ("scrt_grp_isnm", ctypes.c_char * 6),            ("_scrt_grp_isnm", ctypes.c_char * 1),            # 소속구분
        ("crdt_deal_date", ctypes.c_char * 4),           ("_crdt_deal_date", ctypes.c_char * 1),           # 신용거래일자
        ("crdt_loan_gvrt", ctypes.c_char * 5),           ("_crdt_loan_gvrt", ctypes.c_char * 1),           # 보증금율(%)
        ("per", ctypes.c_char * 5),                      ("_per", ctypes.c_char * 1),                      # PER
        ("hando_gb", ctypes.c_char * 1),                 ("_hando_gb", ctypes.c_char * 1),                 # 종목별신용한도
        ("wghn_avrg_prc", ctypes.c_char * 10),           ("_wghn_avrg_prc", ctypes.c_char * 1),            # 가중평균가
        ("lstn_stcn_unit0", ctypes.c_char * 12),         ("_lstn_stcn_unit0", ctypes.c_char * 1),          # 상장주식수_원
        ("add_lstn_stcn", ctypes.c_char * 12),           ("_add_lstn_stcn", ctypes.c_char * 1),            # 추가상장주식수
        ("gicomment", ctypes.c_char * 100),              ("_gicomment", ctypes.c_char * 1),                # 종목코멘트
        ("prdy_vol", ctypes.c_char * 12),                ("_prdy_vol", ctypes.c_char * 1),                 # 전일거래량
        ("pre_prdy_sign", ctypes.c_char * 1),            ("_pre_prdy_sign", ctypes.c_char * 1),            # 전일대비부호(전전일)
        ("pre_prdy_vrss", ctypes.c_char * 10),           ("_pre_prdy_vrss", ctypes.c_char * 1),            # 전일대비(전전일)
        ("stck_dryy_hgpr", ctypes.c_char * 10),          ("_stck_dryy_hgpr", ctypes.c_char * 1),           # 연중최고가
        ("dryy_hgpr_date", ctypes.c_char * 4),           ("_dryy_hgpr_date", ctypes.c_char * 1),           # 연중최고가일자
        ("stck_dryy_lwpr", ctypes.c_char * 10),          ("_stck_dryy_lwpr", ctypes.c_char * 1),           # 연중최저가
        ("dryy_lwpr_date", ctypes.c_char * 4),           ("_dryy_lwpr_date", ctypes.c_char * 1),           # 연중최저가일자
        ("frgn_hldn_qty", ctypes.c_char * 15),           ("_frgn_hldn_qty", ctypes.c_char * 1),            # 외국인보유주식수
        ("issu_limt_rate", ctypes.c_char * 5),           ("_issu_limt_rate", ctypes.c_char * 1),           # 외국인한도소진율(%)
        ("frml_mrkt_unit", ctypes.c_char * 5),           ("_frml_mrkt_unit", ctypes.c_char * 1),           # 매매수량단위
        ("comp_cls_code", ctypes.c_char * 1),            ("_comp_cls_code", ctypes.c_char * 1),            # 정규대량거래구분
        ("largem_gb", ctypes.c_char * 1),                ("_largem_gb", ctypes.c_char * 1),                # 대량매매구분
        ("pbr", ctypes.c_char * 5),                      ("_pbr", ctypes.c_char * 1),                      # PBR
        ("dmrs_val", ctypes.c_char * 7),                 ("_dmrs_val", ctypes.c_char * 1),                 # 저항값
        ("dmsp_val", ctypes.c_char * 7),                 ("_dmsp_val", ctypes.c_char * 1),                 # 지지값
        ("prdy_tr_pbmn", ctypes.c_char * 12),            ("_prdy_tr_pbmn", ctypes.c_char * 1),             # 전일거래대금
        ("vi_antc_sdpr", ctypes.c_char * 10),            ("_vi_antc_sdpr", ctypes.c_char * 1),             # VI기준가
        ("vi_antc_mxpr", ctypes.c_char * 10),            ("_vi_antc_mxpr", ctypes.c_char * 1),             # VI상승발동가
        ("vi_antc_llam", ctypes.c_char * 10),            ("_vi_antc_llam", ctypes.c_char * 1),             # VI하락발동가
        ("invt_epmd_yn", ctypes.c_char * 1),             ("_invt_epmd_yn", ctypes.c_char * 1),             # 투자유의종목여부
        ("uplm_qty", ctypes.c_char * 12),                ("_uplm_qty", ctypes.c_char * 1),                 # 상한수량
        ("short_over_code", ctypes.c_char * 1),          ("_short_over_code", ctypes.c_char * 1),          # 외국인소진코드
        ("mrkt_alrm_code", ctypes.c_char * 1),           ("_mrkt_alrm_code", ctypes.c_char * 1),           # 시장조치경고종목코드
        ("sltr_yn", ctypes.c_char * 1),                  ("_sltr_yn", ctypes.c_char * 1),                  # 정리매매여부
        ("crd_rt_grd_nm", ctypes.c_char * 6),            ("_crd_rt_grd_nm", ctypes.c_char * 1),            # 담보비율등급(%)
        ("mid_prc", ctypes.c_char * 10),                 ("_mid_prc", ctypes.c_char * 1),                  # 중간가
        ("midp_total_askp_rsqn", ctypes.c_char * 12),    ("_midp_total_askp_rsqn", ctypes.c_char * 1),     # 매도중간가잔량합계
        ("midp_total_bidp_rsqn", ctypes.c_char * 12),    ("_midp_total_bidp_rsqn", ctypes.c_char * 1),     # 매수중간가잔량합계
        ("nxt_mid_prc", ctypes.c_char * 10),             ("_nxt_mid_prc", ctypes.c_char * 1),              # NXT중간가
        ("nxt_midp_total_askp_rsqn", ctypes.c_char * 12),("_nxt_midp_total_askp_rsqn", ctypes.c_char * 1), # NXT매도중간가잔량합계
        ("nxt_midp_total_bidp_rsqn", ctypes.c_char * 12),("_nxt_midp_total_bidp_rsqn", ctypes.c_char * 1), # NXT매수중간가잔량합계
    ]


class CTIVWUTKMST04OutBlock2(Structure):
    """주식 현재가 조회 출력 블록2 C 구조체 (변동거래량 자료, 반복출력 - 최대 20건)"""
    _fields_ = [
        ("bsop_hour", ctypes.c_char * 8),            ("_bsop_hour", ctypes.c_char * 1),         # 시간
        ("stck_prpr", ctypes.c_char * 10),           ("_stck_prpr", ctypes.c_char * 1),         # 현재가
        ("prdy_vrss_sign", ctypes.c_char * 1),       ("_prdy_vrss_sign", ctypes.c_char * 1),    # 전일대비부호
        ("prdy_vrss", ctypes.c_char * 10),           ("_prdy_vrss", ctypes.c_char * 1),         # 전일대비
        ("askp", ctypes.c_char * 10),                ("_askp", ctypes.c_char * 1),              # 매도호가
        ("bidp", ctypes.c_char * 10),                ("_bidp", ctypes.c_char * 1),              # 매수호가
        ("cntg_vol", ctypes.c_char * 12),            ("_cntg_vol", ctypes.c_char * 1),          # 체결거래량
        ("acml_vol", ctypes.c_char * 12),            ("_acml_vol", ctypes.c_char * 1),          # 누적거래량
    ]


class CTIVWUTKMST04OutBlock3(Structure):
    """주식 현재가 조회 출력 블록3 C 구조체 (예상호가, 단일출력)"""
    _fields_ = [
        ("cncc_aspr_code", ctypes.c_char * 1),       ("_cncc_aspr_code", ctypes.c_char * 1),    # 동시호가구분
        ("antc_cnpr", ctypes.c_char * 10),           ("_antc_cnpr", ctypes.c_char * 1),         # 예상체결가
        ("antc_cntg_sign", ctypes.c_char * 1),       ("_antc_cntg_sign", ctypes.c_char * 1),    # 예상체결부호
        ("antc_cntg_vrss", ctypes.c_char * 10),      ("_antc_cntg_vrss", ctypes.c_char * 1),    # 예상체결대비
        ("antc_prdy_ctrt", ctypes.c_char * 5),       ("_antc_prdy_ctrt", ctypes.c_char * 1),    # 예상체결등락률
        ("antc_vol", ctypes.c_char * 12),            ("_antc_vol", ctypes.c_char * 1),          # 예상체결수량
        ("chkdataz1", ctypes.c_char * 1),            ("_chkdataz1", ctypes.c_char * 1),         # ECN예상자료구분
        ("ovtm_untp_prpr", ctypes.c_char * 10),      ("_ovtm_untp_prpr", ctypes.c_char * 1),    # ECN예상가
        ("ovtm_untp_sign", ctypes.c_char * 1),       ("_ovtm_untp_sign", ctypes.c_char * 1),    # ECN부호
        ("ovtm_untp_vrss", ctypes.c_char * 10),      ("_ovtm_untp_vrss", ctypes.c_char * 1),    # ECN대비
        ("ovtm_untp_ctrt", ctypes.c_char * 5),       ("_ovtm_untp_ctrt", ctypes.c_char * 1),    # ECN등락률
        ("ovtm_untp_vol", ctypes.c_char * 12),       ("_ovtm_untp_vol", ctypes.c_char * 1),     # ECN체결수량
        ("ovtm_antc_sign", ctypes.c_char * 1),       ("_ovtm_antc_sign", ctypes.c_char * 1),    # ECN장중예상체결부호
        ("ovtm_antc_vrss", ctypes.c_char * 10),      ("_ovtm_antc_vrss", ctypes.c_char * 1),    # ECN장중예상체결대비
        ("ovtm_antc_ctrt", ctypes.c_char * 5),       ("_ovtm_antc_ctrt", ctypes.c_char * 1),    # ECN장중예상체결등락률
        ("scoring", ctypes.c_char * 6),              ("_scoring", ctypes.c_char * 1),           # 종합스코어
        ("vi_type_code", ctypes.c_char * 1),         ("_vi_type_code", ctypes.c_char * 1),      # VI거래정지구분 (1:VI발동, N:그외)
    ]


# ==============================================================================
# Pydantic 모델 (사용자 친화적 인터페이스)
# ==============================================================================

class TIVWUTKMST04InBlock(InBlock):
    """주식 현재가 조회 입력 블록

    Attributes:
        form_lang: 한영구분 ('k': 한국어, 'e': 영문)
        shrn_iscd: 종목코드 (6자리, 예: '005930')

    사용 예:
        >>> from pynamuh import WMCAAgent, WMCAMessage
        >>> from pynamuh.structures.inv.ivwutkmst04 import TIVWUTKMST04InBlock
        >>>
        >>> with WMCAAgent() as agent:
        ...     # 로그인 완료 후...
        ...     input_data = TIVWUTKMST04InBlock(
        ...         form_lang="k",
        ...         shrn_iscd="005930",  # 삼성전자
        ...     )
        ...     # 통합시세로 현재가 조회 (계좌번호 불필요)
        ...     tr_index = 1
        ...     agent.query(tr_index, "IVWUTKMST04.UNT", input_data, nAccountIndex=0)
        ...
        ...     for msg_type, data in agent.receive_events(timeout=10.0):
        ...         if msg_type == WMCAMessage.CA_RECEIVEDATA:
        ...             if data.pData.szBlockName == "IVWUTKMST04Out1":
        ...                 out1: TIVWUTKMST04OutBlock1 = data.pData.szData
        ...                 print(f"{out1.hts_isnm}: {out1.stck_prpr}원")
        ...         elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
        ...             break
    """

    C_STRUCT: ClassVar[Type[ctypes.Structure]] = CTIVWUTKMST04InBlock

    form_lang: str = Field(
        default="k",
        pattern=r'^[ke]$',
        description="한영구분 (k:한국어, e:영문)"
    )
    shrn_iscd: str = Field(
        min_length=6,
        max_length=6,
        description="종목코드 (6자리)"
    )


# ==============================================================================
# Output 구조체
# ==============================================================================

@dataclass
class TIVWUTKMST04OutBlock1(OutBlock):
    """주식 현재가 조회 OutBlock1 (종목 기본 정보 / 호가 / 투자지표)

    단일출력. 종목명·현재가·전일대비·시고저·상하한·10단계 호가·잔량·
    52주 최고/최저·재무지표(PER/PBR)·외국인 정보 등을 포함한다.
    """
    # ── 기본 정보 ────────────────────────────────────────────────
    shrn_iscd: str              # 종목코드
    hts_isnm: str               # 종목명
    mrkt_div_isnm: str          # 코스피/코스닥구분
    bstp_kor_isnm: str          # 업종명
    bstp_cls_code: str          # 업종코드

    # ── 현재가/등락 ───────────────────────────────────────────────
    stck_prpr: str              # 현재가
    prdy_vrss_sign: str         # 전일대비부호
    prdy_vrss: str              # 전일대비
    prdy_ctrt: str              # 등락률
    stck_prdy_clpr: str         # 전일종가

    # ── 시고저/상하한 ─────────────────────────────────────────────
    stck_oprc: str              # 시가
    stck_hgpr: str              # 고가
    stck_lwpr: str              # 저가
    stck_mxpr: str              # 상한가
    stck_llam: str              # 하한가

    # ── 거래량/거래대금 ──────────────────────────────────────────
    acml_vol: str               # 누적거래량
    acml_tr_pbmn: str           # 누적거래대금
    vol_rate: str               # 거래량비율
    prdy_vol: str               # 전일거래량
    prdy_tr_pbmn: str           # 전일거래대금

    # ── 호가/잔량 ────────────────────────────────────────────────
    hoga_bsop_hour: str         # 호가시간
    askp: str                   # 매도호가
    bidp: str                   # 매수호가
    askp1: str
    askp2: str
    askp3: str
    askp4: str
    askp5: str
    askp6: str
    askp7: str
    askp8: str
    askp9: str
    askp10: str
    bidp1: str
    bidp2: str
    bidp3: str
    bidp4: str
    bidp5: str
    bidp6: str
    bidp7: str
    bidp8: str
    bidp9: str
    bidp10: str
    askp_rsqn1: str
    askp_rsqn2: str
    askp_rsqn3: str
    askp_rsqn4: str
    askp_rsqn5: str
    askp_rsqn6: str
    askp_rsqn7: str
    askp_rsqn8: str
    askp_rsqn9: str
    askp_rsqn10: str
    bidp_rsqn1: str
    bidp_rsqn2: str
    bidp_rsqn3: str
    bidp_rsqn4: str
    bidp_rsqn5: str
    bidp_rsqn6: str
    bidp_rsqn7: str
    bidp_rsqn8: str
    bidp_rsqn9: str
    bidp_rsqn10: str
    total_askp_rsqn: str        # 총매도잔량
    total_bidp_rsqn: str        # 총매수잔량

    # ── 52주 최고/최저, 연중 최고/최저 ───────────────────────────
    w52_hgpr: str               # 52주최고가
    w52_hgpr_date: str          # 52주최고가일자
    w52_lwpr: str               # 52주최저가
    w52_lwpr_date: str          # 52주최저가일자
    stck_dryy_hgpr: str         # 연중최고가
    dryy_hgpr_date: str         # 연중최고가일자
    stck_dryy_lwpr: str         # 연중최저가
    dryy_lwpr_date: str         # 연중최저가일자

    # ── 시가총액/주식수/재무지표 ────────────────────────────────
    hts_avls: str               # 시가총액
    move_stcn: str              # 유통주식수
    lstn_stcn_unit3: str        # 상장주식수
    stck_fcam: str              # 액면가
    per: str                    # PER
    pbr: str                    # PBR
    wghn_avrg_prc: str          # 가중평균가

    # ── 외국인 ───────────────────────────────────────────────────
    frgn_hldn_qty: str          # 외국인보유주식수
    issu_limt_rate: str         # 외국인한도소진율(%)
    for_rate: str               # 외국인소진율
    frgn_ntby_vol: str          # 외국인순매수수량

    # ── VI / 시장조치 ────────────────────────────────────────────
    vi_antc_sdpr: str           # VI기준가
    vi_antc_mxpr: str           # VI상승발동가
    vi_antc_llam: str           # VI하락발동가
    mrkt_alrm_code: str         # 시장조치경고종목코드
    invt_epmd_yn: str           # 투자유의종목여부
    sltr_yn: str                # 정리매매여부


@dataclass
class TIVWUTKMST04OutBlock2(OutBlock):
    """주식 현재가 조회 OutBlock2 (변동거래량 자료, 반복 출력)

    최근 체결 단위로 시간/현재가/등락/호가/체결거래량을 제공.
    """
    bsop_hour: str              # 시간
    stck_prpr: str              # 현재가
    prdy_vrss_sign: str         # 전일대비부호
    prdy_vrss: str              # 전일대비
    askp: str                   # 매도호가
    bidp: str                   # 매수호가
    cntg_vol: str               # 체결거래량
    acml_vol: str               # 누적거래량


@dataclass
class TIVWUTKMST04OutBlock3(OutBlock):
    """주식 현재가 조회 OutBlock3 (예상호가)

    동시호가 시간대의 예상체결가 및 ECN 야간거래 예상 정보.
    """
    cncc_aspr_code: str         # 동시호가구분
    antc_cnpr: str              # 예상체결가
    antc_cntg_sign: str         # 예상체결부호
    antc_cntg_vrss: str         # 예상체결대비
    antc_prdy_ctrt: str         # 예상체결등락률
    antc_vol: str               # 예상체결수량
    chkdataz1: str              # ECN예상자료구분
    ovtm_untp_prpr: str         # ECN예상가
    ovtm_untp_sign: str         # ECN부호
    ovtm_untp_vrss: str         # ECN대비
    ovtm_untp_ctrt: str         # ECN등락률
    ovtm_untp_vol: str          # ECN체결수량
    ovtm_antc_sign: str         # ECN장중예상체결부호
    ovtm_antc_vrss: str         # ECN장중예상체결대비
    ovtm_antc_ctrt: str         # ECN장중예상체결등락률
    scoring: str                # 종합스코어
    vi_type_code: str           # VI거래정지구분 (1:VI발동, N:그외)


__all__ = [
    "CTIVWUTKMST04InBlock",
    "TIVWUTKMST04InBlock",
    "CTIVWUTKMST04OutBlock1",
    "TIVWUTKMST04OutBlock1",
    "CTIVWUTKMST04OutBlock2",
    "TIVWUTKMST04OutBlock2",
    "CTIVWUTKMST04OutBlock3",
    "TIVWUTKMST04OutBlock3",
]
