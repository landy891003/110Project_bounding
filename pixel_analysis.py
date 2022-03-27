import cv2
from PIL import Image
import xlsxwriter

def openfile(str):
    file=open(str,"r")
    text=file.read().splitlines()
    file.close()
    return text

def save_excel(str,arry):
    with xlsxwriter.Workbook(str) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(arry):
            worksheet.write_row(row_num, 0, data)

def pixelAnalysis():
    for j in range(line[count][1]):                
        for i in range(line[count][2]):
            r, g, b = im.getpixel((j, i))
            if(r<200 and g<200 and b<200):
                columnA = (x0+j)*5
                columnB = (real_coordinate-i)/8
                print(start,count,real_coordinate,'x',x0+j,'y',line[count][0]+i,columnA,'ms',columnB,'mV')
                LongQT.append([x0+j,line[count][0]+i,columnA, columnB])

count=0
LongQT,line=[],[]

coords = openfile("number.csv")
number = openfile("realnum.csv")

coordinates=[coord.split(",") for coord in coords]

for coordinate in coordinates:
    line.append([int(pos) for pos in coordinate])

for n in range(len(number)):
    start,x0=579,79
    # LongQT.append(['x','y','ms','mV'])
    
    for k in range(1,14):    
        real_coordinate=start-line[count][0]
        im = Image.open("heart_diagram\EKG_segmentation\pic\EKG_"+number[n]+"_post_"+str(k)+".jpg").convert('RGB')    
        pixelAnalysis()  

        if k%4==0:
            start+=291
            x0=79
        else:
            x0+=line[count][1]
        count+=1
        # LongQT.append(['BP','BP','BP','BP'])

    print(number[n],'is done')
    save_excel(number[n]+'.xlsx',LongQT)    
    LongQT.clear()


