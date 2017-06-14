# Thrive-voice 鲜声

**Under MIT License**

## 简单介绍

这是一个有趣的 VoIP 客户端。

作为计算机网络TCP与UDP合理使用的练习。

同时也是一个采用Actor模型（参与者模式）练习并发编程的良好实践。

我的心路历程记录在[这篇博客](http://blog.thrimbda.com/2017/05/18/%E4%BA%8C%E6%8E%A2%E5%B9%B6%E5%8F%91/)里。

**希望各位不吝赐教**。

## 安装

首先要做的是把这个仓库clone下来：

```bash
$ git clone https://github.com/Thrimbda/Thrive-voice.git
```

在确保你使用的是python3后安装依赖（这个操作可能需要管理员权限，所以我推荐你使用虚拟环境virtualenv）：

```bash
$ pip install -r requirements.txt
```

然后开始运行~

```bash
$ python -m src.thervice mainThread
```

就OK了。

## 使用说明

~~我没做GUI，因为我是前端渣。~~

由于没有前端，我也不想开两个进程，所以一切操作都由按键中断（Ctrl+C）作为起始：

程序运行后处于监听状态。这时候如果别人打电话进来你会收到提示。

```
  Incoming telegram, accept or deny?
```

如果你想给别人打电话或者退出的话，触发键盘中断后会收到提示，按照操作一步一步来就好了

```
  Do you wanna dial someone or exit?
$ dial
  to whom you want to call?
  please input the host name.
$ xxx.xxx.xxx.xxx
```

你可能看出来了，目前为止这玩意最大的问题除了[Issue #1](https://github.com/Thrimbda/Thrive-voice/issues/1)里面那个Bug以外就是...

**还不支持NAT穿透，打电话的双方必须在同一个局域网内或者其中一方拥有公网IP（多么奢侈！）**

我已经计划把与服务端相连纳入日程了，先凑合和好朋友在同一局域网下玩玩。
