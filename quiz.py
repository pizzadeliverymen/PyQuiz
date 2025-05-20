import random
import requests
from tkinter import *
from tkinter import ttk
from html import unescape
from dataclasses import dataclass

@dataclass
class Question:
    question: str
    correct_answer: str
    all_answers: list
    category: str
    type: str
    difficulty: str


class Quiz:
    def __init__(self, root):
        self.root = root
        root.title("A test quiz")
        # self.base_url= "https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple"
        self.base_url = "https://opentdb.com/api.php?"
        self.amount = 3
        self.type = "multiple"
        self.difficulty = "easy"
        self.category = -1
        self.points = 0
        self.total = 0
        
        self.call_categories()

        self.options_gui()

        
        # self.setup_gui(root)
        # self.call_url()
        # self.ask_questions()
        # root.destroy()
    

    def update_cat(self, cat):
        for category in self.category_list:
            if category[1] == cat:
                self.category = category[0]
                break
    
    def update_diff(self, diff):
        self.difficulty = diff.lower()

    def update_amount(self, amount):
        self.amount = int(amount)

    def options_gui(self):
        root = self.root
        for child in root.winfo_children():
            child.destroy()
        root.title("A test quiz")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe = mainframe
        Label(mainframe, text="Welcome to the quiz!").grid(row=0, column=0, columnspan=2)
        Label(mainframe, text="Select Category:").grid(row=1, column=0)
        cats = []
        for category in self.category_list:
            cats.append(category[1])
        cat_choice = StringVar(value=cats[0])
        OptionMenu(mainframe, cat_choice, *cats, command=self.update_cat).grid(row=1, column=1)

        Label(mainframe, text="Select Difficulty:").grid(row=2, column=0)
        diff_choice = StringVar(value="Easy")
        difficulties = ["Easy", "Medium", "Hard"]
        OptionMenu(mainframe, diff_choice, *difficulties, command=self.update_diff).grid(row=2, column=1)

        Label(mainframe, text="Select Amount:").grid(row=3, column=0)
        amounts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        amount_choice = StringVar(value=3)
        OptionMenu(mainframe, amount_choice, *amounts,command=self.update_amount).grid(row=3, column=1)

        start_button = ttk.Button(mainframe, text="Start Quiz", command=self.call_url)
        start_button.grid(row=4, column=0, columnspan=2)
        # self.choice

    def setup_gui(self):
        root = self.root
        for child in root.winfo_children():
            child.destroy()
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.title_text = StringVar()
        self.title_text.set("A test quiz")
        root.title(self.title_text.get())
        self.q_index = 0

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.question = StringVar()
        self.question_title = ttk.Label(mainframe, textvariable=self.question)
        self.question_title.grid(column=0, row=1, sticky=(W, E))

        self.choice = StringVar(mainframe, "-1")

        self.buttonList = []

        for i in range(4):
            rb = Radiobutton(mainframe, text=i, variable=self.choice, value=i)
            rb.grid(column=0, row=i+2, sticky=(W, E))
            self.buttonList.append(rb)

        next_button = ttk.Button(mainframe, text="Next", command=self.new_question)
        next_button.grid(column=0, row=6, sticky=W)
        
        root.bind("<Return>")

    def new_question(self):
        if self.choice.get() != "-1":
            if self.question_list[self.q_index].all_answers[int(self.choice.get())] == self.question_list[self.q_index].correct_answer:
                self.points += 1
            self.choice.set("-1")
            self.q_index += 1
        if self.q_index < len(self.question_list):
            question = self.question_list[self.q_index]
            self.title_text.set(question.category)
            self.root.title(self.title_text.get())
            self.question.set(question.question)
            for j, answer in enumerate(question.all_answers):
                self.buttonList[j].config(text=answer)
        else:
            print("No more questions available.")
            print(f"You scored {self.points} points.")
            self.finished()

    def call_categories(self):
        self.category_list = [(-1,'Any')]
        try:
            categories = requests.get("https://opentdb.com/api_category.php", timeout=2).json()
            for category in categories["trivia_categories"]:
                add = (category["id"], category["name"])
                self.category_list.append(add)
        except requests.exceptions.RequestException as e:
            print("Error fetching categories:", e)
        # print(self.category_list)

    def call_url(self):
        self.setup_gui()
        to_call = self.create_url()
        x = requests.get(to_call)
        self.manage_questions(x.json())

    def finished(self):
        print("Finished")
        root = self.root
        for child in root.winfo_children():
            child.destroy()
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.title_text = StringVar()
        self.title_text.set("Score: " + str(self.points) + "/" + str(self.total))
        root.title(self.title_text.get())
        Label(mainframe, textvariable=self.title_text).grid(row=0, column=0, columnspan=2)

        ttk.Button(mainframe, text="Quit", command=root.quit).grid(row=1, column=0, columnspan=2)
        ttk.Button(mainframe, text="Play Again", command=self.options_gui).grid(row=2, column=0, columnspan=2)


    def manage_questions(self, response):
        self.question_list = []
        for question in response["results"]:
            all_answers = [ unescape(answer) for answer in question["incorrect_answers"]]
            correct_answer = unescape(question["correct_answer"])
            all_answers.append(correct_answer)
            random.shuffle(all_answers)
            q = Question(
                question=unescape(question["question"]),
                correct_answer=unescape(question["correct_answer"]),
                all_answers=all_answers,
                category=question["category"],
                type=question["type"],
                difficulty=question["difficulty"]
            )
            self.question_list.append(q)
            self.total += 1
        
        # self.print_questions()
        self.new_question()
        

    def print_questions(self):
        for question in self.question_list:
            print(f"Question: {question.question}")


    def create_url(self):
        full_url = self.base_url
        if self.amount:
            full_url += f"amount={self.amount}&"
        if self.difficulty:
            full_url += f"difficulty={self.difficulty}&"
        if self.type:
            full_url += f"type={self.type}&"
        if self.category != -1:
            full_url += f"category={self.category}&"
        if full_url.endswith("&"):
            full_url = full_url[:-1]
        return full_url

root = Tk()
Quiz(root)
root.mainloop()