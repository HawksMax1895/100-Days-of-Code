import turtle
import pandas as pd

screen = turtle.Screen()
screen.title('U.S. States Game')
image = 'blank_states_img.gif'
screen.addshape(image)
turtle.shape(image)

score = 0
game_is_on = True
guessed_states = []

data = pd.read_csv('50_states.csv')
data['state'].astype(str)
state_list = data['state'].to_list()

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{score}/50 States Correct", prompt="What's another state name?")
    answer_state = answer_state.capitalize()
    if answer_state == 'Exit':
        game_is_on = False
        missing_states = [state for state in state_list if state not in guessed_states]
        # for state in state_list:
        #     if state not in guessed_states:
        #         missing_states.append(state)
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv('states_to_learn.csv')
        break
    for num in range(0, len(state_list)):
        if str(state_list[num]) == answer_state:
            score += 1
            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            state_data = data[data.state == answer_state]
            t.goto(int(state_data.x), int(state_data.y))
            t.write(answer_state)
            guessed_states.append(answer_state)









turtle.mainloop()