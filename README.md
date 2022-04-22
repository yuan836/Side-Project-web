# Charles-Proj
side project
It is about my project. I will upload all the skills I learn and hope to keep going on the way to success and pro.

## 1.環境依賴及目錄
使用 
pyhton 3.10.0 環境
flask 21.2.3  網站架構
mongoDB  資料庫

```
project
│   README.md
│   app.py            #主程式    
│   iris_predict2.pgz #ML module for IRIS predict
│   rf_iris.py        #ML module.py << 還未壓縮
│   rf_api.py         #ML module    <<用來開啟pgz (pickle再壓縮之後) 以及定義 function 以供使用
│
└───static              #靜態檔案資料夾
│       css             #靜態CSS檔案夾
│       JS              #靜態Javascript檔案夾      
│       
└───templates           #Flask網頁模板資料夾
│
│   │   Crawler_for_Medium.html   #ajax爬蟲網頁
│   │   Crawler_for_Ptt.html      #PTT網頁爬蟲網頁
│   │   error.html                #錯誤網頁模板
│   │   forgotpassword.html       #忘記密碼確認recovery mail並返回正確或錯誤頁面( 正確寄送security code, 錯誤轉跳forgotpasswordpage.html並使用jquery控制按鈕失效、顯示錯 │   │                              錯誤轉跳forgotpasswordpage.html並使用jquery控制按鈕失效、顯示錯原因。
│   │   forgotpasswordpage.html   #忘記密碼確認security code頁面
│   │   index.html                #封面
│   │   intro.html                #首頁 顯示project有哪些
│   │   login.html                #登入頁面 
│   │   member.html               #會員系統
│   │   predict.html              #Machine Learning API 自己訓練好的ML model 視覺化呈現
│   │   profile.html              #個人資訊網頁模板
│   │   resetpassword.html        #變更 密碼 / recovery email 
│   │   setting.html              #個人資訊顯示
│   │   signup.html               #登出 清除session
│   


```
## 2.框架、資料庫及上傳網站。
使用的是python-Flask框架、MongoDB資料庫、以及使用Heroku上傳雲端。
如有任何問題可以mail至我的gmail會以最快速度回復 : eyway1234@gmail.com



![image](https://user-images.githubusercontent.com/58247533/164707758-c5e86758-fbf4-40fb-b7c7-09b6e4b99eab.png)

<p align="center"> 封面總覽  </p>
<p align="center"> 右上角是選單其餘皆為文字敘述 </p>

![image](https://user-images.githubusercontent.com/58247533/164707803-7b4eb06c-a0e7-4d83-ae06-7d72d0d45e5e.png)

<p align="center"> 功能展示頁面  </p>

## 3.作品簡單描述
### 1.會員系統:
  使用的是MongoDB資料庫(Nosql)儲存檔案。
  你可以在其中使用登入、註冊、更新密碼、更新備援郵件以及忘記密碼。
  
  步驟一:點選會員系統
  ![image](https://user-images.githubusercontent.com/58247533/164707835-cee50528-d94f-4eb6-906c-9bf005d6ba3b.png)

  
  步驟二:註冊，輸入暱稱、信箱、備援郵件(以供忘記密碼時使用)、以及密碼後即可註冊，這測完成會轉跳回登入頁面以便登入。
  ![image](https://user-images.githubusercontent.com/58247533/164644238-fe248d39-ec75-4335-a4c8-cd974025b707.png)

  
  步驟三:登入會員進入會員頁面 可以選擇RMB記住登入資訊以供期限內不用再輸入帳密，可在會員頁面確認自己的資訊以及作設定。 
  ![image](https://user-images.githubusercontent.com/58247533/164707957-a0f57866-932f-4b11-ae29-f19a4d58fbc2.png)
  
  <br/>
  ![image](https://user-images.githubusercontent.com/58247533/164708018-b0dd7b89-5bee-4c2a-a485-0be8a906fd99.png) 

  
  <p align="center"> 設定頁面 按下選紐決定你需要重設什麼資料  </p>
  
 ![image](https://user-images.githubusercontent.com/58247533/164708112-7e201737-4bb5-4d58-b5a1-48f0118940b2.png)
 <br/>
 ![image](https://user-images.githubusercontent.com/58247533/164708176-ceadfbf6-e4aa-4f4c-abba-b34fdf643750.png)


  
  步驟四:登出 右上角又sing out乙己左邊選單Account內可供登出
  ![image](https://user-images.githubusercontent.com/58247533/164708227-c279ff4a-1f09-4085-8a35-c5475a45deec.png)
  
  步驟五:忘記密碼 輸帳號之後在您帳號的備援郵件的信箱中獲取security code以做核實
  ![image](https://user-images.githubusercontent.com/58247533/164708349-f47391ef-baec-4a78-8063-3b1e8d2e264a.png)
<br/>
  ![image](https://user-images.githubusercontent.com/58247533/164707547-7e4d4f39-0a0e-453e-9144-2bdc41aa403b.png)


  ### 2.爬蟲:
  使用的是Beatifulsoup來開發爬蟲系統，獲取的檔案直接回傳在網頁上並建立超連結更視覺化的提供使用者。
  
  1.Crawler for PTT: 
      可以將想看的PTT網頁輸入至input以獲取文章標題
  ![image](https://user-images.githubusercontent.com/58247533/164708470-8f460db3-eab4-4a8c-970f-b8362b7d521c.png)
<br/>
  ![image](https://user-images.githubusercontent.com/58247533/164708539-edee85d3-6d5b-4225-adc4-e38b4d55fa5b.png)


  3.Crawler for Medium: 
      Ajax網頁的爬蟲 抓取Medium網站之文章標題
  ![image](https://user-images.githubusercontent.com/58247533/164708582-9a3ed262-11e6-4cfb-9ce3-c049f3bcd649.png)

  
  ### 3.機械學習 Machine Learning: 
  使用 Python 環境建置，採用 Random Forest 訓練模型再pickle封裝提供使用並以網頁視覺化
  
  1. Predict for IRIS 鳶尾花品種預測:
  
  ![image](https://user-images.githubusercontent.com/58247533/164708616-92386579-b158-4a04-93ff-81a66fe16c9c.png)
