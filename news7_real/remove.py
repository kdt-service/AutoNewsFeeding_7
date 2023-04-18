import os
if __name__ == '__main__':
# news_contents 폴더 안에 파일들 없애기
    filePath = '/home/ubuntu/news7/itnews/itnews/news_contents'
    if os.path.exists(filePath):
        if os.path.exists(filePath):
            for file in os.scandir(filePath):
                os.remove(file.path)
            print('Remove All Files')
        else:
            print("Directory Not Found") 

# sample1.csv 없애기
    samplePath = '/home/ubuntu/news7/itnews/sample1.csv'
    if os.path.exists(samplePath):
        os.remove(samplePath)
# metadata.tsv 없애기
    metaPath = '/home/ubuntu/news7/itnews/itnews/metadata.tsv'
    if os.path.exists(metaPath):
        os.remove(metaPath)


