## markdown 上传 minio 图床

通过正则表达式解析markdown，上传图片到图床并替换图片链接。

图片文件名替换为md5值，当检查到图床上有同名文件会跳过，防止重复上传。同时会给图片添加键为markdown文档名值为日期的tag。

除此之外还会替换latex公式格式：行间公式`$$xxx$$`替换为mathjax代码块；行内公式`$xxx$`外加上\`。

### 用法

+ 将markdown文档拖到drag.cmd上，处理成功后会将内容保存至剪切板；
+ 或是运行generateReg.py生成注册表文件，运行注册表文件添加程序到右键菜单。然后对markdown文档右键选择`markdown image uploader`即可。处理成功后会将内容保存至剪切板。