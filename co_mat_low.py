from __future__ import division
import time, os,  operator
from multiprocessing import Pool
import codecs
import networkx as nx
import sys
import time
from konlpy.tag import Kkma


def parse(file):
    result_list = []
    kkma = Kkma()

    text_file = codecs.open(folder_name + '/' + file, 'r', encoding='utf8')
    file_sentence_list = text_file.readlines()

    for sentence in file_sentence_list:
        sentence_word_list = []

        morphemes = kkma.pos(sentence)
        for word_set in morphemes:
            word = word_set[0]
            type = word_set[1]

            if type in tag_list:
                if word in word_list:
                    if type == 'VV' or type == 'VA':
                        word += '다'
                    word = replace_list.get(word, word)
                    sentence_word_list.append(word)

        result_list.append(sentence_word_list)

    return result_list

def make_log_result(results, len_file_list):
    def log_result(retval):
        results.append(retval)
        sys.stdout.write(" " + str(round(len(results)/len_file_list*100, 2)) + '% \r')

    return log_result

def make_graphml(lists):
    res = {}

    combined_list = []
    for list in lists:
        combined_list.extend(list)

    for sentence_list in combined_list:
        for word1 in sentence_list:
            for word2 in sentence_list:
                key = (word1, word2)
                res[key] = res.get(key, 0) + 1

    res = {k: v for k, v in res.items() if v > 5}
    G = nx.Graph()
    for item in res:
        G.add_edge(item[0], item[1], weight=res[item])

    return G


if __name__ == "__main__":

    start_time = time.time()
    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")

    word_list = [
        '많', '많이', '없', '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사', '기말고사', '고사', '도움', '과제',
        '어렵', '부담', '쉽', '토론', '문제', '통하', '소통', '대화', '준비', '재미있', '재밌', '흥미', '즐겁', '사람', '학생', '질문', '아쉽', '열심히',
        '노력', '열정적', '열정', '평가', '지식', '친절', '관심', '배려', '이야기', '인상깊', '인상', '성적', '점수', '유익', '능력', '실력', '피드백', '선생님',
        '교수', '교수님', '수업', '강의', '휴강', '전혀', '별로', '지각', '늦', '못', '수준', '공지', '범위', '출석'
    ]
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']
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
        별로='전혀',
        늦다='지각',
        베우='배우다',
    )
    file_list = os.listdir(folder_name + '/')

    pools = Pool(3)
    results = []

    for file in file_list:
        pools.apply_async(parse, args=[file], callback=make_log_result(results, len(file_list)))
    pools.close()
    pools.join()

    graph = make_graphml(results)
    nx.write_graphml(graph, './low.graphml')

    end_time = time.time()
    print("완료   ")
    print("걸린 시간" + str(end_time - start_time))
