# Python 퀴즈 게임

## 프로젝트 개요

- Python 기초 퀴즈 게임
- 퀴즈 풀기, 퀴즈 추가, 목록 확인, 최고 점수 관리 기능을 제공하며,
데이터는 `state.json`에 저장되어 프로그램을 재시작해도 유지됨.

## 실행 방법

```bash
cd mission2
python main.py
```

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
        ├── menu.png
        ├── play.png
        ├── add_quiz.png
        └── score.png
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

---

## 실행 화면

### 메뉴 화면

![메뉴 화면](docs/screenshots/menu.png)

### 퀴즈 풀기

![퀴즈 풀기](docs/screenshots/play.png)

### 퀴즈 추가

![퀴즈 추가](docs/screenshots/add_quiz.png)

### 점수 확인

![점수 확인](docs/screenshots/score.png)

---

## Git 이력

### git log --oneline --graph

```
* c803b12 Docs: 실행 화면 스크린샷 추가 (menu, play, add_quiz, score)
* 6a52926 Docs: README 실습 주석 제거
* c24caff Docs: 2번 과제 명세 파일 추가
* 4896bde Docs: clone/pull 실습 확인용 커밋
* d2027dc Docs: README에 주제 선정 이유, 기능 목록, 파일 구조, state.json 설명 추가
* dff98b2 Feat: .gitignore에 state.json, __pycache__ 추가
* c02141d Docs: README 간결하게 수정
* 9608090 Feat: 퀴즈 게임 초기 구현 (Quiz/QuizGame 클래스, 기본 퀴즈 7개, README)
* 81dad12 Refactor: 1번 과제를 mission1/으로 이동, 2번 과제 디렉터리 구조 생성
* 845d36f add: add E1-1
* 90cd23d Initial commit
```

### 브랜치 생성 및 병합

`feature/gitignore` 브랜치를 생성해 `.gitignore` 업데이트 작업을 진행한 뒤 `main`으로 병합

```bash
git checkout -b feature/gitignore   # 브랜치 생성 및 이동
# .gitignore 수정 후
git add .gitignore
git commit -m "Feat: .gitignore에 state.json, __pycache__ 추가"
git checkout main
git merge feature/gitignore         # main으로 병합
```

### clone / pull 실습

```bash
# 1. clone: 저장소를 별도 디렉터리에 복제
git clone https://github.com/kyowon1108/2026_Codyssey_Pre_Session.git /tmp/codyssey_clone

# 2. 복제된 저장소에서 변경 후 push
cd /tmp/codyssey_clone
echo "" >> mission2/README.md
git commit -am "Docs: clone/pull 실습 확인용 커밋"
git push origin main

# 3. 원래 디렉터리에서 pull로 변경사항 수신
cd ~/Projects/.../2026_Codyssey_Pre_Session
git pull origin main
# → mission2/README.md 변경사항이 반영됨 확인
```

---

## 설계 설명

### Quiz / QuizGame 클래스 책임 분리

- **Quiz**: 퀴즈 한 문제를 표현하는 단위 객체이고, 문제 출력(`display`)과 정답 확인(`check_answer`) 같이 퀴즈 자체에 관한 동작만 담당함.
- **QuizGame**: 게임 전체 흐름을 관리함. 퀴즈 목록 유지, 메뉴 출력, 기능 실행, 파일 저장/불러오기를 담당함.

이렇게 나누면 퀴즈 한 문제의 로직이 바뀌어도 `Quiz`만 수정하면 되고, 게임 흐름이 바뀌면 `QuizGame`만 수정하면 됨.

### 로직 분리 기준

| 역할 | 메서드 | 설명 |
| --- | --- | --- |
| 입력 처리/검증 | `get_int_input()` | 빈값·문자·범위 오류를 한 곳에서 처리 |
| 게임 진행 | `play()` | 출제, 정답 판정, 점수 계산 |
| 퀴즈 관리 | `add_quiz()`, `show_list()` | 등록 및 목록 출력 |
| 점수 관리 | `show_score()` | 최고 점수 표시 |
| 데이터 저장/불러오기 | `save()`, `load()` | state.json 읽기·쓰기 |

### state.json 읽기/쓰기 흐름

```
프로그램 시작
  └─ QuizGame.__init__() → load()
       ├─ state.json 없음 → 기본 퀴즈 7개 사용
       └─ state.json 있음 → 퀴즈 목록 + 최고점수 로드

퀴즈 추가 또는 점수 갱신 시
  └─ save() → state.json 덮어쓰기 (UTF-8)

프로그램 종료
  └─ 별도 저장 없음 (변경 시점마다 즉시 저장하는 방식)
```

### Ctrl+C / EOF 안전 종료

