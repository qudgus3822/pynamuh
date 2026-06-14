import os
from dotenv import load_dotenv
from pynamuh import WMCAAgent, WMCAMessage
from pynamuh.structures.ord.c8201 import Tc8201InBlock

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
                print(f"  사용자 ID: {data.pLoginInfo.szUserID}")
                print(f"  계좌 수: {data.pLoginInfo.szAccountCount}")
                for i, account in enumerate(data.pLoginInfo.accountlist, 1):
                    print(f"  계좌 {i}: {account.szAccountNo} ({account.szAccountName})")
                login_success = True
                break
            elif msg_type == WMCAMessage.CA_DISCONNECTED:
                print("로그인 실패")
                break

        if not login_success:
            print("로그인 실패로 종료합니다.")
            return

        # =============================================
        # 2. 연결 상태 확인
        # =============================================
        print("\n" + "=" * 50)
        print(f"[2] 연결 상태: {agent.is_connected()}")

        # =============================================
        # 3. 잔고 조회 (c8201)
        # =============================================
        print("\n" + "=" * 50)
        print("[3] 잔고 조회...")

        # 계좌 비밀번호 해시 생성
        password_hash = agent.get_account_hash_password(
            account_index=1,
            password=os.environ["NAMUH_ACCOUNT_PW"]
        )

        input_data = Tc8201InBlock(
            pswd_noz44=password_hash,
            bnc_bse_cdz1="1"  # 전체 잔고
        )

        tr_index = 1001
        agent.query(
            nTRID=tr_index,
            szTRCode="c8201",
            szInput=input_data,
            nAccountIndex=1
        )

        for msg_type, data in agent.receive_events(timeout=10.0):
            if hasattr(data, "TrIndex") and data.TrIndex == tr_index:
                if msg_type == WMCAMessage.CA_RECEIVEDATA:
                    block = data.pData
                    print(f"  블록 수신: {block.szBlockName}")
                    if block.szBlockName == "c8201OutBlock":
                        print(f"    예수금: {block.szData.dpsit_amtz16}")
                        print(f"    출금가능: {block.szData.chgm_pos_amtz16}")
                    elif block.szBlockName == "c8201OutBlock1":
                        for item in block.szData:
                            print(f"    종목: {item.issue_codez6} {item.issue_namez40}, 잔고: {item.bal_qtyz16}, 현재가: {item.prsnt_pricez16}, 손익율: {item.earn_ratez9}")
                elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                    print("  잔고 조회 완료!")
                    break
                elif msg_type == WMCAMessage.CA_RECEIVEERROR:
                    print("  잔고 조회 실패!")
                    break

        # =============================================
        # 4. 실시간 시세 (j8 - 삼성전자 005930)
        # =============================================
        print("\n" + "=" * 50)
        print("[4] 실시간 시세 등록 (삼성전자 005930)...")

        agent.attach(
            szBCType="j8",
            szInput="005930",
            nCodeLen=6,
            nInputLen=6
        )

        import time
        start_time = time.time()
        count = 0

        for msg_type, data in agent.receive_events():
            if msg_type == WMCAMessage.CA_RECEIVESISE:
                if data.pData.szBlockName == "j8OutBlock":
                    count += 1
                    print(f"  [{count}] 현재가: {data.pData.szData.cur_prcz8}")

            # 10초 후 종료
            if time.time() - start_time > 10:
                break

        print(f"  {count}건 수신 완료")

        # =============================================
        # 5. 실시간 시세 해제
        # =============================================
        print("\n" + "=" * 50)
        print("[5] 실시간 시세 해제...")
        agent.detach(
            szBCType="j8",
            szInput="005930",
            nCodeLen=6,
            nInputLen=6
        )
        print("  해제 완료")

        # =============================================
        # 6. 로그아웃 (with 블록 종료 시 자동)
        # =============================================
        print("\n" + "=" * 50)
        print("[6] 로그아웃 (자동)")

    print("\n모든 테스트 완료!")


if __name__ == "__main__":
    main()
