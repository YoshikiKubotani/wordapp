import random

def make_random_test(all_items, num_question):
    len_data = len(all_items)
    test_set_list = []
    for i in range(num_question):
        item_id_list = random.sample(range(len_data), k=5)
        question_dict = {}
        for idx, item_id in enumerate(item_id_list):
            if idx == 0:
                question_dict["question_en"] = all_items[item_id].english
                question_dict["answer_jp"] = all_items[item_id].japanese
            else:
                question_dict["option_{}".format(idx)] = all_items[item_id].japanese
        test_set_list.append(question_dict)
    return test_set_list