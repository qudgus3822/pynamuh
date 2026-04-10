import os
from dotenv import load_dotenv
from pynamuh import WMCAAgent, WMCAMessage

load_dotenv()

with WMCAAgent() as agent:
    agent.connect(
        szID=os.environ["NAMUH_ID"],
        szPW=os.environ["NAMUH_PW"],
        szCertPW=os.environ["NAMUH_CERT_PW"],
    )

    for msg_type, data in agent.receive_events(timeout=10.0):
        if msg_type == WMCAMessage.CA_CONNECTED:
            print("로그인 성공!")
            break
        elif msg_type == WMCAMessage.CA_DISCONNECTED:
            print("로그인 실패")
            break