```python
if __name__ == "__main__":
    try:
        QuizGame().run()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
```

`KeyboardInterrupt`(Ctrl+C)와 `EOFError`(입력 스트림 종료) 두 경우를 최상위에서 잡아 안내 메시지를 출력하고 종료함. 데이터는 변경 시점마다 즉시 저장하므로 이 시점에 별도 저장이 필요 없음.

### 커밋 단위 및 메시지 규칙

| 접두어 | 의미 | 예시 |
| --- | --- | --- |
| `Feat` | 새 기능 추가 | `Feat: 퀴즈 게임 초기 구현` |
| `Docs` | 문서 작성/수정 | `Docs: README 기능 목록 추가` |
| `Refactor` | 구조 변경 (동작 유지) | `Refactor: 1번 과제 mission1/으로 이동` |
| `Fix` | 버그 수정 | `Fix: 점수 계산 오류 수정` |

### 클래스를 사용한 이유

함수만 사용하면 퀴즈 데이터(문제, 선택지, 정답)를 여러 변수로 따로 관리해야 하지만, 클래스를 쓰면 관련 데이터와 동작을 하나로 묶을 수 있어 코드가 명확해짐.

예를 들어 `quiz.check_answer(3)`처럼 퀴즈 객체 스스로 정답을 판단하게 만들 수 있지만, 반면 함수 방식이면 `check_answer(question, choices, answer, 3)` 식으로 데이터를 계속 전달해야 함.

### JSON 파일 저장 이유

- 텍스트 형식이라 사람이 직접 읽고 수정하기 용이함.
- Python 표준 라이브러리 `json`으로 바로 읽고 쓸 수 있음.
- 딕셔너리·리스트 구조를 그대로 저장할 수 있어 퀴즈 데이터 형태와 잘 맞음.

### 파일 입출력에서 try/except가 필요한 이유

파일 작업은 프로그램 외부 환경(디스크, OS)에 의존하므로 예측 불가능한 오류가 발생할 수 있음.

- 파일이 다른 프로그램에 의해 손상된 경우 → `json.JSONDecodeError`
- 디스크 읽기 실패 → `IOError`

이런 오류를 처리하지 않으면 프로그램이 즉시 종료됨. `try/except`로 감싸면 오류가 발생해도 기본 데이터로 복구하고 실행을 계속할 수 있음.

### 브랜치 분리 이유 및 병합의 의미

브랜치를 만들면 `main`의 안정된 코드를 건드리지 않고 새 작업을 진행할 수 있음. 작업이 완료되고 검증된 후에 `main`에 병합하므로, 개발 중인 코드가 배포 코드에 영향을 주지 않습니다. 팀 협업에서는 각자 브랜치에서 작업한 뒤 PR(Pull Request)로 검토 후 병합하는 방식으로 확장됨.

### state.json 데이터 구조 설계 이유

```json
{
  "quizzes": [...],
  "best_score": 100
}
```

- 최상위를 딕셔너리로 만들어 키로 데이터 종류를 구분함.
- 나중에 `score_history` 같은 항목을 추가해도 기존 키에 영향을 주지 않음. 
- `quizzes`는 리스트로, 각 퀴즈는 딕셔너리로 저장해 `Quiz` 객체와 1:1로 대응되도록 설계함.

### 퀴즈 데이터 증가 시 JSON 방식의 한계

- 퀴즈가 수천 개가 되면 매번 전체 파일을 읽고 쓰므로 속도가 느려짐.
- 동시에 두 프로세스가 저장하면 데이터가 겹쳐 쓰일 수 있음(동시성 문제).
- 검색이나 정렬 기능이 필요해지면 코드로 직접 구현해야 함.

이런 상황이 되면 SQLite 같은 경량 데이터베이스로 전환하는 것이 적합함.

### state.json 손상 시 대응 방안

현재 구현에서는 `load()` 안의 `try/except`가 손상된 파일을 감지하면 기본 퀴즈 데이터로 초기화함.

```python
except Exception:
    print("⚠️  저장 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
    self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
    self.best_score = 0
```

추가 대응 방안으로는 저장 전 백업 파일(`state.json.bak`)을 만들어두면 손상 시 복구가 가능함.

### 요구사항 변경 시 수정 위치

| 변경 내용 | 수정 위치 |
| --- | --- |
| 선택지 개수를 4개 → 5개로 변경 | `Quiz` 클래스, `add_quiz()`, DEFAULT_QUIZZES |
| 메뉴 항목 추가 | `show_menu()`, `run()` |
| 점수 계산 방식 변경 | `play()` |
| 저장 파일 경로 변경 | `STATE_FILE` 상수 |
| 데이터 형식 변경 | `save()`, `load()`, `Quiz.to_dict()`, `Quiz.from_dict()` |
