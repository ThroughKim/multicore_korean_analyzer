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
    combined_list = []
    for list in lists:
        combined_list.extend(list)

    combined_list = [word.replace('안','알다') for word in combined_list]
    combined_list = [word.replace('점수','성적') for word in combined_list]
    combined_list = [word.replace('방법','방식') for word in combined_list]
    combined_list = [word.replace('열정적','열정') for word in combined_list]
    combined_list = [word.replace('교수','선생님') for word in combined_list]
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
    word_list = ["좋", "대하", "많", "없", "듣", "내용", "잘", "이해", "배우", "설명", "감사", "발표", "시험", "알", "도움", "과제", "어렵", "쉽", "토론", "문제", "통하", "공부", "준비", "힘들", "재미있", "가르치", "사람", "방식", "방법", "질문", "다양", "아쉽", "자료", "열심히", "평가", "지식", "흥미", "친절", "안", "아니", "재밌", "참여", "노력", "이야기", "인상깊", "필요", "개선", "이론", "성적", "점수", "유익", "말씀", "부족", "열정적", "열정", "부담", "능력", "의견", "피드백", "소통", "분위기", "관심", "실습", "기준", "즐겁", "진도", "출석", "항상", "선생님",  "교수", "못"]
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

    f = open(folder_name + "_output", 'w')
    for word in reversed(top_words):
        data = word[0] + " " + str(word[1])
        f.write(data + "\n")
    f.close

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
