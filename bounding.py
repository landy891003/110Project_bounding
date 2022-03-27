import cv2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
import math

coordinate=open("number.csv","w")
EKGnumber=open("realnum.csv","r")

layout_type = ['LTTextBox', 'LTFigure', 'LTImage', 'LTCurve', 'LTRect']

scale=25/9
number=[]

big_coordinate=(0,0,2200,1700)
red_coordinate=(35,460,2146,1570)

redLower = np.array([0, 0, 0])
redUpper = np.array([180, 255, 46])

nums=EKGnumber.readlines()

for num in nums:
    list=num.split("\n")
    number.append(list[0])


# number=[861208,252690]
length=len(number)

def parse_obj(lt_objs):
 
    boxs = {x: [] for x in layout_type}
    # loop over the object list
    for obj in lt_objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):    #判斷物件屬性是否為文字
            boxs['LTTextBox'].append(obj.bbox)                      #存入該屬性所在之boxs；以此類推
        elif isinstance(obj, pdfminer.layout.LTFigure):             
            boxs['LTFigure'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTImage):
            boxs['LTImage'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTCurve):
            boxs['LTCurve'].append(obj.bbox)
        elif isinstance(obj, pdfminer.layout.LTRect):
            boxs['LTRect'].append(obj.bbox)
        else:
            raise
    return boxs

def parse_pdf(image_path):
    page_boxs = []

    fp = open(image_path, 'rb')
    parser = PDFParser(fp)
    
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    
    rsrcmgr = PDFResourceManager()

    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        boxs = parse_obj(layout._objs)
        page_sized = tuple([round(i) for i in layout.bbox])
        page_boxs.append((page_sized, boxs))
        pass
    return page_boxs

def KnockOut(image_pil):
    image_numpy = np.array(image_pil)        
    
    hsv = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2HSV)      #圖的二進制數據做顏色空間轉換
    mask = cv2.inRange(hsv, redLower, redUpper)             #控制色度、飽和度、亮度在redUpper跟redLower裡
    mask1 = cv2.bitwise_not(mask,mask)                      #將圖的二進制數據做not轉換
    
    return mask1
    # print(page_boxs[i][1])
    # print(page_boxs[i][0][3])

def coordinate_define(value,page_boxs_height):
    x0=value[0]*scale
    y0=(page_boxs_height-value[3])*scale
    x1=value[2]*scale
    y1=(page_boxs_height-value[1])*scale
    return(x0,y0,x1,y1)

def Floor(num):
    return math.floor(num)

def saveJudgment(x0,count,number):
    if Floor(x0)!=35:
        coordinate.write(real_num)
        count+=1
        path="heart_diagram\EKG_segmentation\pic\EKG_"+number+"_post_"+str(count)+".jpg"
        cv2.imwrite(path, img,[cv2.IMWRITE_JPEG_QUALITY, 100])
    return count

def IsFull(number,j,count):
    if j==4 and count!=13:
        print(number,"not full")
    else:
        print(number,"is done")

for i in range(length):
    count=0
    for j in range(1,5):
        image_path = 'heart_diagram\EKG_segmentation\EKG_segmentation_post\EKG_'+str(number[i])+'_post_'+str(j)+'.pdf'
        page_boxs=parse_pdf(image_path)
        image = convert_from_path(image_path,poppler_path = r"C:\Users\USER\Desktop\110proj\Python 3.9\poppler-21.03.0\Library\bin")

        for k in range(len(image)):
            image_pil = image[k]
            mask1=KnockOut(image_pil)

            page_boxs_height = page_boxs[k][0][3]

            for key, values in page_boxs[k][1].items():
                for value in values:
                    x0,y0,x1,y1=coordinate_define(value,page_boxs_height)

                    width=Floor(x1-x0)
                    height=Floor(y1-y0)
    
                    if x0!=x1 and y0!=y1:                      
                        real_box = (x0,y0,x1,y1) 
                        real_box_integer = tuple([round(jj) for jj in real_box])

                        if real_box_integer!=red_coordinate and real_box_integer!=big_coordinate:                        
                            real_num=str(Floor(y0))+','+str(width)+','+str(height)+"\n"
                            img=mask1[int(y0):int(y1),int(x0):int(x1)]
                            count=saveJudgment(x0,count,str(number[i])) 
    IsFull(number[i],j,count)        
   
coordinate.close()
