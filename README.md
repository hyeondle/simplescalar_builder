# cache_tester
ynu computer architecture subject, cache analyze

## 요구사항

### 도커 및 운영체제
- **MacOS**
  - **하위 버전의 Docker**: 아래 명령어를 실행하여 qemu를 설치한 후 사용하세요.
    ```bash
    make help
    ```
    qemu 설치 후, 다음 명령어를 실행합니다:
    ```bash
    make set
    ```
  - **최신 버전의 Docker**: Docker vmm을 사용할 것.

### 기타 요구사항
- Python 3
- Python 패키지:
  ```bash
  pip install requests
  ```

## 실행 방법

### 전체 빌드 및 실행
```bash
make all
```
위 명령어는 리눅스 환경의 컨테이너를 빌드하고 입력 프로그램을 실행합니다.

### 실행 결과
실행 결과는 data 폴더에 저장됩니다.

### 결과 변환
실행 내역의 수치를 CSV 파일로 변환하려면 아래 명령어를 실행하세요:
```bash
bash script.sh <결과 텍스트 파일>
```

## 종료 방법

입력 프로그램 실행 중 종료를 원할 경우, `Ctrl+C`를 입력하여 프로그램을 종료할 수 있습니다.


