import random

# 玩家列表
players = ["玩家1", "玩家2", "玩家3", "玩家4", "玩家5", "玩家6", "玩家7", "玩家8"]

# 随机打乱玩家顺序
random.shuffle(players)

# 将玩家分为四组
group1 = players[:2]  # 前两个玩家
group2 = players[2:4]  # 接下来两个玩家
group3 = players[4:6]  # 再接下来两个玩家
group4 = players[6:8]  # 最后两个玩家

# 打印分组结果
print("第一组:", group1)
print("第二组:", group2)
print("第三组:", group3)
print("第四组:", group4)
