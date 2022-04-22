# pip install pymongo[srv]
# pip install beautifulsoup4
# pip install bson
# pip install json_util 
# pip install Flask
# pip install flask-mail
# 初始化資料庫連線
from bson.json_util import dumps
import json
import pymongo
import numpy as np
import rf_api
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster.3uih5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.member_system #操作資料庫的名稱
print('資料庫連線建立成功')
# 初始化 Flask 伺服器
from flask import *
app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/')

app.secret_key='any string but secret'
# 設定session存活時間 5分鐘
from datetime import *
# timedelta
app.config["PERMANENT_SESSION_LIFETIME"]= timedelta(minutes=5)


# 傳送email 需安裝 flask-email
from flask_mail import Mail, Message

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Charles.AutoSent@gmail.com'
app.config['MAIL_PASSWORD'] = 'wasungzlzkzbeyox'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# https://blog.user.today/gmail-smtp-authentication-required/ 登入信箱被拒絕參考這篇文章解決


import random
import string

#處理路由
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/introduction')
def intro():
    return render_template('intro.html')


@app.route('/login' , methods=["POST","GET"])
def login():
    if 'user' in session:
        return redirect('/member')
    else:
        session.clear()
        return render_template('login.html')

@app.route('/signuppage')
def signupapge():
    return render_template('signup.html')

@app.route('/member')
def member():
    # return render_template('member.html')
    if 'user'in session:
        return render_template('member.html')
    else:
        return redirect('/login')

@app.route('/profile')
def profile():
    if 'user' in session:
        collection = db.users
        getdata = collection.find_one({
            'email':session['user']['email']
        })
        data = dumps(getdata) #此時還是str
        # 轉json格式的dict
        data_json = json.loads(data)
        del data_json['password']
        return render_template('profile.html',data=data_json)
    else:
        return redirect('/login')
@app.route('/setting',methods=['GET'])
def setting():
    if 'user' in session:
        collection = db.users
        getdata = collection.find_one({
            'email':session['user']['email']
        })
        data = dumps(getdata) #此時還是str
        # 轉json格式的dict
        data_json = json.loads(data)
        del data_json['password']
        print(data_json)
        return render_template('setting.html',data=data_json)
    else:
        return redirect('/login')

@app.route('/reset', methods=["POST"])
def reset():
   
    collecotion = db.users
    Remail = request.form.get('Remail')
    password = request.form.get('password')
    if Remail != None:
        collecotion.update_one(
            {'email' : session['user']['email']},
            {"$set": {
                'Remail' : Remail
            }}
        )
        return redirect('/member')
    else:
        collecotion.update_one(
            {'email' : session['user']['email']},
            {"$set": {
                'password' : password
            }}
        )
        return redirect('/signout')

@app.route('/signup', methods=["POST"])
def signup():
    # 從前端接收資料
    nickname = request.form['nickname']
    email = request.form['email']
    Remail = request.form['Remail']
    password = request.form['password']
    # 根據接收到的資料與資料庫互動
    collition = db.users
    # 檢查會員集合中是否有相同 email 的文件資料
    email_check = collition.find_one({
        'email':email
    })
    if email_check != None:
            return redirect('/error?msg=信箱已經被註冊')
        # 把資料放進資料庫，完成註冊
    else: 
        collition.insert_one({
            'nickname':nickname,
            'email':email,
            'Remail':Remail,
            'password':password,
            'security_code':''
        })
        return redirect('/introduction')
    
@app.route('/signin', methods=["POST"])
def signin():
    # 從前端取得使用者輸入的資料
    email = request.form['email']
    password = request.form['password']
    ses = request.form['ses']
    
    # 根據接收到的資料與資料庫互動
    collition = db.users
    # 檢查會員集合中是否有相同 email 的文件資料 和密碼正確與否
    member_check = collition.find_one({
        '$and':[
            {'email':email},
            {'password':password}
        ]
    })

    if ses =='0' :
    
        if member_check == None:
            return redirect('/error?msg=帳號或密碼錯誤')
        else:
            print('ses=0')
            session['user'] = { 'email': member_check['email'],
                    'switch': ses
                    }     
            print(f'session: {session}')
            return redirect('/member')
            
    else:
        if member_check == None:
            return redirect('/error?msg=帳號或密碼錯誤')
        else:
            print('ses=1')
            app.config["PERMANENT_SESSION_LIFETIME"]= timedelta(minutes=30) 
            session['user'] = { 'email': member_check['email'],
                    'switch': ses
                    }
            print(f'session: {session}')
            return redirect('/member')

@app.route('/forgotpassword')
def forgot():
    return render_template('/forgotpassword.html')

