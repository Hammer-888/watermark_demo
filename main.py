import argparse
from src.attack  import attack_m,attack_method
from src.DCT_method import  WaterMark
from src.LSB_method import IMG_LSB
import cv2

class LSB:
    '''
    it needs three parameter:
    method: attack method,default 'ori'
    ori_filename: carrier image path
    wm_filename: watermark image path

    '''

    def __init__(self,method,ori_filename,wm_filename):
        self.method = method #load attack method
        self.ori_filename = ori_filename
        self.wm_filename = wm_filename
        self.ori_wm_filename = './img/ori_LSB_wm.png' #default watermarked image path

    def encoder(self):
        m=IMG_LSB() # load encoder model
        ori_wm_img = m.create_cover(self.ori_filename, self.wm_filename)
        if self.method in attack_method:
            att_img = attack_m(ori_wm_img,self.method)
            self.ori_wm_filename = './img/'+self.method+'_LSB_wm.png'
            cv2.imwrite(self.ori_wm_filename, att_img)
        else:
            print('THT ATTACK METHOD is NOT CONTAIN') 
    def decoder(self): 
        #define the default recover watermark save path is under './img/' 
        m = IMG_LSB()# load decoder model
        m.extract_img(self.wm_filename,self.ori_wm_filename, './img/'+self.method+'_LSB_re_wm.png')



class DCT:
    ''' 
    KEY POINT: the carrier image size  should  16 times greater than watermark,or it doesn't work.
    it also needs three parameter:
    method: attack method,default 'ori'
    ori_filename: carrier image path
    wm_filename: watermark image path
    '''
    def __init__(self,method,ori_filename,wm_filename):
        self.method=method #load attack method
        self.ori_filename=ori_filename
        self.wm_filename=wm_filename

        self.ori_wm_filename='./img/ori_DCT_wm.png' #default watermarked image path
        self.password_wm=100#init random seed
        self.password_img=11#init random seed
    def encoder(self):
        m = WaterMark(password_wm=self.password_wm,password_img=self.password_img) #init random seed
        m.read_img(self.ori_filename) #load carrier image
        m.read_wm(self.wm_filename) #load watermark
        ori_wm_img=m.embed() #encode ori image
        if self.method in attack_method:
            att_img=attack_m(ori_wm_img,self.method)
            self.ori_wm_filename = './img/'+self.method+'_DCT_wm.png'
            cv2.imwrite(self.ori_wm_filename, att_img)
        else:
            print('THT ATTACK METHOD is NOT CONTAIN') 
    def decoder(self):
        #define the default recover watermark save path is under './img/' 
        m = WaterMark(password_wm=self.password_wm,password_img=self.password_img) #init random seed
        wm_shape=cv2.imread(self.wm_filename).shape
        m.extract(self.ori_wm_filename,wm_shape[:2],out_wm_name='./img/'+self.method+'_DCT_re_wm.png') # extract watermark






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wm_method',type = str,default='DCT',help = 'watermark method,include LSB method,DCT method')
    parser.add_argument('--coder',type=str,default='encoder',help='select encoder or decoder')
    parser.add_argument('--ori_filename',type = str,help = 'watermark carrier image path')
    parser.add_argument('--wm_filename',type = str,help = 'watermark image path')
    parser.add_argument('--ori_wm_filename',type = str,help = 'watermarked image save path')
    parser.add_argument('--att_method',type = str,default='ori',help = 'image attack method')
    opt = parser.parse_args()

    if opt.wm_method == 'DCT':
        model=DCT(opt.att_method,opt.ori_filename,opt.wm_filename)
        if opt.coder == 'encoder':
            model.encoder()
        if opt.coder == 'decoder':    
            model.decoder()
    elif opt.wm_method == 'LSB':
        model=LSB(opt.att_method,opt.ori_filename,opt.wm_filename)
        if opt.coder == 'encoder':
            model.encoder()
        if opt.coder == 'decoder':    
            model.decoder()
    else:
        print('THE WATERMARK METHOD is WRONG')
