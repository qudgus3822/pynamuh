"""잔고 조회 → 매도 주문 → 취소 테스트

보유 종목 1주를 체결 불가능한 높은 가격으로 지정가 매도 후 즉시 취소합니다.
"""

import os
from dotenv import load_dotenv
from pynamuh import WMCAAgent, WMCAMessage
from pynamuh.structures.ord.c8201 import Tc8201InBlock
from pynamuh.structures.ord.c8101 import Tc8101InBlock
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
        # 3. 잔고 조회 (c8201)
        # =============================================
        print("\n" + "=" * 50)
        print("[3] 잔고 조회...")

        balance_input = Tc8201InBlock(
            pswd_noz44=acct_pwd,
            bnc_bse_cdz1="1",
        )
        balance_tr = 1001
        agent.query(nTRID=balance_tr, szTRCode="c8201", szInput=balance_input, nAccountIndex=1)

        stocks = []
        for msg_type, data in agent.receive_events(timeout=10.0):
            if hasattr(data, "TrIndex") and data.TrIndex == balance_tr:
                if msg_type == WMCAMessage.CA_RECEIVEDATA:
                    block = data.pData
                    if block.szBlockName == "c8201OutBlock1":
                        for item in block.szData:
                            code = item.issue_codez6.strip()
                            name = item.issue_namez40.strip()
                            qty = item.bal_qtyz16.strip()
                            price = item.prsnt_pricez16.strip()
                            if code and int(qty) > 0:
                                stocks.append((code, name, qty, price))
                                print(f"  {code} {name} | 잔고: {qty}주 | 현재가: {price}")
                elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                    break

        if not stocks:
            print("  보유 종목이 없어 매도 테스트를 건너뜁니다.")
            return

        # 첫 번째 종목 선택
        target_code, target_name, target_qty, target_price = stocks[0]
        # 현재가의 약 1.2배, 호가단위에 맞게 반올림
        raw_price = int(int(target_price) * 1.2)
        # 호가단위: ~2천:1원, ~5천:5원, ~2만:10원, ~5만:50원, ~20만:100원, ~50만:500원, 50만~:1000원
        if raw_price < 2000: unit = 1
        elif raw_price < 5000: unit = 5
        elif raw_price < 20000: unit = 10
        elif raw_price < 50000: unit = 50
        elif raw_price < 200000: unit = 100
        elif raw_price < 500000: unit = 500
        else: unit = 1000
        sell_price = (raw_price // unit) * unit
        sell_price_str = str(sell_price).zfill(10)  # 10자리 0패딩

        print(f"\n  >> 매도 대상: {target_code} {target_name}")
        print(f"  >> 매도 수량: 1주")
        print(f"  >> 매도 가격: {sell_price}원 (현재가의 1.2배, 상한가 이내)")

        # =============================================
        # 4. 매도 주문 (c8101)
        # =============================================
        print("\n" + "=" * 50)
        print("[4] 매도 주문 전송...")

        sell_input = Tc8101InBlock(
            pswd_noz8=acct_pwd,
            issue_codez6=target_code,
            order_qtyz12="000000000001",
            order_unit_pricez10=sell_price_str,
            trade_typez2="00",              # 지정가
            shsll_pos_flagz1="0",           # 정상 (공매도 아님)
            trad_pswd_no_1z8=trade_pwd,
            trad_pswd_no_2z8=trade_pwd,
            rmt_mkt_cdz3="KRX",
            mkt_insd_cor_req_ynz1="N",
        )

        order_tr = 2001
        agent.query(nTRID=order_tr, szTRCode="c8101", szInput=sell_input, nAccountIndex=1)

        order_no = ""
        for msg_type, data in agent.receive_events(timeout=10.0):
            if hasattr(data, "TrIndex") and data.TrIndex == order_tr:
                if msg_type == WMCAMessage.CA_RECEIVEDATA:
                    if data.pData.szBlockName == "c8101OutBlock":
                        order_no = data.pData.szData.order_noz10.strip()
                        if order_no:
                            print(f"  매도 주문 성공! 주문번호: {order_no}")
                        else:
                            print("  매도 주문 실패 (주문번호 없음)")
                elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                    break
                elif msg_type == WMCAMessage.CA_RECEIVEERROR:
                    print("  매도 주문 실패 (에러)")
                    break
            if msg_type == WMCAMessage.CA_RECEIVEMESSAGE:
                msg = data.pData.szData
                print(f"  메시지: [{msg.msg_cd}] {msg.user_msg}")

        if not order_no:
            print("  주문번호를 받지 못해 취소 테스트를 건너뜁니다.")
            return

        # =============================================
        # 5. 주문 취소 (c8104)
        # =============================================
        print("\n" + "=" * 50)
        print(f"[5] 주문 취소 (주문번호: {order_no})...")

        cancel_input = Tc8104InBlock(
            pswd_noz8=acct_pwd,
            issue_codez6=target_code,
            canc_qtyz12="000000000001",
            orgnl_order_noz10=order_no.zfill(10),
            all_part_typez1="1",
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
                msg = data.pData.szData
                print(f"  메시지: [{msg.msg_cd}] {msg.user_msg}")

        # =============================================
        # 6. 완료
        # =============================================
        print("\n" + "=" * 50)
        print("[6] 테스트 완료!")

    print("\n로그아웃 완료")


if __name__ == "__main__":
    main()
