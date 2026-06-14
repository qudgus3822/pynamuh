"""주문 → 취소 안전 테스트

삼성전자 1주를 체결 불가능한 낮은 가격으로 지정가 매수 후 즉시 취소합니다.
"""

import os
from dotenv import load_dotenv
from pynamuh import WMCAAgent, WMCAMessage
from pynamuh.structures.ord.c8102 import Tc8102InBlock
from pynamuh.structures.ord.c8104 import Tc8104InBlock

load_dotenv()


def main():
    with WMCAAgent() as agent:
        # =============================================
        # 1. 로그인
        # =============================================
        print("=" * 50)
        print("[1] 로그인 시도...")
        agent.connect(
            szID=os.environ["NAMUH_ID"],
            szPW=os.environ["NAMUH_PW"],
            szCertPW=os.environ["NAMUH_CERT_PW"],
        )

        login_success = False
        for msg_type, data in agent.receive_events(timeout=10.0):
            if msg_type == WMCAMessage.CA_CONNECTED:
                print("로그인 성공!")
                login_success = True
                break
            elif msg_type == WMCAMessage.CA_DISCONNECTED:
                print("로그인 실패")
                break

        if not login_success:
            print("로그인 실패로 종료합니다.")
            return

        # =============================================
        # 2. 비밀번호 해시 생성
        # =============================================
        print("\n" + "=" * 50)
        print("[2] 비밀번호 해시 생성...")
        acct_pwd = agent.get_account_hash_password(1, os.environ["NAMUH_ACCOUNT_PW"])
        trade_pwd = agent.get_order_hash_password(os.environ["NAMUH_TRADE_PW"])
        print("  해시 생성 완료")

        # =============================================
        # 3. 매수 주문 (삼성전자 1주, 10000원 지정가 - 체결 불가 가격)
        # =============================================
        print("\n" + "=" * 50)
        print("[3] 매수 주문 전송...")
        print("  종목: 005930 (삼성전자)")
        print("  수량: 1주")
        print("  가격: 10,000원 (지정가 - 체결 불가)")

        order_input = Tc8102InBlock(
            pswd_noz8=acct_pwd,
            issue_codez6="005930",
            order_qtyz12="000000000001",  # 12자리 0패딩 우측정렬
            order_unit_pricez10="0000180000",  # 10자리 0패딩 우측정렬
            trade_typez2="00",           # 지정가
            trad_pswd_no_1z8=trade_pwd,
            trad_pswd_no_2z8=trade_pwd,
            rmt_mkt_cdz3="KRX",
        )

        order_tr = 2001
        agent.query(nTRID=order_tr, szTRCode="c8102", szInput=order_input, nAccountIndex=1)

        order_no = ""
        for msg_type, data in agent.receive_events(timeout=10.0):
            if hasattr(data, "TrIndex") and data.TrIndex == order_tr:
                if msg_type == WMCAMessage.CA_RECEIVEDATA:
                    if data.pData.szBlockName == "c8102OutBlock":
                        order_no = data.pData.szData.order_noz10.strip()
                        if order_no:
                            print(f"  주문 성공! 주문번호: {order_no}")
                        else:
                            print("  주문 실패 (주문번호 없음)")
                elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                    break
                elif msg_type == WMCAMessage.CA_RECEIVEERROR:
                    print("  주문 실패 (에러)")
                    break
            if msg_type == WMCAMessage.CA_RECEIVEMESSAGE:
                print(f"  메시지: {data}")

        if not order_no:
            print("  주문번호를 받지 못해 취소 테스트를 건너뜁니다.")
            return

        # =============================================
        # 4. 주문 취소
        # =============================================
        print("\n" + "=" * 50)
        print(f"[4] 주문 취소 (주문번호: {order_no})...")

        cancel_input = Tc8104InBlock(
            pswd_noz8=acct_pwd,
            issue_codez6="005930",
            canc_qtyz12="1",
            orgnl_order_noz10=order_no,
            all_part_typez1="1",         # 잔량 전체 취소
            trad_pswd_no_1z8=trade_pwd,
            trad_pswd_no_2z8=trade_pwd,
        )

        cancel_tr = 2002
        agent.query(nTRID=cancel_tr, szTRCode="c8104", szInput=cancel_input, nAccountIndex=1)

        for msg_type, data in agent.receive_events(timeout=10.0):
            if hasattr(data, "TrIndex") and data.TrIndex == cancel_tr:
                if msg_type == WMCAMessage.CA_RECEIVEDATA:
                    if data.pData.szBlockName == "c8104OutBlock":
                        cancel_no = data.pData.szData.order_noz10.strip()
                        if cancel_no:
                            print(f"  취소 성공! 취소주문번호: {cancel_no}")
                        else:
                            print("  취소 실패")
                elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                    break
                elif msg_type == WMCAMessage.CA_RECEIVEERROR:
                    print("  취소 실패 (에러)")
                    break
            if msg_type == WMCAMessage.CA_RECEIVEMESSAGE:
                print(f"  메시지: {data}")

        # =============================================
        # 5. 완료
        # =============================================
        print("\n" + "=" * 50)
        print("[5] 테스트 완료!")

    print("\n로그아웃 완료")


if __name__ == "__main__":
    main()