@app.route('/getremail', methods=["GET","POST"])
def forgetpasswordpage():
    
    email = request.form['email']
    collition = db.users
    user = collition.find_one({
        'email':email
    })
    print(f'email: {email}')
    print(f'getremail: {user}')
    if user != None:
        if '@' not in user['Remail']:
            user['Remail'] = 'is not be a emaill address'
            return render_template('forgotpasswordpage.html',data=user)            
        else:
            app.permanent_session_lifetime = timedelta(minutes=15)# session失效時間
            print('session reset 15mins 更改成功')
            Remail = user['Remail']
            remail = user['Remail']
            print(f'remail: {remail}')
            x = 'x'
            y = remail.find('@')
            for i in range(2,y-2):
                remail = remail[:i] + x + remail[i+1:]
            user['Remail'] = remail
            del user['password']
                        
            # 用string 取 英文 數字 區間會比用ASCII直接取來的方便
            # string.digits > 0123456789 string.ascii_letters > 大小寫混和

            random_code = ''.join(random.sample(string.digits + string.ascii_letters,6))
            print(random_code)
            user['security_code'] = random_code
            print(f'user: {user}')

            # 更新資料哭 上傳驗證碼            
            collition.update_one(
               {"email" : email },
               {"$set": {"security_code": random_code}}
            )

            #  主旨
            msg_title = "Hello It is security code for Charles's website Account. "
            #  寄件者，
            msg_sender = 'Charles.AutoSent@gmail.com'
            #  收件者 > list
            msg_recipients = [f'{Remail}']
            #  mail內容
            # msg_body = 'Hey, I am mail body! <h1>Hey,Flask-mail Can Use HTML</h1>'
            #  也可以使用html
            msg_html = f"<h1>Hello {user['nickname']}:</h1><blockquote><h3 style='color:grey;font-weight:300;'>Charles's Website Account</h3><h1 style='color:rgb(75, 75, 245);font-weight:800;'>security code</h1><p>Reset password for {user['email']} Please use the following security code.</p><br><p>security code: <span style='color:rgb(231, 24, 24);font-weight:800;font-size:30px'>{random_code}</span></p><br><p>Thank you!!</p><p>Charles's Web Account Team</p></blockquote>"
            msg = Message(msg_title,
                        sender=msg_sender,
                        recipients=msg_recipients)
            # msg.body = msg_body
            msg.html = msg_html
            
            #  寄出 記得打開
            mail.send(msg)
            # print('\n'+'sent!!'+'\n')

            # 紀錄session以便進入reset頁面判斷
            session['reset'] ={
                'security_code' : 'exist' ,
                'Remail' :  remail
            } 
            print(f'session: {session}')
            print(f'user: {user}')
            return render_template('forgotpasswordpage.html',data=user)
    else:
        return redirect('/error?msg=帳號不存在')
        
@app.route('/resetpassword', methods=["GET","POST"])
def getremail():
    collition = db.users
    code = request.form['code']
    db_code = collition.find_one({
        'security_code' : code
    })
    print(f'db_code: {db_code}')
    if 'reset' in session:
        if db_code != None:
            dic={
                'email' : db_code['email'],
                'nickname' : db_code['nickname']
            }
            
            return render_template('resetpassword.html',data=dic)
        else:
            dic={ 'Remail' :  session['reset']['Remail'],
                'error' : 'incorrect security code '
            }
            return render_template('forgotpasswordpage.html',data=dic)
    else:
        return redirect('/error?msg=驗證錯誤')
@app.route('/update',methods=["POST"])
def updatenewpassword():
    collition = db.users
    email = request.form['email']
    password = request.form['password']
    print(f'email: {email}')
    print(f'password: {password}')
    collition.update_one(
        {"email" : email },
        {"$set": {"password": password}}
    )
    return redirect('/login')

@app.route('/signout')
def signout():
    if 'user' in session:
        # 移除 session 中的會員資訊
        # del session['user']
        session.clear()
        print(f'session: {session}')
        return redirect('/introduction')
    else:
        print(f'session: {session}')
        return redirect('/introduction')

# /error?msg=錯誤訊息
@app.route('/error')
def error():
    msg = request.args.get('msg','發生錯誤請聯繫客服')
    return render_template('error.html',msg=msg)


@app.route('/Crawler_for_Ptt',methods=['POST','GET'])
def crawler():
    if request.method=='POST':
        href = request.form['url']
        result = crawler(href)

        # json字串化
        return json.dumps(result)
    else:
        return render_template('Crawler_for_Ptt.html')


