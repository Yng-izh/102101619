import pandas
# 该部分用于将xls文档转成txt文档方便词云图生成


def Excel_to_Txt(input_path, output_path):  # 将xlx文档转化为txt并生成.txt文件
    df = pandas.read_excel(input_path, header=None)
    print('开始写入txt文件')
    df.to_csv(output_path, header=None, sep=',', index=False)
    print('写入成功')


def creat_txt(input_path):  # 创建txt文件名
    length = len(input_path)
    output_path = ''
    for i in range(length-1, -1, -1):
        if input_path[i] == '.':
            break
    for j in range(0, i+1):
        output_path = output_path + input_path[j]
        print(output_path)
    output_path = output_path + 'txt'
    return output_path


if __name__ == '__main__':  # 主程序入口
    input_path = '弹幕统计.xlsx'
    output_path = creat_txt(input_path)
    Excel_to_Txt(input_path, output_path)
