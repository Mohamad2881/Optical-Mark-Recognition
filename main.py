from utlis import *


img_path = "imgs/t1.jpg"

# img_coords --> [q_x, q_y, q_w, q_h]
q1_coords = [47, 370, 700, 376]  # Qusetion 1
q2_coords = [47, 776, 658, 88]  # Qusetion 2

# get the Model answer
ans = get_ans()
# print(ans)

# Convert String to integer
ans_1 = [*map(int, ans[0])]
ans_2 = [*map(int, ans[1])]

q1_labels = ['A', 'B', 'C', 'D']

threshold_1 = 150

q2_labels = ['T', 'F']

threshold_2 = 150

# quest_specs --> [no_of_blocks, no_of_block_quest, no_of_choices, labels, ans1]
q1_specs = [6, 15, 4, q1_labels, ans_1]
q2_specs = [10, 3, 2, q2_labels, ans_2]

img_coords = [q1_coords, q2_coords]
quest_specs = [q1_specs, q2_specs]
threshold = [threshold_1, threshold_2]

q1_weight = 1
q2_weight = 1
img, grading_1, grading_2, gray_1_count, gray_2_count, user_choices_1, user_choices_2 = evaluate_1(img_path, img_coords,
                                                                                                   quest_specs,
                                                                                                   threshold)

gradings = [grading_1, grading_2]
q_weights = [q1_weight, q2_weight]
no_of_question_1 = q1_specs[0] * q1_specs[1]
no_of_question_2 = q2_specs[0] * q2_specs[1]

no_of_questions = [no_of_question_1, no_of_question_2]
result = find_results(gradings, q_weights, no_of_questions)
result = round(result, 2)
print("Total score", result)
correct_1 = grading_1.count(1)
correct_2 = grading_2.count(1)

print("Q1 correct Answers", correct_1)
print("Q1 Wrong Answers", no_of_question_1 - (correct_1 + gray_1_count))
print("Q1 Gray Answers", gray_1_count)

print("Q2 correct Answers", correct_2)
print("Q2 Wrong Answers", no_of_question_2 - (correct_2 + gray_2_count))
print("Q2 Gray Answers", gray_2_count)

student_id = 2

# Save Student Grade into csv
mark_grade(student_id, result, user_choices_1 + user_choices_2)


cv2.putText(img, f'Grade: {result}%', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)

# grading, correct ..,
img = cv2.resize(img, (800, 800))
cv2.imshow("image", img)
cv2.waitKey(0)