import urllib.request as req
def crawler(url):
    url_i = url
    # 建立一個 Request 物件, 附加 Request Headers 的資訊
    request = req.Request(url_i, headers={
        "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    # 解析原始碼, 取得每篇的文章標題
    import bs4
    root = bs4.BeautifulSoup(data, 'html.parser')

    dic={
        'result':[],
        'url':[]
    }
    dic_t={
    'result':[]
    }
    i=0

    titles_all = root.find_all('div',class_='title')

    for title in titles_all:
        if title.a != None: #標題包含 a 標籤則印出來
            dic_a= f'"標題" : {str(title.a.string)}'
                
            dic['result'].append(dic_a)
            i+=1

    for title in titles_all:
        if title.a != None: #標題包含 a 標籤則印出來
            dic_a=f'標題 : {str(title.a)}'
                    
            dic_t['result'].append(dic_a)
            
    for i in dic_t['result']:
        # print(i)
        if 'href=' in i:
            x = i.find('hr')
            y = i.find('">')
            z=i[x:y]
            url="https://www.ptt.cc"
            url+=z[6:]
            # print(url)
            dic['url'].append(url)
            
    return dic

@app.route('/Crawler_for_Medium',methods=['POST','GET'])
def crawler2():
    if request.method=='POST':
        href = request.get_json()['url']  # 但先不使用 之後可以用前端維護 但我喜歡後端直接改所以不用 展示而已
        url = 'https://medium.com/_/graphql'
        result = crawler2(url)
        return json.dumps(result)
    else:
        return render_template('Crawler_for_Medium.html')

def crawler2(url):
    
    requestData = {"operationName":"TopicHandlerHomeFeed","variables":{"topicSlug":"editors-picks","feedPagingOptions":{"limit":25,"to":"1650296138639"}},"query":"query TopicHandlerHomeFeed($topicSlug: ID!, $feedPagingOptions: PagingOptions) {\n  topic(slug: $topicSlug) {\n    ...CuratedHomeFeedItems_topic\n    __typename\n  }\n}\n\nfragment CuratedHomeFeedItems_topic on Topic {\n  id\n  name\n  latestPosts(paging: $feedPagingOptions) {\n    postPreviews {\n      postId\n      post {\n        id\n        ...HomeFeedItem_post\n        __typename\n      }\n      __typename\n    }\n    pagingInfo {\n      next {\n        limit\n        to\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...OverflowMenuButtonWithNegativeSignal_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  __typename\n}\n\nfragment OverflowMenuButtonWithNegativeSignal_post on Post {\n  id\n  ...OverflowMenuWithNegativeSignal_post\n  ...CreatorActionOverflowPopover_post\n  __typename\n}\n\nfragment OverflowMenuWithNegativeSignal_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  __typename\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  inResponseToPostResult {\n    __typename\n  }\n  inResponseToCatalogResult {\n    __typename\n  }\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...useIsPinnedInContext_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  ...OverflowMenuItemUndoClaps_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isNewsletter\n  isAuthorNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n"}
    request = req.Request(url,headers={
        "Content-Type":"application/json",
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }, data = json.dumps(requestData).encode("UTF-8")
    ) #data為請求的而外資料

    #發出請求
    with req.urlopen(request) as response:
        result = response.read().decode("UTF-8")
    # print(result)

    # 解析 JSON 格式資料, 取得每篇文章標題
    result = json.loads(result) #字串轉字典

    # print(result['data']['topic']['latestPosts']['postPreviews'][0]['post']['title'])
    items = result['data']['topic']['latestPosts']['postPreviews']
    
    dic={
    'result':[],
    'url':[]
    }
    for i in items:
        dic_t = f"title: {i['post']['title']}"
        dic['result'].append(dic_t)
        dic_u = i['post']['mediumUrl']
        dic['url'].append(dic_u)
    # json字串化
    return dic

@app.route('/predict', methods=['POST','GET'])
def predict_func():
    if request.method=='POST':
        insertValues = request.get_json()
        # x1 =  insertValues['url']
        x1 = insertValues['sepalLengthCm']
        x2 = insertValues['sepalWidthCm']
        x3 = insertValues['petalLengthCm']
        x4 = insertValues['petalWidthCm']
        input = np.array([[x1,x2,x3,x4]])

        result = rf_api.predict(input)
        print(input)
        if result == 0:
            result = 'setosa'
        elif result == 1:
            result = 'versicolor'
        else:
            result = 'virginica'
        return result
    else:
        return render_template('predict.html')

# # 重新整理刷新session 
@app.before_request 
def make_session_permanent():
    
    if 'user' in session:
        if session['user']['switch'] == '0':
            app.permanent_session_lifetime = timedelta(minutes=5)# session失效時間
            print('session ses = 0 更改成功')
        else: 
            print('session ses = 1不用更改')
    else:
        print('session 沒有 user')
        
            
# # 傳送email 需安裝 flask-email
# from flask_mail import Mail, Message

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'Charles.AutoSent@gmail.com'
# app.config['MAIL_PASSWORD'] = 'wasungzlzkzbeyox'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)

# # https://blog.user.today/gmail-smtp-authentication-required/ 登入信箱被拒絕參考這篇文章解決
# @app.route("/message")
# def message():
#     #  主旨
#     msg_title = 'Hello It is Flask-Mail'
#     #  寄件者，
#     msg_sender = 'Charles.AutoSent@gmail.com'
#     #  收件者 > list
#     msg_recipients = ['eyway1234@gmail.com']
#     #  mail內容
#     msg_body = 'Hey, I am mail body! <h1>Hey,Flask-mail Can Use HTML</h1>'
#     #  也可以使用html
#     msg_html = '<h1>Hey,Flask-mail Can Use HTML</h1>'
#     msg = Message(msg_title,
#                   sender=msg_sender,
#                   recipients=msg_recipients)
#     msg.body = msg_body
#     msg.html = msg_html
    
#     #  寄出
#     mail.send(msg)
#     return 'You Send Mail by Flask-Mail Success!!'
# https://hackmd.io/@shaoeChen/BytvGKs4M?type=view


if __name__ == "main":
    app.run(port=1028)    