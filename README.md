# 用 PYTHON 写的端口扫描程序
## 使用方法
```
Usage:
  python portScanner.py <host>
For Example:
  python portScanner.py www.baidu.com
```

## 示例
```
D:\code\python\port_scan>python portScanner.py www.baidu.com

正在获取主机[www.baidu.com]的IP……
主机[www.baidu.com]的IP是：14.215.177.38
开始扫描[14.215.177.38]的端口……
最大线程数：2000，活动线程数：4，端口数：65534，已扫描端口数：65533，已扫描端口量百分比：100.0%
端口开放情况:
80: OPEN
443: OPEN
扫描结束，用时：34.145004 秒

```

### 环境
```
python3
```

### 参考
* https://www.jianshu.com/p/b1994a370660