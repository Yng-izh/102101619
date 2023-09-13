import jieba
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# 设置词云图图片轮廓
picture = Image.open("backgroung-img.png")
shape = np.array(picture)
image_colors = ImageColorGenerator(shape)
# 打开.txt文档，对内容进行分词处理
with open("弹幕统计.txt", 'r', encoding='utf-8') as page:
    text = page.read()
cut_text = " ".join(jieba.cut(text))
ciyun_words = ''
# 设置停用词
stopwords = set()
content = [line.strip() for line in open('stopwords.txt', 'r').readlines()]
stopwords.update(content)
# 将分割好的词加入数组中等待使用
for word in cut_text:
    if word not in stopwords:
        ciyun_words += word
# 设置词云图参数
cloud = WordCloud(
    mask=shape,  # 图片背景
    font_path="simkai.ttf",  # 字体大小
    background_color="white",  # 背景颜色
    width=800,  # size
    height=600,
    max_words=2000,
).generate(ciyun_words)
plt.figure(figsize=[10, 10])
plt.imshow(cloud.recolor(color_func=image_colors))  # 终端打开图片
plt.axis('off')
plt.savefig('barrage.png')  # 保持图片
