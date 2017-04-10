# 문장 단위로 문장에 나온 단어를 추출하여 출력해주는 스크립트

from __future__ import division
from multiprocessing import Pool
from konlpy.tag import Kkma
import time
import os
import sys


def parse(file):
    result_list = []
    kkma = Kkma()                                       # Konlpy의 꼬꼬마 형태소 분석기 사용
    file = open(folder_name + '/' + file)               # 인자로 전달받은 파일 열기
    file_text = file.read()                             # 파일의 텍스트를 읽어옴
    sentences = kkma.sentences(file_text)               # 형태소 분석기로 텍스트 내의 문장을 리스트로 추출

    for sentence in sentences:                          # 개별 문장 단위로 작업
        sentense_list = []                              # 문장별 단어 저장할 리스트 생성

        morphemes = kkma.pos(sentence)                  # 문장 내의 형태소를 품사와 함께 추출 (단어, 품사)
        for word_set in morphemes:
            word = word_set[0]                          # 단어와 품사로 분리
            type = word_set[1]
            if type in tag_list:                        # 지정된 품사를 갖는 단어만 추출
                if word in word_list:                   # 지정된 단어만 추출
                    if type == 'VV' or type == 'VA':    # 동사인 경우 뒤에 '다'를 붙여줌
                        word += '다'
                    word = replace_list.get(word, word) # 특정 조건에 해당하는 단어의 경우 치환해줌
                    sentense_list.append(word)          # 단어를 문장별 리스트에 저장

        result_list.append(sentense_list)               # 결과값에 문장별 리스트들을 더해줌

    return result_list                                  # 결과값 반환


def combine_lists(lists):
    combined_list = []                                  # 결과를 저장할 리스트
    for list in lists:
        combined_list.extend(list)                      # 각 프로세스별 분산되어있던 리스트를 하나의 리스트로 통합

    return combined_list                                # 통합된 리스트를 반환

def make_log_result(results, len_file_list):            # 현재 진행상황을 터미널에 출력해주는 함수
    def log_result(retval):
        results.append(retval)
        sys.stdout.write(" " + str(round(len(results)/len_file_list*100, 2)) + '% \r')

    return log_result

def get_word_list(type):                                # 사용자가 선택한 단어 세트를 반환해주는 함수
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

def get_replace_list(type):                                 # 사용자가 선택한 단어 세트에 대한 단어 치환 리스트 반환
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
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']                # 출력할 품사를 지정
    word_set_list = ['total', 'top', 'low']                     # 사용할 단어 세트 이름을 지정

    word_set_type = input("어떤 단어 세트를 사용하시겠습니까? [total, top, low] : ")
    if word_set_type not in word_set_list:                      # 지정되지 않은 단어세트 예외 처리
        print("유효하지 않은 답변입니다.")
        exit()
    word_list = get_word_list(word_set_type)                    # 사용자가 지정한 단어 세트 로드
    replace_list = get_replace_list(word_set_type)              # 단어 세트에 해당하는 단어 대치 리스트 로드

    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")
    file_list = os.listdir(folder_name + '/')                   # 분석할 텍스트 파일이 있는 폴더 지정

    pools = Pool(3)                                             # 분석 프로세스를 진행할 코어의 갯수 지정
    results = []

    for file in file_list:
            pools.apply_async(                                  # 폴더 내 개별 파일에 대해 비동기로 작업 진행
            parse,                                              # 파싱 함수 사용
            args=[file],                                        # 인자로 개별 파일명을 넘겨줌
            callback=make_log_result(results, len(file_list))   # 콜백 메소드를 활용해 진행율을 표시해준다
        )
    pools.close()
    pools.join()

    word_lists = combine_lists(results)                         # 비동기 작업의 결과물을 원하는 형태로 재배치

    f = open(folder_name + "_lda_wordset", 'w')                 # 결과값을 저장할 파일을 지정
    for word_list in word_lists:
        for word in word_list:
            f.write(word + " ")                                 # 결과값을 기록
        f.write("\n")
    f.close()

    end_time = time.time()
    print("완료   출력파일 - " + folder_name + '_lda_wordset')
    print("걸린 시간" + str(end_time - start_time))
