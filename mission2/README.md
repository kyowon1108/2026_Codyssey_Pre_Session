# Python 퀴즈 게임

## 프로젝트 개요

- Python 기초 퀴즈 게임
- 퀴즈 풀기, 퀴즈 추가, 목록 확인, 최고 점수 관리 기능을 제공하며, 데이터는 `state.json`에 저장되어 프로그램을 재시작해도 유지됨

## 실행 방법

```bash
cd mission2
python main.py
```

Python 3.10 이상 필요. 외부 라이브러리 없음.

## 기능 목록

| 번호 | 기능 | 설명 |
| --- | --- | --- |
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 랜덤 순서로 출제, 결과 및 점수 표시 |
| 2 | 퀴즈 추가 | 문제/선택지 4개/정답 번호를 입력해 새 퀴즈 등록 |
| 3 | 퀴즈 목록 | 등록된 퀴즈 전체 목록 확인 |
| 4 | 점수 확인 | 지금까지의 최고 점수 확인 |
| 5 | 종료 | 프로그램 종료 |

## 파일 구조

```
mission2/
├── main.py              # 메인 실행 파일
├── state.json           # 퀴즈 데이터 및 최고 점수 저장 (자동 생성)
└── docs/
    └── screenshots/     # 실행 화면 스크린샷
```

## 데이터 파일 설명 (state.json)

- **경로**: `mission2/state.json`
- **역할**: 퀴즈 목록과 최고 점수를 영속적으로 저장
- **인코딩**: UTF-8
- **생성 시점**: 첫 퀴즈 추가 또는 점수 갱신 시 자동 생성

```json
{
  "quizzes": [
    {
      "question": "Python을 만든 사람은?",
      "choices": ["James Gosling", "Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie"],
      "answer": 2
    }
  ],
  "best_score": 100
}
```
