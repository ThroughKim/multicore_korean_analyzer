import time, os,  operator
from multiprocessing import Pool
from konlpy.tag import Kkma
from collections import Counter


def parse(file):
    print("processing file: " + file)
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
                if word not in exception_list:
                    if type == 'VV' or type == 'VA':
                        word += "다"
                    result_list.append(word)

    return result_list

def combine_lists(lists):
    combined_list = []
    for list in lists:
        combined_list.extend(list)

    return combined_list

if __name__ == "__main__":
    start_time = time.time()
    print("분석할 폴더의 이름을 입력하세요.")
    print("현재 파일에 대한 상대경로만 입력하면 되며, 끝에 '/'는 생략해주세요.")
    folder_name = input("폴더이름을 입력하세요:  ")
    word_count = 50
    file_count = 0
    exception_list = ["교수님", "수업", "있", "학생", "강의", "하", "학기", "점", "같", "되", "때"]
    tag_list = ['NNG', 'NNP', 'VV', 'VA', 'MAG']
    file_list = os.listdir(folder_name + '/')

    pools = Pool(3)
    results = pools.map(parse, file_list)
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
    print("완료")
    print("걸린 시간" + str(end_time - start_time))
