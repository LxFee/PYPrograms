## markdown 图片下载及格式化

使用正则表达式获取markdown文档中所有图片的url地址，下载到文档同目录的assets文件夹中，并修改markdown文档中的图片路径为本地路径

### 用法

```sh
python ./main.py [input path]  [output path] [--help] [--debug]
```

+ `input path`：markdown文档所在的文件夹，会遍历所有文件和子文件夹，对每个markdown文档进行处理
+ `output path`：输出目录，程序会将处理完成后的markdown文档和下载的图片复制到output文件夹中；对于其余不相干文件则会直接复制过来。不会对原文件有任何修改操作
+ `--debug`：debug模式，将打印遍历过程

### 注意事项

所指定的output path文件夹必须**不存在**，程序会会自己建立文件夹