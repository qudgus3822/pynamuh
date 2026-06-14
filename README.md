# pynamuh

**Python wrapper for Namuh Securities OpenAPI**

나무증권 OpenAPI를 Python에서 사용할 수 있도록 만든 래퍼입니다.
## 주의
 - 이 프로젝트는 **개인적으로 사용하기 위해 작성한 코드**를 공개하게 된 것입니다. 나무증권과 공식적인 관련은 없습니다.  
    - 작동을 위해서는 나무증권 홈페이지에서 OpenAPI .dll 파일들을 ./src/bin 폴더에 수동으로 위치시켜주셔야 합니다.  
 - **정상 작동을 보장하지 않으니 충분한 테스트 이후 본인의 판단 및 책임 하에 사용하시기 바랍니다.**

## 시스템 요구사항
- **OS**: Windows 11(64비트 환경)에서 정상 작동 확인
- **Python**: **32비트 Windows 파이썬 가상환경**에서 작동시켜야 합니다.
- 사용자의 단일 공인인증서가 하드디스크에 위치한 환경에서 정상 작동을 확인했습니다.

## 설치 방법
아래에서는 `uv`를 이용해 본 라이브러리를 설치하는 방법을 다룹니다.

### 1. uv 설치

먼저 [uv](https://docs.astral.sh/uv/)를 설치합니다:

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

자세한 설치 방법은 [uv 공식 문서](https://docs.astral.sh/uv/getting-started/installation/)를 참고하세요.

### 2. pynamuh 설치

본 패키지는 PyPI에 배포되지 않은 패키지로서 Git 저장소에서 직접 설치해야 합니다

```bash
# Git 저장소에서 설치
uv add git+https://github.com/odumag99/pynamuh.git
```

### 3. DLL 파일 설치

**중요**: 나무증권 OpenAPI 라이브러리를 다운로드한 후 .dll 파일을 수동으로 위치시켜야 합니다.

1. [나무증권 홈페이지](https://www.mynamuh.com/)에서 OpenAPI 다운로드
2. 다운로드한 파일에서 `.dll` 파일들을 추출
3. pynamuh 설치 경로의 `dll` 폴더에 복사:

```
<python-site-packages>/pynamuh/
└── dll/
    └── *.dll      ← 여기에 복사
```

## 사용법

### 기본 사용법

pynamuh는 `WMCAAgent` 클래스를 통해 NH증권 OpenAPI를 사용합니다:

```python
from pynamuh import WMCAAgent, WMCAMessage

# WMCAAgent 생성 및 사용
with WMCAAgent() as agent:
    # 로그인
    agent.connect(szID="your_id", szPW="your_password", szCertPW="cert_password")

    # 응답 수신
    for msg_type, data in agent.receive_events(timeout=10.0):
        if msg_type == WMCAMessage.CA_CONNECTED:
            print("로그인 성공!")
            break
```

### 요청/응답 모델 이해하기

**중요**: WMCAAgent는 **요청을 보내는 메서드와 응답을 받는 메서드가 별개**입니다.

**일반적인 함수 호출과의 차이:**

- **일반적인 함수 호출**: 요청하고 응답을 **한 함수에서** 받음
  ```python
  # 예: 일반적인 API 호출
  result = some_api.login(id, pw)  # 여기서 결과를 바로 받음
  print(result)
  ```

- **WMCAAgent의 방식**: 요청을 보내는 메서드와 응답을 받는 메서드가 **별개**
  ```python
  # 1. 요청 전송
  agent.connect(id, pw, cert_pw)

  # 2. 응답 수신 (별도 메서드)
  for msg_type, data in agent.receive_events():
      if msg_type == WMCAMessage.CA_CONNECTED:
          print("로그인 성공!")
  ```

**동작 흐름:**

```python
# 1. 로그인 요청 전송 (즉시 전송 완료됨!)
agent.connect(...)
# ← 여기서 바로 다음 줄로 넘어갑니다 (로그인 완료를 기다리지 않음)

# 2. receive_events()로 응답을 수신
for msg_type, data in agent.receive_events():
    if msg_type == WMCAMessage.CA_CONNECTED:
        print("로그인 성공!")  # ← 이제야 로그인 결과를 받음
        break
```

**TRIndex를 이용한 요청-응답 매칭:**

여러 요청을 동시에 보냈을 때, 어떤 응답이 어떤 요청에 대한 것인지 구분하기 위해 `TRIndex`를 사용합니다:

```python
# 여러 TR 요청을 동시에 전송 (각기 다른 TRIndex 사용)
agent.query(nTRID=1001, szTRCode="c8201", ...)  # 잔고 조회
agent.query(nTRID=1002, szTRCode="c1101", ...)  # 현재가 조회
# ↑ 두 요청 모두 즉시 반환됨 (결과를 기다리지 않음)

# 나중에 응답이 오면 TRIndex로 구분
for msg_type, data in agent.receive_events():
    if msg_type == WMCAMessage.CA_RECEIVEDATA:
        if data.TrIndex == 1001:
            print("잔고 조회 응답:", data)
        elif data.TrIndex == 1002:
            print("현재가 조회 응답:", data)
```

## WMCAAgent API 레퍼런스

### 초기화

**권장 사용법**: `with` 문을 사용하여 자동으로 초기화 및 정리를 수행합니다.

```python
with WMCAAgent() as agent:
    # 자동으로 Windows 메시지 윈도우 생성
    agent.connect(...)
    # ... 작업 수행 ...
# with 블록 종료 시 자동으로 리소스 정리 (연결 해제, 윈도우 파괴)
```

---

### 로그인/로그아웃

#### `connect(szID, szPW, szCertPW, MediaType='T', UserType='W')`

서버 연결(로그인) 요청을 전송합니다.

**파라미터:**
- `szID` (str): 사용자 ID
- `szPW` (str): 사용자 비밀번호
- `szCertPW` (str): 공인인증서 비밀번호
- `MediaType` (str): 매체유형 (`'P'`: QV계좌, `'T'`: Namuh계좌, 기본값: `'T'`)
- `UserType` (str): 사용자유형 (`'1'`: QV계좌, `'W'`: Namuh계좌, 기본값: `'W'`)

**반환값:**
- `bool`: wmcaConnect 호출 성공 여부 (응답은 `receive_events()`로 수신)

**수신되는 응답 메시지 타입:**
- `CA_CONNECTED`: 로그인 성공 (LoginBlock 데이터 포함)
- `CA_DISCONNECTED`: 로그인 실패

**예제:**

```python
with WMCAAgent() as agent:
    # 로그인 요청 전송
    success = agent.connect(
        szID="your_id",
        szPW="your_password",
        szCertPW="cert_password"
    )

    if not success:
        print("connect() 호출 실패")
        return

    # 응답 수신 (최대 10초 대기)
    for msg_type, data in agent.receive_events(timeout=10.0):
        if msg_type == WMCAMessage.CA_CONNECTED:
            print("로그인 성공!")
            print(f"사용자 ID: {data.pLoginInfo.szUserID}")
            print(f"계좌 수: {data.pLoginInfo.szAccountCount}")
            for i, account in enumerate(data.pLoginInfo.accountlist, 1):
                print(f"  계좌 {i}: {account.szAccountNo} ({account.szAccountName})")
            break
        elif msg_type == WMCAMessage.CA_DISCONNECTED:
            print("로그인 실패")
            break
```


#### `disconnect()`

서버 연결을 해제합니다(로그아웃).

**반환값:**
- `bool`: wmcaDisconnect 호출 성공 여부

**예제:**

```python
agent.disconnect()
```

#### `is_connected()`

현재 연결 상태를 확인합니다.

**반환값:**
- `bool`: 연결 상태 (`True`: 연결됨, `False`: 연결 해제)

**예제:**

```python
if agent.is_connected():
    print("서버에 연결되어 있습니다")
else:
    print("연결되지 않았습니다")
```

---

### TR 조회

#### `query(nTRID, szTRCode, szInput, nAccountIndex=0)`

TR(Transaction) 조회 요청을 전송합니다.

**파라미터:**
- `nTRID` (int): Transaction ID (응답 구분용, 임의의 정수)
- `szTRCode` (str): 서비스 코드 (예: `"c8201"`, `"c1101"`). 나무증권 SPEC 문서 참조.
- `szInput` (InBlock): TR 입력 데이터 (Pydantic 모델)
- `nAccountIndex` (int): 계좌 인덱스 (`0`: 계좌 불필요, `1~`: 로그인 시 받은 계좌 순서)

**반환값:**
- `bool`: wmcaQuery 호출 성공 여부 (응답은 `receive_events()`로 수신)

**수신되는 응답 메시지 타입:**
- `CA_RECEIVEDATA`: TR 블록 데이터 수신 (여러 번 수신 가능)
- `CA_RECEIVECOMPLETE`: 모든 블록 수신 완료
- `CA_RECEIVEERROR`: TR 처리 실패

**예제 1: 잔고 조회 (c8201)**

```python
from pynamuh.structures.ord.c8201 import *

with WMCAAgent() as agent:
    # 로그인 먼저 수행 (생략)

    # 계좌 비밀번호 해시 생성
    password_hash = agent.get_account_hash_password(
        account_index=1,
        password="1234"
    )

    # 입력 데이터 생성
    input_data = Tc8201InBlock(
        pswd_noz44=password_hash,  # 44자 해시
        bnc_bse_cdz1="1"            # 잔고 구분 (1: 전체)
    )

    # TR 조회 요청 전송
    tr_index = 1001  # 임의의 고유 ID
    agent.query(
        nTRID=tr_index,
        szTRCode="c8201",
        szInput=input_data,
        nAccountIndex=1  # 첫 번째 계좌
    )

    # 응답 수신
    blocks = []
    for msg_type, data in agent.receive_events(timeout=10.0):
        # TrIndex로 응답 구분
        if hasattr(data, 'TrIndex') and data.TrIndex == tr_index:
            if msg_type == WMCAMessage.CA_RECEIVEDATA:
                print(f"블록 수신: {data.pData.szBlockName}")
                blocks.append(data.pData)
            elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                print("조회 완료!")
                break
            elif msg_type == WMCAMessage.CA_RECEIVEERROR:
                print("조회 실패!")
                break

    # 결과 처리
    for block in blocks:
        if block.szBlockName == "c8201OutBlock":
            print(f"예수금: {block.szData.dpsit_amtz16}")
        elif block.szBlockName == "c8201OutBlock1":
            for item in block.szData:  # 반복 블록 (리스트)
                print(f"종목: {item.issue_codez6} {item.issue_namez40}")
                print(f"잔고수량: {item.bal_qtyz16}")
```

**예제 2: 여러 TR 동시 요청**

```python
# 잔고 조회 (TrIndex=1001)
agent.query(nTRID=1001, szTRCode="c8201", szInput=balance_input, nAccountIndex=1)

# 현재가 조회 (TrIndex=1002)
agent.query(nTRID=1002, szTRCode="c1101", szInput=price_input, nAccountIndex=0)

# 응답 수신 (TrIndex로 구분)
completed = {1001: False, 1002: False}
for msg_type, data in agent.receive_events(timeout=30.0):
    if hasattr(data, 'TrIndex'):
        tr_id = data.TrIndex

        if msg_type == WMCAMessage.CA_RECEIVEDATA:
            print(f"TR {tr_id}: {data.pData.szBlockName}")
        elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
            print(f"TR {tr_id} 완료")
            completed[tr_id] = True

        # 모두 완료되면 종료
        if all(completed.values()):
            break
```

**참고:**
- 시세 TR 명세: `시세_SPEC_20201015.pdf`
- 주문 TR 명세: `주문_SPEC_20190919.pdf`

#### `get_account_hash_password(account_index, password)`

계좌 비밀번호를 44자 해시값으로 변환합니다.

**파라미터:**
- `account_index` (int): 계좌 인덱스 (1부터 시작)
- `password` (str): 평문 비밀번호

**반환값:**
- `str`: 44자 해시 문자열

**예제:**

```python
# 계좌 비밀번호 해시 생성
hash_pwd = agent.get_account_hash_password(
    account_index=1,
    password="1234"
)
print(len(hash_pwd))  # 44

# InBlock에 설정
input_data = Tc8201InBlock(
    pswd_noz44=hash_pwd,  # 44자 해시
    bnc_bse_cdz1="1"
)
```

**참고:**
- TR 조회 시 계좌 비밀번호가 필요한 경우 사용

---

### 실시간 시세

#### `attach(szBCType, szInput, nCodeLen, nInputLen)`

실시간 시세를 등록합니다.

**파라미터:**
- `szBCType` (str): 실시간 서비스 코드 (2자리). 나무증권 시세 SPEC 문서 참조. (예: `"j8"`)
- `szInput` (str): 종목코드 (여러 종목 연결 가능)
- `nCodeLen` (int): 종목코드 개별 길이 (주식: 6)
- `nInputLen` (int): 입력값 전체 길이 (종목수 × nCodeLen)

**반환값:**
- `bool`: wmcaAttach 호출 성공 여부 (응답은 `receive_events()`로 수신)

**수신되는 응답 메시지 타입:**
- `CA_RECEIVESISE`: 실시간 시세 데이터 (지속적으로 수신)

**예제 1: 단일 종목 등록**

```python
with WMCAAgent() as agent:
    # 로그인 먼저 수행 (생략)

    # SK하이닉스(000660) 실시간 체결가 등록
    agent.attach(
        szBCType="j8",
        szInput="000660",
        nCodeLen=6,
        nInputLen=6
    )

    # 실시간 데이터 수신 (무한 루프)
    for msg_type, data in agent.receive_events():
        if msg_type == WMCAMessage.CA_RECEIVESISE:
            if data.pData.szBlockName == "j8OutBlock":
                print(f"종목: {data.pData.szData.code}")
                print(f"현재가: {data.pData.szData.price}")
                print(f"거래량: {data.pData.szData.volume}")
```

**예제 2: 여러 종목 등록**

```python
# 3개 종목 동시 등록 (SK하이닉스, NH투자증권, 삼성전자)
agent.attach(
    szBCType="j8",
    szInput="000660005940005930",  # 종목코드 연결
    nCodeLen=6,
    nInputLen=18  # 6 × 3 = 18
)
```

**참고:**
- 명시적으로 `detach()` 호출하거나 프로그램 종료 시까지 지속 수신

#### `detach(szBCType, szInput, nCodeLen, nInputLen)`

실시간 시세를 해제합니다.

**파라미터:**
- `szBCType` (str): 실시간 서비스 코드 (2자리). `attach()`와 동일
- `szInput` (str): 종목코드. `attach()`와 동일
- `nCodeLen` (int): 종목코드 개별 길이. `attach()`와 동일
- `nInputLen` (int): 입력값 전체 길이. `attach()`와 동일

**반환값:**
- `bool`: wmcaDetach 호출 성공 여부

**예제:**

```python
# 등록했던 실시간 시세 해제
agent.detach(
    szBCType="j8",
    szInput="000660",
    nCodeLen=6,
    nInputLen=6
)
```

---

### 이벤트 수신

#### `receive_events(timeout=None)`

Windows 메시지 큐에서 이벤트를 수신하는 Generator입니다.

**파라미터:**
- `timeout` (float, optional): 최대 대기 시간(초). `None`이면 무한 대기

**반환값:**
- `Generator[Tuple[WMCAMessage, Any], None, None]`
  - `WMCAMessage`: 메시지 타입 (enum)
  - `Any`: 파싱된 데이터 (메시지 타입에 따라 다름)

**메시지 타입:**

| 메시지 타입 | 설명 | 데이터 타입 |
|------------|------|-----------|
| `CA_CONNECTED` | 로그인 성공 | `LoginBlock` |
| `CA_DISCONNECTED` | 연결 해제 | `None` |
| `CA_SOCKETERROR` | 통신 오류 | (구현 예정) |
| `CA_RECEIVEDATA` | TR 블록 데이터 수신 | `OUTDATABLOCK` |
| `CA_RECEIVESISE` | 실시간 시세 수신 | `OUTDATABLOCK` |
| `CA_RECEIVEMESSAGE` | 상태 메시지 | `OUTDATABLOCK` (메시지) |
| `CA_RECEIVECOMPLETE` | TR 처리 완료 | `OUTDATABLOCK` |
| `CA_RECEIVEERROR` | TR 처리 실패 | `OUTDATABLOCK` |

**예제 1: timeout 지정**

```python
# 최대 10초 대기
for msg_type, data in agent.receive_events(timeout=10.0):
    if msg_type == WMCAMessage.CA_CONNECTED:
        print("로그인 성공!")
        break
# 10초 경과 시 자동 종료
```

**예제 2: 무한 대기**

```python
# 사용자가 명시적으로 break 할 때까지 계속 수신
for msg_type, data in agent.receive_events():
    if msg_type == WMCAMessage.CA_RECEIVESISE:
        print(f"실시간 시세: {data}")
    # break 없이 계속 수신...
```

**예제 3: 특정 TrIndex 응답만 처리**

```python
tr_index = 1001
agent.query(nTRID=tr_index, ...)

for msg_type, data in agent.receive_events(timeout=10.0):
    # TrIndex 확인
    if hasattr(data, 'TrIndex') and data.TrIndex == tr_index:
        if msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
            print("내가 요청한 TR 완료!")
            break
```

**참고:**
- Windows 메시지 펌핑을 자동으로 처리
- `timeout=None`이면 무한 루프 (명시적 `break` 필요)
- 각 메시지는 이미 파싱된 Python 객체로 반환됨

---

## 전체 사용 예제

### 예제 1: 로그인 → 잔고 조회 → 로그아웃

```python
from pynamuh import WMCAAgent, WMCAMessage
from pynamuh.structures.ord.c8201 import Tc8201InBlock

with WMCAAgent() as agent:
    # 1. 로그인
    agent.connect(
        szID="your_id",
        szPW="your_password",
        szCertPW="cert_password"
    )

    # 로그인 응답 대기
    login_success = False
    for msg_type, data in agent.receive_events(timeout=10.0):
        if msg_type == WMCAMessage.CA_CONNECTED:
            print("로그인 성공!")
            login_success = True
            break

    if not login_success:
        print("로그인 실패")
        return

    # 2. 잔고 조회
    password_hash = agent.get_account_hash_password(1, "1234")
    input_data = Tc8201InBlock(
        pswd_noz44=password_hash,
        bnc_bse_cdz1="1"
    )

    tr_index = 1001
    agent.query(nTRID=tr_index, szTRCode="c8201", szInput=input_data, nAccountIndex=1)

    # 잔고 조회 응답 대기
    for msg_type, data in agent.receive_events(timeout=10.0):
        if hasattr(data, 'TrIndex') and data.TrIndex == tr_index:
            if msg_type == WMCAMessage.CA_RECEIVEDATA:
                print(f"블록: {data.pData.szBlockName}")
            elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
                print("조회 완료!")
                break

    # 3. 로그아웃 (with 블록 종료 시 자동 수행)
```

### 예제 2: 실시간 시세 스트리밍

```python
from pynamuh import WMCAAgent, WMCAMessage

with WMCAAgent() as agent:
    # 로그인 (생략)

    # 실시간 체결가 등록
    agent.attach(
        szBCType="j8",
        szInput="005930",  # 삼성전자
        nCodeLen=6,
        nInputLen=6
    )

    # 실시간 데이터 수신 (1분간)
    import time
    start_time = time.time()

    for msg_type, data in agent.receive_events():
        if msg_type == WMCAMessage.CA_RECEIVESISE:
            if data.pData.szBlockName == "j8OutBlock":
                print(f"현재가: {data.pData.szData.price}")

        # 1분 경과 시 종료
        if time.time() - start_time > 60:
            break

    # 실시간 시세 해제
    agent.detach(
        szBCType="j8",
        szInput="005930",
        nCodeLen=6,
        nInputLen=6
    )
```

---

## 지원하는 TR

### 주문 관련 (ord)

| TR 코드 | 설명 | 구현 상태 |
|---------|------|-----------|
| c8201 | 잔고 조회 | ✅ 완료 |
| c0101 | 주식 주문 | 🚧 예정 |
| c0102 | 주식 정정 | 🚧 예정 |

### 시세 관련 (inv)

| TR 코드 | 설명 | 구현 상태 |
|---------|------|-----------|
| j8 | 실시간 현재가 | ✅ 완료 |
| c1101 | 현재가 조회 | 🚧 예정 |

---


## 개발자 가이드

### 현재 구현 상태

현재 다음 TR/실시간 시세만 구현되어 있습니다:
- **TR 조회**: `c8201` (주식잔고조회)
- **실시간 시세**: `j8` (주식 체결가)

나머지 TR은 아래 가이드를 참고하여 직접 구현하실 수 있습니다.

### 새로운 TR 추가 방법

TR을 추가하려면 **Input 구조체**를 정의해야 합니다. (Output 구조체는 선택 사항)

**전체 흐름:**
```
Python 사용자 입력
    ↓
Pydantic Model 생성 (사용자 친화적 인터페이스)
    ↓
to_c_struct() 자동 변환
    ↓
C 구조체 (DLL이 이해하는 형식)
    ↓
WMCA DLL에 전달
```

**정의할 것:**
1. **C 구조체**: DLL에 전달될 최종 형태 (변환 결과 모양)
2. **Pydantic Model**: Python 사용자가 사용할 입력 블록 (입력 필드 + C_STRUCT 지정)

→ 이 둘을 잘 정의하면, C 구조체로의 변환은 내부에서 자동적으로 처리됩니다.

#### 1단계: C 구조체 정의 (변환 결과 모양)

나무증권 OpenAPI 샘플 코드의 `trio_ord.h` 또는 `trio_inv.h`를 참고하여 **DLL에 전달될 최종 형태**인 C 구조체를 정의합니다.

**예시: `c8201` Input 구조체** (`structures/ord/c8201.py`)

```python
import ctypes
from ctypes import Structure

class CTc8201InBlock(Structure):
    """주식잔고조회 입력 블록 C 구조체"""
    _fields_ = [
        ("pswd_noz44", ctypes.c_char * 44),      # 계좌비밀번호
        ("_pswd_noz44", ctypes.c_char * 1),      # 속성 바이트
        ("bnc_bse_cdz1", ctypes.c_char * 1),     # 잔고구분
        ("_bnc_bse_cdz1", ctypes.c_char * 1),    # 속성 바이트
    ]
```

**주의사항:**
- 필드명은 나무증권 SPEC 문서 및 나무증권 샘플 코드의 `trio_ord.h` / `trio_inv.h`와 정확히 일치시킵니다.
- 필드명 앞에 "_"가 붙은 1byte짜리 속성 바이트도 누락되지 않도록 유의하세요.

#### 2단계: Pydantic Model 정의 (Python 사용자 인터페이스)

`structures.common.InBlock`을 상속받아 **Python 사용자가 query()에 넘길 InBlock의 속성**을 정의합니다.

```python
from typing import ClassVar, Type
from pydantic import Field
from ..common import InBlock

class Tc8201InBlock(InBlock):
    """주식잔고조회 입력 블록

    Attributes:
        pswd_noz44: 해시 처리된 계좌비밀번호 (44자)
        bnc_bse_cdz1: 잔고구분 (1~5)
    """

    # (중요!) 1단계에서 정의한 C 구조체를 지정.
    C_STRUCT = CTc8201InBlock

    # 사용자가 입력할 필드만 정의 (속성 바이트는 제외)
    pswd_noz44: str = Field(
        min_length=44,
        max_length=44,
        description="해시 처리된 계좌비밀번호"
    )

    bnc_bse_cdz1: str = Field(
        pattern=r'^[1-5]$',
        description="잔고구분 (1~5)"
    )
```

**핵심:**
- **`C_STRUCT`**: 1단계에서 정의한 C 구조체 클래스를 지정 (변환 결과 모양 지정)
- **필드 정의**: 사용자가 입력할 필드를 정의
- **자동 변환**: 위 C_STRUCT와 InBlock을 예시의 사례와 같이 잘 정의한 후 사용하면 pynamuh가 내부에서 자동적으로 변환해 라이브러리 함수를 호출합니다.



#### 3단계: query() 함수에서 사용

```python
from pynamuh import WMCAAgent
from pynamuh.structures.ord.c8201 import Tc8201InBlock

with WMCAAgent() as agent:
    # 로그인 후...

    # Python 객체 생성
    input_data = Tc8201InBlock(
        pswd_noz44=hash_pwd,
        bnc_bse_cdz1="1"
    )

    # query()에 전달 -> 자동으로 C 구조체로 변환됨!
    agent.query(
        nTRID=1001,
        szTRCode="c8201",
        szInput=input_data,  # Python 객체
        nAccountIndex=1
    )
```

### Output 구조체 추가 (선택 사항)

Output 구조체를 정의하면 **조회 결과를 자동으로 파싱**할 수 있습니다.

**전체 흐름:**
```
WMCA DLL 응답
    ↓
C 구조체 형태의 바이너리 데이터
    ↓
from_c_struct() 자동 파싱
    ↓
Python 클래스 (dataclass)
    ↓
사용자가 편리하게 접근
```

**정의할 것:**
1. **C 구조체**: DLL이 전달하는 응답 데이터 형식 (파싱 대상)
2. **Python 클래스**: 파싱된 데이터를 담을 객체 (사용자가 접근할 속성)

→ 이 둘을 잘 정의하면, 응답 데이터의 파싱은 내부에서 자동적으로 처리됩니다.

#### 1단계: C 구조체 정의 (DLL 응답 형식)

나무증권 샘플 코드의 `trio_ord.h` 또는 `trio_inv.h`를 참고하여 **DLL이 전달하는 응답 데이터 형식**인 C 구조체를 정의합니다.

**예시: `c8201` OutBlock 구조체** (`structures/ord/c8201.py`)

```python
import ctypes
from ctypes import Structure

class CTc8201OutBlock(ctypes.Structure):
    """c8201 잔고조회 Output C 구조체 (계좌 요약 정보)"""
    _fields_ = [
        ("dpsit_amtz16", ctypes.c_char * 16),       # 예수금
        ("_dpsit_amtz16", ctypes.c_char * 1),       # 속성 바이트
        ("mrgn_amtz16", ctypes.c_char * 16),        # 신용융자금
        ("_mrgn_amtz16", ctypes.c_char * 1),
        ("chgm_pos_amtz16", ctypes.c_char * 16),    # 출금가능금액
        ("_chgm_pos_amtz16", ctypes.c_char * 1),
        # ... 기타 필드
    ]
```

**주의사항:**
- Input과 마찬가지로 **속성 바이트(`_필드명`)를 반드시 포함**해야 합니다

#### 2단계: Python 클래스 정의 (파싱 결과)

`@dataclass`와 `OutBlock`을 사용하여 **파싱된 데이터를 담을 Python 객체**를 정의합니다.

```python
from dataclasses import dataclass
from ..common import OutBlock

@dataclass
class Tc8201OutBlock(OutBlock):
    """c8201 잔고조회 OutBlock (계좌 요약 정보)"""

    # 사용자가 접근할 필드만 정의 (속성 바이트는 제외)
    dpsit_amtz16: str        # 예수금
    mrgn_amtz16: str         # 신용융자금
    chgm_pos_amtz16: str     # 출금가능금액
    # ... 기타 필드
```

**핵심:**
- **`@dataclass`**: 어노테이션을 반드시 달아주세요.
- **`OutBlock` 상속**: OutBlock을 상속받아야 자동으로 parsing됩니다.
- 필드를 정의할 때에는 필드명이 나무증권 API 샘플 코드와 동일해야 합니다.

#### 3단계: 파서 정보 등록

정의한 Output 구조체를 **`parser_info.py`에 등록**하여 자동 파싱을 활성화합니다.

```python
# structures/parser_info.py

def get_parser_info(block_name: str) -> tuple[Type[Structure], Type["OutBlock"], bool]:
    """파서 정보 조회"""
    match block_name:
        # 기존 코드...

        # 새로운 TR의 OutBlock 추가
        case "c8201OutBlock":
            from .ord.c8201 import CTc8201OutBlock, Tc8201OutBlock
            return (CTc8201OutBlock, Tc8201OutBlock, False)
        case "c8201OutBlock1":
            from .ord.c8201 import CTc8201OutBlock1, Tc8201OutBlock1
            return (CTc8201OutBlock1, Tc8201OutBlock1, True)  # 반복 블록

        case _:
            raise ValueError(f"아직 Block이 구현되지 않음! : {block_name}")
```

**반환 튜플:**
- 첫 번째: 변환할 C 구조체 클래스
- 두 번째: 변환된 결과로 반환될 Python 클래스
- 세 번째: 반복 블록인지 여부 (`False`: 단일 블록, `True`: 반복 블록, 나무증권 API SPEC 문서 참고)

#### 4단계: 사용 예시

```python
from pynamuh import WMCAAgent, WMCAMessage

with WMCAAgent() as agent:
    # 로그인 및 query 호출 (생략)

    # 응답 수신
    for msg_type, data in agent.receive_events(timeout=10.0):
        if msg_type == WMCAMessage.CA_RECEIVEDATA:
            # 자동으로 파싱된 데이터 접근
            if data.pData.szBlockName == "c8201OutBlock":
                outblock = data.pData.szData  # Tc8201OutBlock 객체
                print(f"예수금: {outblock.dpsit_amtz16}")
                print(f"출금가능금액: {outblock.chgm_pos_amtz16}")
        elif msg_type == WMCAMessage.CA_RECEIVECOMPLETE:
            break
```
---

## 라이선스

MIT License

---

## 기여

이슈 및 PR 환영합니다!

- **Issues**: [https://github.com/odumag99/pynamuh/issues](https://github.com/odumag99/pynamuh/issues)
- **Pull Requests**: [https://github.com/odumag99/pynamuh/pulls](https://github.com/odumag99/pynamuh/pulls)

---

## 작성자

- **GitHub**: [@odumag99](https://github.com/odumag99)
- **Email**: odumag99@gmail.com
