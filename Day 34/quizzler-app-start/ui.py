from multiprocessing.connection import answer_challenge
from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = Canvas(width=300, height=250)
        self.canvas.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
        self.question_text = self.canvas.create_text(150, 125, text="Question", font=("Arial", 16, "italic"), width=290)

        pic_right = PhotoImage(file="images/true.png")
        self.button_right = Button(image=pic_right, command=self.check_true)
        self.button_right.grid(column=0, row=2, pady=20, padx=20)

        pic_wrong = PhotoImage(file="images/false.png")
        self.button_wrong = Button(image=pic_wrong, command=self.check_false)
        self.button_wrong.grid(column=1, row=2, pady=20, padx=20)

        self.score = Label(text="Score: 0", bg=THEME_COLOR, fg="White")
        self.score.grid(column=1, row=0, pady=20, padx=20)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="White")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.score.config(text=f"Score: {self.quiz.score}")
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the Quiz")
            self.button_wrong.config(state="disabled")
            self.button_right.config(state="disabled")

    def check_true(self):
        answer = self.quiz.check_answer("True")
        self.give_feedback(answer)

    def check_false(self):
        answer = self.quiz.check_answer("False")
        self.give_feedback(answer)

    def give_feedback(self, answer):
        if answer:
            self.canvas.config(bg="Green")
        else:
            self.canvas.config(bg="Red")
        self.window.after(1000, self.get_next_question)
