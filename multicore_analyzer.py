# 멀티 프로세싱을 이용해 다수의 텍스트 파일에서 정해진 품사로 된 단어를 추출하여
# 가장 자주 등장하는 n개의 단어를 추출함

from __future__ import division
import time, os,  operator
from multiprocessing import Pool
from konlpy.tag import Kkma
from collections import Counter
import sys

# 파싱함수 - 문장에서 정해진 품사 단어를 추출함
def parse(file):
    result_list = []
    kkma = Kkma()                               # Konlpy의 꼬꼬마 형태소 분석기 사용
    file = open(folder_name + '/' + file)       # 인자로 받은 파일명의 파일 열기
    file_text = file.read()                     # 파일 내 텍스트 읽어옴
    sentences = kkma.sentences(file_text)       # 형태소 분석기로 문장을 리스트로 추출

    for sentence in sentences:                  # 개별 문장별로 작업
        morphemes = kkma.pos(sentence)          # 문장내에서 형태소를 품사와 함께 추출 ('단어', '품사')
        for word_set in morphemes:
            word = word_set[0]                  # 단어와 품사로 분리
            type = word_set[1]
            if type in tag_list:                # 단어의 품사가 지정되어있는 경우
                if word not in exception_list:  # 단어가 예외 목록에 속하지 않는 경우
                    if type == 'VV' or type == 'VA':
                        word += '다'             # 동사인 경우 '다'를 붙여줌
                    result_list.append(word)    # 결과 리스트에 단어를 넣는다.

    return result_list                          # 결과 리스트 반환

# 코어별로 추출한 단어의 리스트를 원하는 형태로 재배치하는 함수
def combine_lists(lists):
    combined_list = []                          # 결과 저장 리스트
    for list in lists:
        combined_list.extend(list)              # 리스트 안의 리스트를 하나의 리스트로 합쳐줌

    return combined_list                        # 합쳐진 단일 리스트 반환

# 현재 진행상황을 터미널에 출력해주는 함수
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

    word_count = 200                                # 몇 개의 단어를 추출할 것인지 설정
    exception_list = ["교수님", "수업", "학생", "강의", "학기", "점", "때", "시간", "중간", "기말", "고사", "생각", "시간", "동안","있","하","같","되"]
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']    # 어떤 품사의 단어를 추출할 것인지 설정
    file_list = os.listdir(folder_name + '/')       # 입력받은 폴더 내의 파일들을 리스트로 읽어옴

    pools = Pool(7)                                 # 몇 개의 코어에서 멀티 프로세싱을 할 것인지 설정
    results = []                                    # 결과 값을 저장할 리스트

    for file in file_list:                          # 각각에 파일에 대해 작업진행
        pools.apply_async(                          # 개별 코어에 비동기로 작업을 할당
            parse,                                  # 파싱 함수 실행
            args=[file],                            # 인자로 파일명 전달
            callback=make_log_result(results, len(file_list))   # 콜백함수를 이용해 진행률 표시
        )
    pools.close()
    pools.join()

    word_list = combine_lists(results)              # 받아온 결과 리스트를 원하는 형태로 재배치

    top_words = sorted(                             # 단어를 빈도순으로 정렬하여 상위 n개로 줄이고, 출현횟수를 적어줌
        dict(Counter(word_list).most_common(word_count)).items(),
        key=operator.itemgetter(1)
    )

    f = open(folder_name + "_output", 'w')          # 결과값을 저장할 파일을 생성
    for word in reversed(top_words):                # 결과값을 내림차순으로 정렬하여 파일에 기록
        data = word[0] + " " + str(word[1])
        f.write(data + "\n")
    f.close

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
