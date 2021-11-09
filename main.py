from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.graphics.charts.legends import Legend


pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))  #注册字体
doc = SimpleDocTemplate("实验报告(样例).pdf")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(fontName='SimSun', name='Song', leading=20, fontSize=12, alignment=TA_CENTER))  #自己增加新注册的字体

#段落
title_style = styles['Song']

story = list()
story.append(Paragraph("实验报告", title_style))

data= [['实验ID', '实验类型', '实验时间', 'Accuracy'],
['Task01', 'xgboost', '2012-12-01', '0.95']]


t = Table(data)
t.setStyle(TableStyle(
    [
    ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
    ("FONTNAME", (0, 0), (-1, -1), ('SimSun'))
    ]

))
story.append(t)


#图片
fig = plt.figure(figsize=(4, 3))
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.title("Image",)
fp = BytesIO()

fig.savefig(fp, dpi=500, format="jpeg")
fp.seek(0)
image = Image(fp, useDPI=True)
story.append(image)

#矢量图
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.textlabels import Label

def autoLegender(chart, categories=[], use_colors=[], title=''):
    width = 448
    height = 230
    d = Drawing(width, height)
    lab = Label()
    lab.x = 220  #x和y是title文字的位置坐标
    lab.y = 210
    lab.setText(title)
    lab.fontName = 'SimSun' #增加对中文字体的支持
    lab.fontSize = 20
    d.add(lab)
    d.background = Rect(0,0,width,height,strokeWidth=1,strokeColor="#868686",fillColor=None) #边框颜色
    d.add(chart)
    #颜色图例说明等
    leg = Legend()
    leg.x = 500   # 说明的x轴坐标
    leg.y = 0     # 说明的y轴坐标
    leg.boxAnchor = 'se'
    # leg.strokeWidth = 4
    leg.strokeColor = None
    leg.subCols[1].align = 'right'
    leg.columnMaximum = 10  # 图例说明一列最多显示的个数
    return d

def draw_bar_chart(min, max, x_list, data=[()], x_label_angle=0, bar_color=HexColor("#7BB8E7","#7B08E7" ), height=125, width=280):
    '''
    :param min: 设置y轴的最小值
    :param max: 设置y轴的最大值
    :param x_list: x轴上的标签
    :param data: y轴对应标签的值
    :param x_label_angle: x轴上标签的倾斜角度
    :param bar_color: 柱的颜色  可以是含有多种颜色的列表
    :param height: 柱状图的高度
    :param width: 柱状图的宽度
    :return:
    '''
    bc = VerticalBarChart()
    bc.x = 50            # x和y是柱状图在框中的坐标
    bc.y = 50
    bc.height = height  # 柱状图的高度
    bc.width = width    # 柱状图的宽度
    bc.data = data
    for j in range(len(x_list)):
        setattr(bc.bars[j], 'fillColor', bar_color)  # bar_color若含有多种颜色在这里分配bar_color[j]
    # 调整step
    minv = min * 0.5
    maxv = max * 1.5
    maxAxis = int(height/10)
    # 向上取整
    minStep = int((maxv-minv+maxAxis-1)/maxAxis)

    bc.valueAxis.valueMin = min * 0.5      #设置y轴的最小值
    bc.valueAxis.valueMax = max * 1.5      #设置y轴的最大值
    bc.valueAxis.valueStep = (max-min)/4   #设置y轴的最小度量单位
    if bc.valueAxis.valueStep < minStep:
        bc.valueAxis.valueStep = minStep
    if bc.valueAxis.valueStep == 0:
        bc.valueAxis.valueStep = 1
    bc.categoryAxis.labels.boxAnchor = 'ne'   # x轴下方标签坐标的开口方向
    bc.categoryAxis.labels.dx = -5           # x和y是x轴下方的标签距离x轴远近的坐标
    bc.categoryAxis.labels.dy = -5
    bc.categoryAxis.labels.angle = x_label_angle   # x轴上描述文字的倾斜角度
    bc.categoryAxis.labels.fontName = 'SimSun'
    x_real_list = []
    if len(x_list) > 10:
        for i in range(len(x_list)):
            tmp = '' if i%5 != 0 else x_list[i]
            x_real_list.append(tmp)
    else:
        x_real_list = x_list
    bc.categoryAxis.categoryNames = x_real_list
    return bc


z = autoLegender(draw_bar_chart(100, 300, ['a', 'b', 'c'], [(100, 200, 120), (90, 250, 60)]), title="图形Figure")
story.append(z)

doc.build(story)
