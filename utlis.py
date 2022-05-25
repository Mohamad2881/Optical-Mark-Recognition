import cv2
import numpy as np
from datetime import datetime
import csv


def pre_process(img_path):
    img = cv2.imread(img_path)
    # img = cv2.resize(img, (794, 1123))
    # print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
    img_thresh = cv2.threshold(img_gray, 160, 255, cv2.THRESH_BINARY_INV)[1]  # APPLY THRESHOLD AND INVERSE
    return img, img_thresh


def split_1(img_thresh, img_coords, no_of_blocks, no_of_block_quest, no_of_choices):
    q_x, q_y, q_w, q_h = img_coords

    # 2D(questions x choices) array TO STORE THE NON ZERO VALUES OF EACH BOX
    pixel_val = np.zeros((no_of_blocks*no_of_block_quest, no_of_choices))

    # img_thresh = img_thresh[q_y+5:q_y + q_h-13, q_x:q_x + q_w-23]  # Outer bounding rectangle
    img_thresh = img_thresh[q_y:q_y + q_h, q_x:q_x + q_w]  # Outer bounding rectangle
    # cv2.imshow("imgContours", img_thresh)
    # cv2.waitKey(0)

    cells = []
    for i in range(no_of_blocks):
        w = 114*i
        b = img_thresh[:, 29+w-1:29+w+90+1]
        # print(b.shape)
        # cv2.imshow("imgCo'ntours", b[11-3:365+3, :])
        # cv2.waitKey(0)

        rows = np.vsplit(b[11 - 3:365 + 3, :], no_of_block_quest)

        for ir, r in enumerate(rows):
            # print(r.shape)
            # cv2.imshow("imgContosurss", r)
            # cv2.waitKey(0)

            cols = np.hsplit(r, no_of_choices)

            for iy, c in enumerate(cols):
                cells.append(c)
                total_pixels = cv2.countNonZero(c)
                pixel_val[ir+(i*no_of_block_quest)][iy] = total_pixels

                # cv2.imwrite(f"out/{idx}.jpg", c)
                # idx += 1
                # cv2.imshow("imgCosntosur", c)
                # cv2.waitKey(0)
    # print(len(cells))
    return pixel_val


def user_ans(pixel_val, no_of_blocks, no_of_block_quest, labels, ans, thresh):
    no_of_quests_1 = no_of_blocks * no_of_block_quest
    choice_index = []  # Index of user choice
    user_choices = []

    for x in range(0, no_of_quests_1):
        arr = pixel_val[x]

        # get user ans label(s)
        choices = " or ".join([labels[idx] for idx, i in enumerate(arr > thresh) if i ])
        user_choices.append(choices)

        # Ensure that only one circle (ans) is well marked
        if sum(arr > thresh) == 1:
            myIndexVal = np.where(arr == np.amax(arr))
            choice_index.append(myIndexVal[0][0])
        else:
            choice_index.append(-1)

    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    grading = []
    for x in range(0, no_of_quests_1):
        if ans[x] == choice_index[x]:
            grading.append(1)
        else:
            grading.append(0)

    return choice_index, user_choices, grading


def split_2(img_thresh, img_coords, no_of_blocks, no_of_block_quest, no_of_choices):
    # q_x, q_y = 47, 776
    # q_w, q_h = 658, 88

    # c1_x, c1_y = 29, 11
    # c2_x, c2_y = 53, 35
    # c_w, c_h = 18, 18
    #
    # no_of_blocks = 10
    # no_of_block_quest = 3
    # no_of_choices = 2

    q_x, q_y, q_w, q_h = img_coords

    # 2D(questions x choices) array TO STORE THE NON ZERO VALUES OF EACH BOX
    pixel_val = np.zeros((no_of_blocks*no_of_block_quest, no_of_choices))

    img_thresh = img_thresh[q_y:q_y + q_h, q_x :q_x + q_w]  # Outer bounding rectangle
    # cv2.imshow("imgContours", img_thresh)
    # cv2.waitKey(0)

    cells = []
    # idx = 1
    for i in range(no_of_blocks):  # __no_of_blocks
        if i < 3:
            w = 60 * i
        else:
            w = (60*2) + (66 * (i-2))

        b = img_thresh[:, 23+w-2:23+w+42+2]
        # cv2.imshow("imgContourss", b)
        # cv2.waitKey(0)

        rows = np.vsplit(b[11-3:77+3, :], no_of_block_quest) # __no_of_block_quest

        for ir, r in enumerate(rows):
            # print(r.shape)
            # cv2.imshow("imgContosurss", r)
            # cv2.waitKey(0)

            cols = np.hsplit(r, no_of_choices) # __no_of_choices

            for iy, c in enumerate(cols):
                cells.append(c)
                total_pixels = cv2.countNonZero(c)
                pixel_val[ir+(i*no_of_block_quest)][iy] = total_pixels

                # cv2.imwrite(f"out/{idx}.jpg", c)
                # idx += 1
                # cv2.imshow("imgContosur", c)
                # cv2.waitKey(0)
    # print("ds>>", len(cells))
    return pixel_val


