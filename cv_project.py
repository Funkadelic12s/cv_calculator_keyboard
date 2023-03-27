import cv2
import mediapipe as mp
import cvzone
import time
from winsound import *


number = 0                                                   # 0 - choice, 1 - calculator, 2 - keyboard
keys_calc = [
    ['7', '8', '9', '/', 'C'],
    ['4', '5', '6', '*', '<'],
    ['1', '2', '3', '-'],
    ['0', ',', '+', '=']
]                                           # calculator button.text

keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '<'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ' ', 'Ent']
]                                                # keyboard button.text


class Button:                                               # class for calculator and keyboard buttons
    def __init__(self, pos, text, size=[110, 120]):
        self.pos = pos
        self.text = text
        self.size = size


button_list = []                                           # list of calculator buttons
for i in range(len(keys_calc)):
    for j, key in enumerate(keys_calc[i]):
        if i == 3:                                      # 3 row
            button_list.append(Button([120 * j + 720, 140 * i + 20], key))
        else:
            button_list.append(Button([120*j + 600, 140*i+20], key))

keyboard_list = []                                         # list of keyboard buttons
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        keyboard_list.append(Button([120 * j + 30, 170 * i + 20], key))


class Project:
    def __init__(self):                                 # all you need to find hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.draw = mp.solutions.drawing_utils
        self.text = ''
        self.final_text = ''

    def find_hands(self, img):                        # find 21 landmarks
        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
        return img

    def point(self, img):                              # point finger
        global number, volume
        if number == 1:                                # calculator
            # draw calculator text
            cv2.rectangle(img, (15, 55), (380, 170), (155, 155, 0), cv2.FILLED)
            cv2.putText(img, self.text, (25, 125), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 255, 255), 4)
            # draw exit to choice between calculator and keyboard
            cv2.rectangle(img, (405, 55), (570, 170), (105, 105, 255), cv2.FILLED)
            cv2.putText(img, 'Exit', (425, 125), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 255, 255), 4)
            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    h, w, color = img.shape
                    x8, y8 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                    x12, y12 = int(hand.landmark[12].x * w), int(hand.landmark[12].y * h)
                    cv2.circle(img, (x8, y8), 14, (100, 0, 0), cv2.FILLED)
                    # exit
                    if 405 < x8 < 570 and 55 < y8 < 170:
                        cv2.rectangle(img, (405, 55), (570, 170), (5, 25, 255), cv2.FILLED)
                        cv2.putText(img, 'Exit', (425, 125), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 255), 4)
                        if 405 < x12 < 570 and 55 < y12 < 170:
                            PlaySound('click.wav', SND_ASYNC)
                            time.sleep(0.30)
                            number = 0
                    for button in button_list:                         # calculator basics
                        x, y = button.pos
                        w, h = button.size
                        if x < x8 < x + w and y < y8 < y + h:
                            cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (150, 150, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                                        4, (255, 255, 255), 4)
                            if x < x12 < x + w and y < y12 < y + h:
                                if button.text == '=':
                                    PlaySound('click.wav', SND_ASYNC)
                                    t = eval(self.text)
                                    self.text = str(t)
                                    time.sleep(0.3)
                                elif button.text == 'C':
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.text = ''
                                    time.sleep(0.3)
                                elif button.text == '<':
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.text = self.text[:-1]
                                    time.sleep(0.3)
                                else:
                                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (150, 150, 150),
                                                  cv2.FILLED)
                                    cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                                                4, (255, 255, 255), 4)
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.text += button.text
                                    time.sleep(0.3)
        elif number == 0:                                                # choice
            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    h, w, color = img.shape
                    x8, y8 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                    x12, y12 = int(hand.landmark[12].x * w), int(hand.landmark[12].y * h)
                    cv2.circle(img, (x8, y8), 14, (100, 0, 0), cv2.FILLED)
                    if 950 < x8 < 1220 and 10 < y8 < 172:                 # turn keyboard
                        if 950 < x12 < 1220 and 10 < y12 < 172:
                            PlaySound('click.wav', SND_ASYNC)
                            time.sleep(0.30)
                            number = 2
                    if 770 < x8 < 930 and 10 < y8 < 172:                  # turn calculator
                        if 770 < x12 < 930 and 10 < y12 < 172:
                            PlaySound('click.wav', SND_ASYNC)
                            time.sleep(0.30)
                            number = 1
        elif number == 2:                                                    # keyboard
            cv2.rectangle(img, (30, 550), (1010, 680), (255, 191, 0), cv2.FILLED)   # draw text
            cv2.putText(img, self.final_text, (50, 600), cv2.FONT_HERSHEY_PLAIN,
                        4, (255, 255, 205), 4)
            cv2.rectangle(img, (1050, 550), (1200, 680), (105, 105, 255), cv2.FILLED)  # draw exit
            cv2.putText(img, 'Exit', (1100, 600), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 255, 255), 4)

            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    h, w, color = img.shape
                    x8, y8 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                    x12, y12 = int(hand.landmark[12].x * w), int(hand.landmark[12].y * h)
                    cv2.circle(img, (x8, y8), 15, (0, 0, 0), cv2.FILLED)
                    if 1050 < x8 < 1200 and 550 < y8 < 680:                                # turn exit
                        cv2.rectangle(img, (1050, 550), (1200, 680), (5, 25, 255), cv2.FILLED)
                        cv2.putText(img, 'Exit', (1100, 600), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 255), 4)
                        if 1050 < x12 < 1200 and 550 < y12 < 680:
                            PlaySound('click.wav', SND_ASYNC)
                            time.sleep(0.30)
                            number = 0

                    for button in keyboard_list:
                        x, y = button.pos
                        w, h = button.size
                        if x < x8 < x + w and y < y8 < y + h:
                            if button.text == 'Ent':
                                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x, y + 40), cv2.FONT_HERSHEY_PLAIN,
                                            2, (255, 255, 255), 4)
                                if x < x12 < x + w and y < y12 < y + h:
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.final_text = ''
                                    time.sleep(0.3)
                            elif button.text == '<':
                                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x, y + 40), cv2.FONT_HERSHEY_PLAIN,
                                            2, (255, 255, 255), 4)
                                if x < x12 < x + w and y < y12 < y + h:
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.final_text = self.final_text[:-1]
                                    time.sleep(0.3)
                            else:
                                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                                            4, (255, 0, 205), 4)
                                if x < x12 < x + w and y < y12 < y + h:
                                    cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 128), cv2.FILLED)
                                    cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                                                4, (255, 0, 205), 4)
                                    PlaySound('click.wav', SND_ASYNC)
                                    self.final_text += button.text
                                    time.sleep(0.30)
        return img


