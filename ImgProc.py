  
##### Read and Write Image #####

def Cvt_str2list(st):
    l = len(st) - 1
    lst = list()
    i = -1
    while((i < l)):
        s = str()
        i += 1
        while((st[i] != ' ') and (i < l) ):
            s += st[i]
            i += 1
        lst.append(int(s))
    return lst
def Cvt_txt2img(f,r,c):
    import numpy as np
    a = open(f,"r")
    lst = [[0]*c]*r
    for i in range(0,r):
        lst[i] = Cvt_str2list(a.readline())
    img = np.ones((r,c),np.uint8)
    for i in range(0,r):
        for k in range(0,c):
            img[i][k] = lst[i][k]
    return img
def Cvt_img2txt(img,file_name):
    x,y = img.shape
    st = str()
    for i in range(0,x):
        for k in range(0,y-1):
            st += str(img[i][k]) + " "
        st += str(img[i][y-1])
        st += '\n'  
    a = open(file_name,"w")
    a.write(st)
    a.close()

######## Equalize Histogram #########

def Calc_Histogram(img):
    if(len(img.shape)!=2):
        print("Input image must be Gray_image")
        return -1
    lst = [0]*256
    x,y = img.shape
    for i in range(0,x):
        for k in range(0,y):
            lst[img[i,k]] += 1
    return lst
def Calc_CF(hist):
    lst = [0]*256
    for i in range(0,256):
        lst[i] = sum(hist[:i+1])
    return lst
def EqualizeHistogram(img):
    hist = Calc_Histogram(img)
    CF = Calc_CF(hist)
    min_value = int(min(CF))
    max_value = int(max(CF))
    x,y = img.shape
    img1 = img.copy()
    lst = [0] * 256
    for i in range(0,256):
        lst[i] = int(( (CF[i] - min_value)/(max_value - min_value) )*254) +1
    for i in range(0,x):
        for k in range(0,y):
            img1[i,k] = lst[img1[i,k]]
    return img1
def BuildGraphHist(img,Color):
    from matplotlib import pyplot as plt
    lt = [str(i) for i in range(0,256)]
    hist = Calc_Histogram(img)
    CF = Calc_CF(hist)
    plt.subplot(131),plt.bar(lt,hist,color = Color),plt.title('Histogram')
    plt.xlabel("intensity"),plt.ylabel("pixels"),plt.xlim(0,255)
    plt.subplot(133),plt.bar(lt,CF,color = Color),plt.title('CF')
    plt.xlabel("intensity"),plt.ylabel("pixels"),plt.xlim(0,255)
    plt.show()
def Compare(img):
    img1 = EqualizeHistogram(img)
    img2 = cv.equalizeHist(img)
    x,y = img.shape
    acr = [0]*(x*y)
    for i in range(0,x):
        for k in range(0,y):
            acr[i+k] = int(img1[i,k]) - int(img2[i,k])
        
    a = 1 - sum(acr)/(x*y)
    return a

######### Median Filter #########

def take_med(lst):
    lst.sort()
    med = int(len(lst) / 2)
    return lst[med]
def MedFilter(img,d):
    l = int(d/2)
    x,y = img.shape
    img1 = img.copy()
    for i in range(0,x):
        for k in range(0,y):
            lst = list()
            for n in range(-l,l+1):
                for m in range(-l,l+1):
                    if((i-n >= 0) and (i-n < x-1) and (k-m >= 0) and (k-m < y)):
                        lst.append(img[i-n,k-m])
            img1[i,k] = take_med(lst)
    return img1
def Compare(img1,img2):
    x,y = img1.shape
    acr = [0]*(x*y)
    for i in range(0,x):
        for k in range(0,y):
            acr[i+k] = int(img1[i,k]) - int(img2[i,k])
        
    a = 1 - sum(acr)/(x*y)
    return a
import cv2 as cv
st = str(input("File name: "))
img = Cvt_txt2img(st,512,512)
img1 = EqualizeHistogram(img)
img2 = MedFilter(img,5)
cv.imshow("Orginal image",img)
cv.imshow("After Equalizing Histogram",img1)
cv.imshow("After Filting",img2)
cv.waitKey(0)
cv.destroyAllWindows()