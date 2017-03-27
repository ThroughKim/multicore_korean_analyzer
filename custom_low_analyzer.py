from __future__ import division
import time, os,  operator
from multiprocessing import Pool
from konlpy.tag import Kkma
from collections import Counter
import sys


def parse(file):
    result_list = []
    kkma = Kkma()
    file = open(folder_name + '/' + file)
    file_text = file.read()
    sentences = kkma.sentences(file_text)

    for sentence in sentences:
        morphemes = kkma.pos(sentence)
        for word_set in morphemes:
            word = word_set[0]
            type = word_set[1]
            if type in tag_list:
                if word in word_list:

                    if type == 'VV' or type == 'VA':
                        word += '다'
                    result_list.append(word)

    return result_list


def combine_lists(lists):
    replace_list = dict(
        별로='전혀',
        늦다='지각'
    )
    combined_list = []
    for list in lists:
        combined_list.extend(list)

    combined_list = [str(replace_list.get(word, word)) for word in combined_list]

    return combined_list

def make_log_result(results, len_file_list):
    def log_result(retval):
        results.append(retval)
        sys.stdout.write(" " + str(round(len(results)/len_file_list*100, 2)) + '% \r')

    return log_result

if __name__ == "__main__":
    start_time = time.time()
    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")
    word_count = 100
    word_list = ['휴강', '전혀', '별로', '지각', '늦', '못', '수준', '공지', '범위', '출석']
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']
    file_list = os.listdir(folder_name + '/')

    pools = Pool(3)
    results = []

    for file in file_list:
        pools.apply_async(parse, args=[file], callback=make_log_result(results, len(file_list)))
    pools.close()
    pools.join()

    word_list = combine_lists(results)

    top_words = sorted(dict(Counter(word_list).most_common(word_count)).items(), key=operator.itemgetter(1))

    f = open(folder_name + "_lowword_output", 'w')
    for word in reversed(top_words):
        data = word[0] + " " + str(word[1])
        f.write(data + "\n")
    f.close

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
