# coding=utf-8
import minioUploader
import re
import os

pattern = re.compile(r'(!\[.*\]\((.*?)( +"(.*?)")?\))')

def replaceImagePath(current_path, content, client, label):
    imagePaths = pattern.findall(content)
    print(imagePaths)
    for imagePath in imagePaths:
        markdownCode = imagePath[0]
        newMarkdownCode = markdownCode
        imageUrl = imagePath[1].strip()
        description = imagePath[3]
        if imageUrl.startswith(("https", "http")):
            pass
        elif os.path.isfile(os.path.join(current_path, imageUrl)):
            url = minioUploader.uploadImage(client, os.path.join(current_path, imageUrl), label)
            if url is not None:
                newMarkdownCode = newMarkdownCode.replace(imageUrl, url)
            else:
                print("upload error.\n")
                continue
        else:
            print("unknown url: {}".format(imageUrl))
            continue
        if len(description) > 0:
            newMarkdownCode = '%' + newMarkdownCode[1:]
        print("{} -> {}".format(markdownCode, newMarkdownCode))
        content = content.replace(markdownCode, newMarkdownCode)
    return content