def draw_butts(img, img_clava, img_cal, button_list, klava_list):                       # draw buttons
    if number == 0:                      # draw keyboard and calculator
        img = cvzone.overlayPNG(img, img_clava, [950, 10])
        img = cvzone.overlayPNG(img, img_cal, [770, 10])
    elif number == 1:                                   # calculator
        for button in button_list:
            x, y = button.pos
            w, h = button.size
            if button.text == '=':
                cv2.rectangle(img, button.pos, (x + w, y + h), (100, 250, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)
            elif button.text == 'C':
                cv2.rectangle(img, button.pos, (x + w, y + h), (100, 100, 250), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)
            else:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)
    elif number == 2:                                                      # keyboard
        for button in klava_list:
            x, y = button.pos
            w, h = button.size
            if button.text == 'Ent':
                cv2.rectangle(img, button.pos, (x + w, y + h), (205, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 40), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 255, 255), 4)
            else:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 191, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)
    return img


def main():
    camera = cv2.VideoCapture(0)
    img_clava = cv2.imread('pngegg.png', cv2.IMREAD_UNCHANGED)
    img_clava = cv2.resize(img_clava, (270, 162))
    img_cal = cv2.imread('kal.png', cv2.IMREAD_UNCHANGED)
    project = Project()

    while True:
        _, img = camera.read()
        img = cv2.flip(img, 180)                                     # flip the image
        img = cv2.resize(img, (1280, 960))
        project.find_hands(img)                                      # find hands
        # draw buttons
        img = draw_butts(img, img_clava=img_clava, img_cal=img_cal, button_list=button_list, klava_list=keyboard_list)
        img = project.point(img)                            # point finger

        cv2.imshow('result', img)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
