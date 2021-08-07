import datetime
from flask import Flask, render_template, request, make_response,jsonify
from pymongo import MongoClient
import random


app = Flask(__name__)
client = MongoClient("mongodb+srv://wolf_comos:021115@cluster0.9km7y.mongodb.net/test")
app.db = client.TheHelp
# 链接Mongodb数据库

key = False
@app.route("/", methods=["GET","POST"])
def index():
    if get_cookie():
        print("-------已经检测到用户的登陆信息--------")

    else:
        set_cookie()
        print("-------未检测到用户登录信息，开始自动设置--------")
#判定是否又cookie
    #print([e for e in app.db.entries.find({})])
    if request.method == "POST":
        entry_user = request.cookies.get("name")
        entry_content = request.form.get("content")
        print(entry_content)
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        random.seed(8)
        post_id = str(random.random()*(10^8))
        print(post_id)
        app.db.entries.insert({"content": entry_content,
                               "date": formatted_date,
                               "user": entry_user,
                               "post_id": post_id})
        #post_id = random.seed(8)
        # one_post = app.db.post
        # one_post.insert({"post_id":post_id})

    entries_with_date = [
        (
            entry["user"],
            entry["content"],
            entry["date"],
            entry["post_id"]
        )
        for entry in app.db.entries.find({})
    ]
    return render_template("index.html", entries=entries_with_date)
#网站主页
@app.route("/person_profile/")
def personal_page():
    if key == True:
        info = app.db.user_profile.find({})

        return render_template("userpanel.html", name=info["username"], likes=info["likes"],credit=info["credit"])
    else:
        return render_template("userpanel.html", name="Doge666", likes="10", credit= 15)

@app.route("/posts/")
def show_posts():
    if request.method == "POST":
        entry_content = request.form.get("chat_content")
    else:
        pass
    return render_template("tiezi.html")

@app.route("/posts/<post_id>")
def get_posts(post_id):
    post = app.db.entries
    info = post.find({"post_id": post_id})
    if info:
        return render_template("tiezi.html", content=info["content"],date=info["date"],user=info["user"],post=["post_id"])
    else:
        print("响应时间超时/未能找到页面")
@app.route("/register/")
def reg():
    entry_account = request.form.get("")
    entry_password = request.form.get("")
    entry_zan = 0
    entry_credit = 0
    app.db.user_profile.insert({"username":entry_account,"password" : entry_password, "likes":entry_zan,"credit":entry_credit})
    return """
    
    
    <html><h1>Registration Complete</h1h></html>
    
    
    """
@app.route("/login/")
def login():
    entry_account = request.form.get("")
    entry_password = request.form.get("")
    entry_zan = 0
    entry_credit = 0
    if app.db.user_profile.find({"username": entry_account, "password": entry_password}):
        global key
        key = True
        return render_template("""<html>
        Welcome come back! 
        {{ x }}
        </html>
        """, x=entry_account)
    else:
        return """<html><h1>Sorry, Can't find your information</h1></html>"""
@app.route("/update_zan",methods=["POST"])
def update_zan():
    pass
#该功能还未实现



def set_cookie():
    response = make_response("success")
    outdate = datetime.datetime.today() + datetime.timedelta(days=10)
    response.set_cookie("name","id",expires=outdate)
    return response
    #设置cookie

def get_cookie():
    all_items = request.cookies.get("name")
    return all_items
    #获取cookie


def del_cookie():
    response=make_response('delete cookie')
    response.set_cookie("name",'',expires=0)
    return response
    #删除cookie

#cookie的增删改查

# def rand_name():
#     fruit = ["apple","peach","banana","pineapple","watermellon","cocona"]
#     a = random.randint(0, 5)
#     b = random.randint(0,9)+random.randint(0,9)+random.randint(0,9)+random.randint(0,9)
#     return (fruit[a],b)

#随机生成用户名

class User():
    def __init__(self, username, password,score=0,numLikes=0):
        self.username = username
        self.password = password
        self.score = score
        self.numLikes = numLikes

    def getUsername(self):
        return self.username
    def getScore(self):
        return self.score
    def getPassword(self):
        return self.password
    def getNumLikes(self):
        return self.numLikes
    def post(self,post):
        print(post)
    def addComment(self,comment):
        print(comment)
        self.score += 10
    def giveLike(self,user):
        # 点赞功能
        user.numLikes += 1
        self.score += 1
#奖励机制管理系统，待完善

if __name__ == "__main__":
    app.run()
