## 代码统计

### 用法

```sh
python ./cc.py [path] [--debug] [--dir-filter ...] [--ext-filter ...]
```

+ `path`：工作目录，不指定则为当前目录
+ `--debug`：debug模式，将打印遍历过程
+ `--dir-filter`：需要遍历的子文件夹，不指定则直接遍历整个工作目录。用空格隔开
+ `--ext-filter`：后缀名过滤，不指定则为`.h`、`.c`、`.cpp`

### 例子
```sh
python ./cc.py ./project --debug --dir-filter src/App1 src/App2 --ext-filter .h .c .py
```
将会统计`./project/src/App1`、`./project/src/App2`下所有`.h`、`.c`和`.py`后缀的文件。