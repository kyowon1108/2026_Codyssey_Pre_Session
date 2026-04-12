import json
import os
import random

STATE_FILE = "state.json"

DEFAULT_QUIZZES = [
    {
        "question": "Python을 만든 사람은?",
        "choices": ["James Gosling", "Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie"],
        "answer": 2
    },
    {
        "question": "Python에서 주석을 나타내는 기호는?",
        "choices": ["//", "/*", "#", "--"],
        "answer": 3
    },
    {
        "question": "Python에서 함수를 정의할 때 사용하는 키워드는?",
        "choices": ["function", "def", "func", "define"],
        "answer": 2
    },
    {
        "question": "Python에서 True와 False는 어떤 타입인가?",
        "choices": ["int", "str", "bool", "float"],
        "answer": 3
    },
    {
        "question": "Python 리스트에서 마지막 요소를 꺼내는 메서드는?",
        "choices": ["pop()", "remove()", "delete()", "discard()"],
        "answer": 1
    },
    {
        "question": "Python에서 딕셔너리를 만들 때 사용하는 괄호는?",
        "choices": ["()", "[]", "{}", "<>"],
        "answer": 3
    },
    {
        "question": "Python에서 None은 어떤 의미인가?",
        "choices": ["0", "빈 문자열", "값이 없음", "False"],
        "answer": 3
    }
]


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        print(f"\n[문제 {number}]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load()

    def load(self):
        if not os.path.exists(STATE_FILE):
            self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
            print("기본 퀴즈 데이터를 사용합니다.")
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data["best_score"]
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except Exception:
            print("⚠️  저장 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
            self.best_score = 0

    def save(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_int_input(self, prompt, min_val, max_val):
        while True:
            raw = input(prompt).strip()
            if not raw:
                print(f"⚠️  입력이 없습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            try:
                val = int(raw)
            except ValueError:
                print(f"⚠️  잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            if not (min_val <= val <= max_val):
                print(f"⚠️  범위를 벗어났습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            return val

    def play(self):
        if not self.quizzes:
            print("\n퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        quiz_list = self.quizzes[:]
        random.shuffle(quiz_list)
        correct = 0

        print(f"\n퀴즈를 시작합니다! (총 {len(quiz_list)}문제)")
        print("-" * 40)

        for i, quiz in enumerate(quiz_list, 1):
            quiz.display(i)
            answer = self.get_int_input("정답 입력: ", 1, 4)
            if quiz.check_answer(answer):
                print("정답입니다!")
                correct += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        total = len(quiz_list)
        score = round(correct / total * 100)
        print("\n========================================")
        print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
            self.save()
        print("========================================")

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        print("-" * 40)

        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("⚠️  문제를 입력하지 않았습니다.")
            return

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if not choice:
                print("⚠️  선택지를 입력하지 않았습니다.")
                return
            choices.append(choice)

        answer = self.get_int_input("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("퀴즈가 추가되었습니다!")

    def show_list(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        if self.best_score == 0:
            print("\n아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"\n최고 점수: {self.best_score}점")

    def show_menu(self):
        print("\n========================================")
        print("          Python 퀴즈 게임")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def run(self):
        actions = {1: self.play, 2: self.add_quiz, 3: self.show_list, 4: self.show_score}
        while True:
            self.show_menu()
            choice = self.get_int_input("선택: ", 1, 5)
            if choice == 5:
                print("종료합니다.")
                break
            actions[choice]()


if __name__ == "__main__":
    try:
        QuizGame().run()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