def user_ans_2(pixel_val, no_of_blocks, no_of_block_quest, labels, ans, thresh):
    no_of_quests_1 = no_of_blocks * no_of_block_quest
    choice_index = []  # Index of user choice
    user_choices = []

    for x in range(0, no_of_quests_1):
        arr = pixel_val[x]

        # get user ans label(s)
        choices = " or ".join([labels[idx] for idx, i in enumerate(arr > thresh) if i ])
        user_choices.append(choices)

        # Ensure that only one circle (ans) is well marked
        if sum(arr > thresh) == 1:
            myIndexVal = np.where(arr == np.amax(arr))
            choice_index.append(myIndexVal[0][0])
        else:
            choice_index.append(-1)

    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    grading = []
    for x in range(0, no_of_quests_1):
        if ans[x] == choice_index[x]:
            grading.append(1)
        else:
            grading.append(0)



    return choice_index, user_choices, grading


def evaluate_1(img_path, img_coords, quest_specs, thresh):
    no_of_blocks_1, no_of_block_quest_1, no_of_choices_1, labels_1, ans_1 = quest_specs[0]

    img, img_thresh = pre_process(img_path)

    pixel_val_1 = split_1(img_thresh, img_coords[0], no_of_blocks_1, no_of_block_quest_1, no_of_choices_1)

    choice_index_1, user_choices_1, grading_1 = user_ans(pixel_val_1, no_of_blocks_1, no_of_block_quest_1, labels_1, ans_1, thresh[0])
    # print(choice_index_1)
    # print(user_choices_1)

    # Question 2
    no_of_blocks_2, no_of_block_quest_2, no_of_choices_2, labels_2, ans_2 = quest_specs[1]
    pixel_val_2 = split_2(img_thresh, img_coords[1], no_of_blocks_2, no_of_block_quest_2, no_of_choices_2)
    choice_index_2, user_choices_2, grading_2 = user_ans_2(pixel_val_2, no_of_blocks_2, no_of_block_quest_2, labels_2, ans_2, thresh[1])


    gray_1_count = choice_index_1.count(-1)
    gray_2_count = choice_index_2.count(-1)

    # Show use Q1 Answers
    for i in range(no_of_blocks_1):
        w = 114 * i
        for j in range(no_of_block_quest_1):
            user_ans_index = choice_index_1[j + (i * no_of_block_quest_1)]
            grad = grading_1[j + (i * no_of_block_quest_1)]
            correct_ans = ans_1[j + (i * no_of_block_quest_1)]
            if user_ans_index == -1:
                color = (255, 0, 0)
                cv2.circle(img, (47 + 29 + 9 + (24 * user_ans_index) + w, 370 + 11 + 9 + (24 * j)), 6, color,
                           cv2.FILLED)
                cv2.circle(img, (47 + 29 + 9 + (24 * correct_ans) + w, 370 + 11 + 9 + (24 * j)), 6, (0, 255, 0),
                           cv2.FILLED)

            elif grad == 0:
                color = (0, 0, 255)
                cv2.circle(img, (47 + 29 + 9 + (24 * user_ans_index) + w, 370 + 11 + 9 + (24 * j)), 6, color,
                           cv2.FILLED)
                cv2.circle(img, (47 + 29 + 9 + (24 * correct_ans) + w, 370 + 11 + 9 + (24 * j)), 6, (0, 255, 0),
                           cv2.FILLED)


    # Show use Q2 Answers
    for i in range(no_of_blocks_2):  # __no_of_blocks
        if i < 3:
            w = 60 * i
        else:
            w = (60 * 2) + (66 * (i - 2))

        for j in range(no_of_block_quest_2):  # __no_of_block_quest
            user_ans_index = choice_index_2[j + (i * no_of_block_quest_2)]
            grad = grading_2[j + (i * no_of_block_quest_2)]
            correct_ans = ans_2[j + (i * no_of_block_quest_2)]
            if user_ans_index == -1:
                color = (255, 0, 0)
                cv2.circle(img, (47 + 23 + 9 + (24 * user_ans_index) + w, 776 + 11 + 9 + (24 * j)), 6, color,
                           cv2.FILLED)
                cv2.circle(img, (47 + 23 + 9 + (24 * correct_ans) + w, 776 + 11 + 9 + (24 * j)), 6, (0, 255, 0),
                           cv2.FILLED)
            elif grad == 0:
                color = (0, 0, 255)
                cv2.circle(img, (47 + 23 + 9 + (24 * user_ans_index) + w, 776 + 11 + 9 + (24 * j)), 6, color,
                           cv2.FILLED)
                cv2.circle(img, (47 + 23 + 9 + (24 * correct_ans) + w, 776 + 11 + 9 + (24 * j)), 6, (0, 255, 0),
                           cv2.FILLED)


    # img = cv2.resize(img, (800, 800))
    # cv2.imshow("imgContours", img)
    # cv2.waitKey(0)
    return img, grading_1, grading_2, gray_1_count, gray_2_count, user_choices_1, user_choices_2


def find_results(gradings, q_weights, no_of_questions):
    grading_1, grading_2 = gradings
    q1_weight, q2_weight = q_weights
    no_of_question_1, no_of_question_2 = no_of_questions
    totalScore = ((sum((grading_1 * q1_weight) + (grading_2 * q2_weight))) / ((no_of_question_1 * q1_weight) + (no_of_question_2 * q2_weight))) * 100
    return totalScore


def mark_grade(name, Grade, userchoices):
    with open('Grades.csv', 'a', newline='') as f:
        currtime = datetime.now()
        timestr = currtime.strftime('%x')

        row = [name] + [Grade] + [timestr] + userchoices
        writer = csv.writer(f)
        writer.writerow(row)


def get_ans():
    lines = []
    with open('Model Answers.csv', "r") as f1:
        csv_reader = csv.reader(f1, delimiter=',')
        for line in csv_reader:
            lines.append(line)
    return lines[-2:]
