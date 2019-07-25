# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 17:29:45 2017

@author: Monana serena9636@163.com
"""

import time
import pandas as pd
import winsound
import pickle
import numpy as np
import os
from pronounce import apicatch

class WordTest():
    
    def __init__(self,filename=None,filelist=None,
                 start=0,end='last',mode='order',score=True,
                 save=False,csvsep='\t',myorder=None,
                 *args,**kwargs):
        '''
        end: the end of words print, default 'last' will print all words.
        '''
        
        #传入的是几个文件['F13.xlsx','F14.xlsx']这样的
        if filelist:
            self.filelist=[]
            self.data=pd.DataFrame(columns=['English','Chinese'])
            for eachfile in filelist:
                self.filelist.append(eachfile)
                if eachfile[-4:]=='xlsx':
                    data=pd.read_excel('words/'+eachfile)
                else:
                    data=pd.read_csv('words/'+eachfile,sep=csvsep,header=None,names=['English','Chinese'], error_bad_lines=False)
                self.data=pd.concat([self.data,data])

        
        #传入的是单个文件可以是csv或者xlsx
        if filename:
            self.filename=filename
            if filename[-4:]=='xlsx':
                self.data=pd.read_excel('words/'+filename)
            else:
                self.data=pd.read_csv('words/'+filename,sep=csvsep,header=None,names=['English','Chinese'], error_bad_lines=False)
                
                
        self.start=start
        self.end=end
        self.wrongflag=False
        self.wrong=[]
        self.save=save
        self.score=score
        self.mode=mode#random order review
        self.myorder=myorder
        print("初始化测试")
        print("如果单词发音卡顿，请尝试将VPN切换至PAC。")
        
        if not self.score:
            print("Review模式：score=False，不计分也不记录本次学习数据，一直按回车键即可。")
        else:
            print("计分模式：正确按回车，错误或者想不起来按任意键，退出按q。")
#    def time_me(self,fn):
#        def _wrapper(*args, **kwargs):
#            start = time.clock()
#            fn(*args, **kwargs)
##            print("%s cost %s second"%(fn.__name__, time.clock() - start))
#            print("共花费 %s second"%(time.clock() - start))
#            return _wrapper   
        
        self.wrongstack=[]#专门用来背错词的栈

    def main(self,data):

        
        English=data['English']
        Chinese=data['Chinese']
        wrong=0
        right=0
        wrong_index=[]
        word_num=len(English)
        word_count=0 #背了多少个单词计数
        if len(self.wrong)!=0 and self.wrongflag:
            #错词巩固模式
            order=np.arange(0,word_num)
            order=np.random.permutation(order)
            self.save=False
            
        else:
            #不是错词巩固，是正常背诵单词时
            if self.end=='last':
                self.end=word_num
            if self.end>word_num:#当输入的end多余单词个数，防止溢出
                self.end=word_num
            order=np.arange(0,word_num)
            order=order[self.start:self.end]
            if self.mode=='random':
                order=np.random.permutation(order)#这里的order就已经是被截取过的
                
            
        if type(self.myorder)==np.ndarray:#如果myorder存在，使用预置
            order=self.myorder#这里myorder是完整的
            order=order[self.start:self.end] #这里再把order截取一次
            print("使用预置的myorder",order[0:3])
            
        self.order=order
        
        
        print("本次单词范围%s~%s,%s/%s"%(self.start,self.end,len(order),word_num))
        print("==========================")
        for i in order:
            #打印单词
            word_count+=1
            if word_count%10==0:
                print(word_count,"/",len(order))
            current_word=English.values.tolist()[i]
            print(i,".",current_word)
            if not os.path.exists(current_word+".mp3"):
                apicatch(current_word,"2")
            self.playmp3("audio/"+current_word+".mp3")
            

            #打印出英文单词，输入任意键到中文单词
            input1=input()
            
            print(Chinese.values.tolist()[i])
            #退出条件
            if input1=='q' or i==order[-1]:
                ctime = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
                
                print(ctime)
                print('Words Test Finished!')

                self.playSound("finish")
                
                if self.score:
                    print('本次共检测%s个单词。正确%s个，错误%s个，正确率%s。'%(right+wrong,right,wrong,right/(right+wrong)))
                    if wrong==0 and right>=5:
                        print("一个没错，完美学神！")
                        break

                    else:
                        print("记得不熟，多背几遍哦！")
                        print("出错的单词:")
                        print(data.iloc[wrong_index])
                        #TODO 后期把这个if条件判断去掉，太蠢
                        if not self.wrongflag:
                            self.wrong=data.iloc[wrong_index]
                            self.wrongstack.append(self.wrong)
                            if self.save==True:
                                print("正在写入excel")
                                self.wrong.to_csv('words/wrong.csv',index=False,header=False,sep='\t')

                break
            #打印出中文释义
            
            #回车对，其他任意是错 
            input2=input()
            if input2!='q':
                if input1!='' or input2!='':
                    wrong+=1
                    wrong_index.append(i)
                    self.playSound("wrong")
                else:
                    right+=1
                    if self.score:
                        self.playSound("right2")
  
        self.record={"ctime":ctime,
        "word_num":word_num,"right":right,"wrong":wrong,
        "wrong_index":wrong_index,"wrong_words":data.iloc[wrong_index]}

        return self.record
        

    
    def about():
        print("Monana喜欢背单词！")
        
    def playSound(self,sound):
    #播放猜对猜错音效
#        winsound.PlaySound(sound, winsound.SND_ALIAS)
        winsound.PlaySound(sound, winsound.SND_ASYNC)
        
        
    def playmp3(self,sound):
        #播放单词发音
        import pygame  
        pygame.mixer.init()  
#        sound='abeyance.mp3'
        try:
            pygame.mixer.music.load(sound)  
        except:
            print('pronounce error..')
            pass
        pygame.mixer.music.play()
        
    def saveRecord(self,record):
        recordfile='record/record-'+self.record['ctime']+'.pickle'
#        pickle.dump(str(record), open(recordfile, 'w'))
        with open(recordfile, 'wb') as handle:
            pickle.dump(record, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    def loadRecord(self,record):
        if type(record)==str:
            with open(record, 'rb') as handle:
                record = pickle.load(handle)
        return record

    def go(self):
        #主程序，直接运行
        record=self.main(self.data)
        if self.score:
            self.saveRecord(record)  

    def keywords(self):
        return self.data.iloc[self.forget]
    
    def printAccuracy(self,record):
        pass
    
#TODO 还需要完善的错题模式很不智能
    def wrongmode(self):
        self.wrongflag=True
#        if len(self.wrongstack)!=0:
#            self.realwrong=self.wrongstack[-1]#取栈顶元素
#        while(len(self.realwrong)==0 and len(self.wrongstack)!=0):
#            print(self.wrongstack)
#            self.realwrong=self.wrongstack.pop()#每次只取最新的一个
        self.main(self.wrong)
        
    
    #按照自定义顺序打印
    @property
    def data2(self):
        self.data.iloc[self.order]

        

if __name__=='__main__':
    
#    test1=WordTest(filename='toefl.tsv',start=48,end='last',mode='order',score=False,save=False)
#    test1=WordTest(filename='F17.xlsx',start=0,end=30,mode='random',score=True,save=True)
#    test1=WordTest(filename='F14.xlsx',start=40,end=60,mode='random',score=True,save=1)
#    
    
    #%%下面是多个单词
#    lista=['F2.xlsx','F6.xlsx','F7.xlsx','F8.xlsx','F9.xlsx','F10.xlsx','F11.xlsx','F12.xlsx','F13.xlsx','F14.xlsx','F15.xlsx','F16.xlsx']
#    test2=WordTest(filelist=lista,start=0,end='last',mode='random',score=True,save=1)
#    test2.go()
    
    #%%
    #words/1~16.npy导入到变量区，改名称aa
    test1=WordTest(filelist=lista,start=550,end=600,mode='random',score=True,save=1,myorder=aa)
    #test1.data.iloc[test1.myorder][550:600]
    #错题
    test1=WordTest(filename='F17.xlsx',start=0,end=90,mode='random',score=True,save=1)
#    test1=WordTest(filename='geo',csvsep=',',start=0,end=20,mode='order',score=True,save=1)
#    test1=WordTest(filename='wrong1~15',start=40,end='last',mode='random',score=True,save=1)
#    test1.wrongmode()
    
    
    test1.go()
#    print(test1.wrong_data)


