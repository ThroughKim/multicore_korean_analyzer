from __future__ import division
import time, os
from multiprocessing import Pool
from konlpy.tag import Kkma
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
    replace_list = get_replace_list(word_set_type)
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

def get_word_list(type):
    word_list = []

    if type == "total":
        word_list = [
            '많', '많이', '없', '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사', '기말고사', '고사',
            '도움', '과제', '어렵', '부담', '쉽', '토론', '문제', '통하', '소통', '대화', '준비', '재미있', '재밌', '흥미', '즐겁', '사람',
            '학생', '질문', '아쉽', '열심히', '노력', '열정적', '열정', '평가', '지식', '친절', '관심', '배려', '이야기', '인상깊', '인상',
            '성적', '점수', '유익', '능력', '실력', '피드백', '선생님', '교수', '교수님', '수업', '강의'
        ]
    elif type =="top":
        word_list = [
            '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사',
            '기말고사', '고사', '도움', '과제', '쉽', '토론', '통하', '소통', '대화', '준비', '재미있',
            '재밌', '흥미', '즐겁', '사람', '학생', '질문', '열심히', '노력', '열정적', '열정', '평가', '친절', '관심',
            '배려', '이야기', '인상깊', '인상', '성적', '점수', '능력', '실력', '피드백', '선생님', '교수', '교수님', '수업', '강의',
            '최고', '완벽', '잘하', '기억', '사랑', '이름', '어렵', '부담', '만족'
        ]
    elif type == "low":
        word_list = [
            '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사',
            '기말고사', '고사', '도움', '과제', '어렵', '부담', '쉽', '토론', '통하', '소통', '대화', '준비',
            '사람', '학생', '질문', '평가', '이야기', '인상깊', '인상', '성적', '점수', '능력', '실력', '피드백',
            '선생님', '교수', '교수님', '수업', '강의', '휴강', '전혀', '별로', '지각', '늦', '못', '공지', '출석',
            '재미있', '재밌', '흥미', '즐겁', '열심히', '노력', '열정적', '열정', '친절', '관심', '배려',
        ]
    else:
        print("error")
        exit()

    return word_list

def get_replace_list(type):
    replace_list = []

    if type == "total":
        replace_list = dict(
            많이='많다',
            알다='배움',
            알='배움',
            배우='배움',
            배우다='배움',
            중간='시험',
            기말='시험',
            중간고사='시험',
            기말고사='시험',
            고사='시험',
            부담='어렵다',
            통하다='소통',
            대화='소통',
            인상='인상깊다',
            점수='성적',
            실력='능력',
            선생님='교수',
            교수님='교수',
            강의='수업',
            사람='학생',
            재미있다='재미',
            흥미='재미',
            재밌다='재미',
            즐겁다='재미',
            열심히='열정',
            노력='열정',
            열정적='열정',
            관심='친절',
            배려='친절',
        )
    elif type == "top":
        replace_list = dict(
            알다='배움',
            알='배움',
            배우='배움',
            배우다='배움',
            중간='시험',
            기말='시험',
            중간고사='시험',
            기말고사='시험',
            고사='시험',
            통하다='소통',
            대화='소통',
            재미있다='재미',
            흥미='재미',
            재밌다='재미',
            즐겁다='재미',
            열심히='열정',
            노력='열정',
            열정적='열정',
            선생님='교수',
            교수님='교수',
            강의='수업',
            사람='학생',
            부담='어렵다',
            완벽='최고',
            관심='친절',
            배려='친절',
            인상='인상깊다',
            점수='성적',
            실력='능력',
        )
    elif type == "low":
        replace_list = dict(
            알다='배움',
            알='배움',
            배우='배움',
            배우다='배움',
            중간='시험',
            기말='시험',
            중간고사='시험',
            기말고사='시험',
            고사='시험',
            부담='어렵다',
            통하다='소통',
            대화='소통',
            인상='인상깊다',
            점수='성적',
            실력='능력',
            선생님='교수',
            교수님='교수',
            강의='수업',
            사람='학생',
            전혀='별로',
            못='못하다',
            재미있다='재미',
            흥미='재미',
            재밌다='재미',
            즐겁다='재미',
            열심히='열정',
            노력='열정',
            열정적='열정',
            관심='친절',
            배려='친절',
        )
    else:
        print("error")
        exit()

    return replace_list

if __name__ == "__main__":
    start_time = time.time()

    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']
    word_set_list = ['total', 'top', 'low']

    word_set_type = input("어떤 단어 세트를 사용하시겠습니까? [total, top, low] : ")
    if word_set_type not in word_set_list:
        print("유효하지 않은 답변입니다.")
        exit()
    word_list = get_word_list(word_set_type)

    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")
    file_list = os.listdir(folder_name + '/')

    pools = Pool(3)
    results = []

    for file in file_list:
        pools.apply_async(parse, args=[file], callback=make_log_result(results, len(file_list)))
    pools.close()
    pools.join()

    word_list = combine_lists(results)

    f = open(folder_name + "_output", 'w')
    for word in word_list:
        f.write(word + "\n")
    f.close

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
