import datetime
import os
import zipfile

def main(config):
    dtNow = datetime.datetime.now()
    nowTime = dtNow.strftime('%Y-%m-%d_%H-%M-%S')
    print("バックアップを開始します...")
    print(nowTime)

    if os.path.exists(config['distPath']):
        oldFileFelete(config['distPath'], config['limit'])
        zipArchive(config['targetPaths'], config['distPath'], nowTime)
    else:
        os.mkdir(config['distPath'])
        zipArchive(config['targetPaths'], config['distPath'], nowTime)
    
    print("バックアップが完了しました！")

def zipArchive(srcPathList, distPath, nowTime):#zipで保存
    print("now archiveing...")
    nowSrcPathPath = ''
    try:
        with zipfile.ZipFile(os.path.join(distPath, nowTime+'.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for srcPath in srcPathList:
                print(f"srcPath > {srcPath}")
                nowSrcPathPath = srcPath
                if os.path.isfile(srcPath): # file archive
                    zipf.write(srcPath, os.path.basename(srcPath))
                elif os.path.isdir(srcPath): # folder archive
                    srcPathName = os.path.basename(srcPath)
                    for root, dirs, files in os.walk(srcPath):
                        for file in files:
                            filePath = os.path.join(root, file)
                            # arcName = os.path.relpath(file_path, srcPath)
                            arcName = os.path.join(srcPathName, os.path.basename(filePath))
                            print(f"add file > {arcName}")
                            zipf.write(filePath, arcName)
                else:
                    print("指定されたファイルまたはフォルダが存在しません")
    except Exception as e:
        print(f"ZIP圧縮中にエラーが発生しました: ERROR Path > {nowSrcPathPath}\n\n{str(e)}")

    print("complete!\n")

def oldFileFelete(distPath, limit):
    fileList = []
    count = 0
    for file in os.listdir(distPath):
        count += 1
        fileList.append([os.path.join(distPath, file), os.path.getctime(os.path.join(distPath, file))])
        if count >= limit:
            print(f"バックアップ上限により {min(fileList)[0]} が消去されます")
            os.remove(min(fileList)[0])

def getSizeDir(path):
    totalSize = 0
    for dirPath in os.listdir(path):
        fullPath = os.path.join(path, dirPath)
        if os.path.isfile(fullPath):
            totalSize += os.path.getsize(fullPath)
        elif os.path.isdir(fullPath):
            totalSize += getSizeDir(fullPath)
    return totalSize