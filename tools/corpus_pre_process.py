# coding=utf-8
import csv
import random
import re

TIME_PATTERN = '(:?\[\d{2}:\d{2}\])|(:?\[HH:MM\])'
RANG_PATTERN = '\(([\d(:?+∞)]+),([\d(:?+∞)]+)\)'
COLOR_PATTERN = '\(c\)'
ENUM_PATTERN = ''
P_INF = 65535
N_INF = 65535
COLORS = (
    '黑色', '昏灰', '灰色', '暗灰', '银色', '亮灰色', '庚斯博罗灰', '白烟色', '白色', '雪色', '铁灰色', '沙棕', '玫瑰褐', '亮珊瑚色', '印度红', '褐色',
    '耐火砖红', '栗色', '暗红', '鲜红', '红色', '柿子橙', '雾玫瑰色', '鲑红', '腥红', '蕃茄红', '暗鲑红', '珊瑚红', '橙红', '亮鲑红', '朱红', '赭黄',
    '热带橙', '驼色', '杏黄', '椰褐', '海贝色', '鞍褐', '巧克力色', '燃橙', '阳橙', '粉扑桃色', '沙褐', '铜色', '亚麻色', '蜜橙', '秘鲁色',
    '乌贼墨色', '赭色', '陶坯黄', '橘色', '暗橙', '古董白', '日晒色', '硬木色', '杏仁白', '那瓦霍白', '万寿菊黄', '蕃木瓜色', '灰土色', '卡其色',
    '鹿皮鞋色', '旧蕾丝色', '小麦色', '桃色', '橙色', '花卉白', '金菊色', '暗金菊色', '咖啡色', '茉莉黄', '琥珀色', '玉米丝色', '铬黄', '金色', '柠檬绸色',
    '亮卡其色', '灰金菊色', '暗卡其色', '含羞草黄', '奶油色', '象牙色', '米黄色', '亮黄', '亮金菊黄', '香槟黄', '芥末黄', '月黄', '橄榄色', '鲜黄', '黄色',
    '苔藓绿', '亮柠檬绿', '橄榄军服绿', '黄绿', '暗橄榄绿', '苹果绿', '绿黄', '草绿', '草坪绿', '查特酒绿', '叶绿', '嫩绿', '明绿', '钴绿', '蜜瓜绿',
    '暗海绿', '亮绿', '灰绿', '常春藤绿', '森林绿', '柠檬绿', '暗绿', '绿色', '鲜绿色', '孔雀石绿', '薄荷绿', '青瓷绿', '碧绿', '绿松石绿', '铬绿',
    '苍色', '海绿', '中海绿', '薄荷奶油色', '春绿', '孔雀绿', '中春绿色', '中碧蓝色', '碧蓝色', '青蓝', '水蓝', '土耳其蓝', '绿松石色', '亮海绿',
    '中绿松石色', '亮青', '浅蓝', '灰绿松石色', '暗岩灰', '凫绿', '暗青', '青色', '水色', '暗绿松石色', '军服蓝', '孔雀蓝', '婴儿粉蓝', '浓蓝', '亮蓝',
    '灰蓝', '萨克斯蓝', '深天蓝', '天蓝', '亮天蓝', '水手蓝', '普鲁士蓝', '钢青色', '爱丽丝蓝', '岩灰', '亮岩灰', '道奇蓝', '矿蓝', '湛蓝', '韦奇伍德瓷蓝',
    '亮钢蓝', '钴蓝', '灰丁宁蓝', '矢车菊蓝', '鼠尾草蓝', '暗婴儿粉蓝', '蓝宝石色', '国际奇连蓝', '蔚蓝', '品蓝', '暗矿蓝', '极浓海蓝', '天青石蓝', '幽灵白',
    '薰衣草紫', '长春花色', '午夜蓝', '藏青', '暗蓝', '中蓝', '蓝色', '紫藤色', '暗岩蓝', '岩蓝', '中岩蓝', '木槿紫', '紫丁香色', '中紫红', '紫水晶色',
    '浅灰紫红', '缬草紫', '矿紫', '蓝紫', '紫罗兰色', '靛色', '暗兰紫', '暗紫', '三色堇紫', '锦葵紫', '优品紫红', '中兰紫', '淡紫丁香色', '蓟紫',
    '铁线莲紫', '梅红色', '亮紫', '紫色', '暗洋红', '洋红', '品红', '兰紫', '浅珍珠红', '陈玫红', '浅玫瑰红', '中青紫红', '洋玫瑰红', '玫瑰红', '红宝石色',
    '山茶红', '深粉红', '火鹤红', '浅珊瑚红', '暖粉红', '勃艮第酒红', '尖晶石红', '胭脂红', '浅粉红', '枢机红', '薰衣草紫红', '灰紫红', '樱桃红', '浅鲑红',
    '绯红', '粉红', '亮粉红', '壳黄红', '茜红')

if __name__ == '__main__':
    nh = '小黑'
    out_file = open('../data/corpus_process.txt', 'wr')
    with open('../data/corpus_source_zh.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        reader.next()
        for row in reader:
            for text in row[3:]:
                if text != '':
                    m = re.search(TIME_PATTERN, text)
                    if m:
                        for h in range(0, 23):
                            for i in range(0, 59):
                                t = '%02d:%02d' % (h, i)
                                r = re.sub(TIME_PATTERN, t, text)
                                out_file.write(nh + r + '\n')
                    else:
                        m = re.search(RANG_PATTERN, text)
                        if m:
                            start, end = m.group(1), m.group(2)
                            start = P_INF if start == '+∞' else N_INF if start == '-∞' else int(start)
                            end = P_INF if end == '+∞' else N_INF if end == '-∞' else int(end)
                            for i in range(start, end, random.randint(1, 1000 if (
                                            start == P_INF or start == N_INF or end == P_INF or end == N_INF) else 1)):
                                t = '%d' % i
                                r = re.sub(RANG_PATTERN, t, text)
                                out_file.write(nh + r + '\n')
                        else:
                            m = re.search(COLOR_PATTERN, text)
                            if m:
                                for c in COLORS:
                                    r = re.sub(COLOR_PATTERN, c, text)
                                    out_file.write(nh + r + '\n')
                            else:
                                out_file.write(nh + text + '\n')
