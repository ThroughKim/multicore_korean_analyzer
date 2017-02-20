# 멀티코어 한글 텍스트 분석기

> Python3.5와 JDK가 설치된 리눅스 혹은 맥에서 작동합니다.

한글로 이루어진 텍스트파일에서 특정 품사인 단어 출현갯수를 카운트하는 프로그램입니다.  
대용량 텍스트를 보다 원활히 분석할 수 있도록 멀티코어를 활용하도록 구성했습니다.  
분석할 파일을 원하는 폴더에 집어넣고

```bash
$ split -l 100 file_name
```

위 명령어를 사용해 잘게 나누어주면 각 코어에서 단위파일들을 가져가 분석을 한 뒤 합쳐줍니다.

파일을 실행하고, 분석하고자 하는 텍스트파일들이 들어있는 폴더의 이름을 입력하면 폴더 내 모든 파일을 불러와 분석합니다.
```bash
$ python multicore_analyzer.py
...
폴더이름을 입력하세요: your_folder_name
```
