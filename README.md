# 用 PYTHON 写的端口扫描程序
## 1 使用方法
```
git clone https://github.com/jinghang/port_scan.git
cd port_scan
python portScanner.py github.com
```
### 1.1 命令说明
```
Usage:
  python portScanner.py <host> [option]
option:
  -t: 连接超时时间，单位是秒，默认是1秒，
  -p: 要扫秒的端口好，多个用逗号给开，不指定将扫描所有端口，
For Example:
  python portScanner.py www.baidu.com
  python portScanner.py www.baidu.com -t 3 -p 80,443
```
* 如果没有扫描到端口，可以用参数 -t 来增长连接的超时时间，比如 -t 3 或者 -t 5

### 1.2 示例
```
> python portScanner.py www.baidu.com

正在获取主机[www.baidu.com]的IP……
主机[www.baidu.com]的IP是：14.215.177.38
开始扫描[14.215.177.38]的端口……
最大线程数：2000，活动线程数：4，端口数：65534，已扫描端口数：65533，已扫描端口量百分比：100.0%
端口开放情况:
80: OPEN
443: OPEN
扫描结束，用时：34.145004 秒
```

## 2 查看文档
```
python -m pydoc portScanner
```

## 3 生成HTML文档
```
python -m pydoc -w portScanner
```


## 4 环境
```
python3
```

