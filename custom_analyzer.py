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
    replace_list = get_replace_list()

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

def get_word_list():
    word_list = [
        '많', '많이', '없', '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사', '기말고사', '고사',
        '도움', '과제', '어렵', '부담', '쉽', '토론', '문제', '통하', '소통', '대화', '준비', '재미있', '재밌', '흥미', '즐겁', '사람',
        '학생', '질문', '아쉽', '열심히', '노력', '열정적', '열정', '평가', '지식', '친절', '관심', '배려', '이야기', '인상깊', '인상',
        '성적', '점수', '유익', '능력', '실력', '피드백', '선생님', '교수', '교수님', '수업', '강의'
    ]

    return word_list

def get_tag_list():
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']

    return tag_list

def get_replace_list():
    replace_list = dict(
        많이='많다',
        알다='배우다',
        중간='시험',
        기말='시험',
        중간고사='시험',
        기말고사='시험',
        고사='시험',
        부담='어렵다',
        소통='통하다',
        대화='통하다',
        흥미='재미있다',
        재밌다='재미있다',
        즐겁다='재미있다',
        노력='열심히',
        열정적='열심히',
        열정='열심히',
        관심='친절',
        배려='친절',
        인상='인상깊다',
        점수='성적',
        실력='능력',
        교수='선생님',
        교수님='선생님',
        강의='수업',
        학생='사람',
        알='배우다',
        배우='배우다'
    )

    return replace_list

if __name__ == "__main__":
    start_time = time.time()
    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")

    word_count = 100

    file_list = os.listdir(folder_name + '/')
    word_list = get_word_list()
    tag_list = get_tag_list()

    pools = Pool(3)
    results = []

    for file in file_list:
        pools.apply_async(parse, args=[file], callback=make_log_result(results, len(file_list)))
    pools.close()
    pools.join()

    word_list = combine_lists(results)

    top_words = sorted(dict(Counter(word_list).most_common(word_count)).items(), key=operator.itemgetter(1))

    f = open(folder_name + "_output", 'w')
    for word in reversed(top_words):
        data = word[0] + " " + str(word[1])
        f.write(data + "\n")
    f.close

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
