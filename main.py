from flask import *
import sqlite3 as sq

app=Flask(__name__, template_folder="./template")
DATABASE=("./db/db.db")
#route main:
@app.route("/")
def main():
    return render_template("/main.html")
#route signup:
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("username")
        password=request.form.get("password")
        reppass=request.form.get("password-repeat")
        if not name or not password or reppass==password:
            with sq.connect(DATABASE) as conn:
                cur=conn.cursor()
                cur.execute("SELECT username FROM users")
                result=cur.fetchall()
            data=[]
            for item in result:
                username=item
                data.append([username])
            if "[(u'"+name+"',)]"  in str(data):
                return '<script>alert("username used.");window.location.href="/signup"</script>'
            username=request.form.get("username")
            password=request.form.get("password")
            with sq.connect(DATABASE) as con:
                con.execute("INSERT INTO users(username,password,point) VALUES (?,?,?)",(username,password,10))
                con.commit()
            return '<script>alert("your acount creatitd.");window.location.href="/login"</script>'
        return '<script>alert("fill in the blank corecly,");window.location.href="/signup"</script>'
    return render_template("/signup.html")
#route login:
@app.route("/login")
def login():
    return render_template("/login.html")
#route check:
@app.route("/check",methods=["GET","POST"])
def check():
    if request.method=="POST":
        name=request.form.get("username")
        word=request.form.get("password")
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("SELECT username FROM users")
            result =cur.fetchall()
        data=[]
        for item in result:
            username=item
            data.append([username])
        with sq.connect(DATABASE) as conn:
            cu=conn.cursor()
            cu.execute("SELECT password FROM users")
            result2=cu.fetchall()
        data2=[]
        for item in result2:
            password=item
            data2.append([password])
        with sq.connect(DATABASE) as co:
            cur2=co.cursor()
            cur2.execute("SELECT point FROM users WHERE username='"+name+"' ")
            result3=cur2.fetchall()
        data3=[]
        for item in result3:
            point=item
            data3.append([point])
        with sq.connect(DATABASE) as cn:
            curs=cn.cursor()
            curs.execute("SELECT * FROM asks WHERE get='false' ")
            results=curs.fetchall()
        asks=[]
        for item in results:
            username,question,answer,get,byans=item
            if get=="check" or get=="true":
                print("OK")
            else:
                asks.append([username,question,answer,get,byans])
        if "[(u'"+name+"',)]"  in str(data) and "[(u'"+word+"',)]" in str(data2):
            return render_template("index.html",name=name,point=data3,asks=asks)
        return '<script>alert("username or password incorect,try agian");window.location.href="/login"</script>'
    return '<script>window.location.href="/"</script>'
#route new-question :
@app.route("/new-question", methods=['GET','POST'])
def newquestion():
    if request.method=="POST":
        username=request.form.get("name")
        return render_template("new-question.html", username=username)
    return '<script>window.location.href="/"</script>'
#route answer:
@app.route("/answer", methods=["GET","POST"])
def answer():
    if request.method=="POST":
        username=request.form.get("username")
        qn=request.form.get("ques-name")
        question=request.form.get("question")
        if username ==qn:
            return '<script>alert("you can not answer your question, login again");window.location.href="/login"</script>'
        return render_template("answer.html",username=username,qn=qn,question=question)
    return '<script>window.location.href="/"</script>'
#route save new question :
@app.route("/save-new-question", methods=["GET","POST"])
def save_new_question():
    if request.method=="POST":
        username=request.form.get("username")
        question=request.form.get("question")
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("SELECT point FROM users WHERE username='"+username+"' ")
            result =cur.fetchall()
        data=''
        for item in result:
            point =item
            data=point
        def de(tex):
            text=str(tex)
            num=''
            numbers=['0','1','2','3','4','5','6','7','8','9']
            for x in range(len(text)):
                if text[x] in numbers:
                    num+=str(text[x])
            num=int(num)
            return num
        points=de(data)
        if points>9:
            point=points-10
            with sq.connect(DATABASE) as con:
                con.execute("UPDATE users SET point ='"+str(point)+"' WHERE username='"+username+"' ")
                con.commit()
            with sq.connect(DATABASE) as conn:
                conn.execute("INSERT INTO asks (username,question,answer,get) VALUES (?,?,?,?)",(username,question,'','false'))
                conn.commit()
            return '<script>alert("your question cretited now login agian.");window.location.href="/login"</script>'
        return '<script>alert("you need 10 points,you dont have 10 points");window.location.href="/login"</script>'
    return '<script>window.location.href="/"</script>'
#route save answer :
@app.route("/save-answer", methods=["POST","GET"])
def save_answer():
    if request.method=="POST":
        username=request.form.get("username")
        qn=request.form.get("qn")
        question=request.form.get("question")
        answer=request.form.get("answer")
        with sq.connect(DATABASE) as con:
            con.execute("UPDATE asks SET answer='"+answer+"'  WHERE username='"+str(qn)+"' AND question='"+question+"'  ")
            con.commit()
        with sq.connect(DATABASE) as con:
            con.execute("UPDATE asks SET get='check'  WHERE username='"+str(qn)+"' AND question='"+question+"'  ")
            con.commit()
        with sq.connect(DATABASE) as con:
            con.execute("UPDATE asks SET byans='"+username+"'  WHERE username='"+str(qn)+"' AND question='"+question+"'  ")
            con.commit()
        return '<script>alert("your answer sended.");window.location.href="/login"</script>'
    return '<script>window.location.href="/"</script>'
#route my Answers :
@app.route("/my-answers", methods=["GET","POST"])
def my_answers():
    if request.method=="POST":
        username=request.form.get("name")
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM asks WHERE username='"+username+"' AND get='check' ")
            result=cur.fetchall()
        data=[]
        for item in result:
            username,question,answer,get,byans=item
            data.append([username,question,answer,get,byans])
        return render_template("my-answers.html",data=data)
    elif request.method=="GET":
        ch=request.args.get("ch")
        if ch=="notwork":
            username=request.args.get("username")
            question=request.args.get("question")
            with sq.connect(DATABASE) as con:
                con.execute("UPDATE asks SET get ='false' WHERE username='"+username+"' AND question='"+question+"' ")
                con.commit()
            return '<script>alert("OK,log in agian");window.location.href="/login";</script>'
        username=request.args.get("username")
        question=request.args.get("question")
        byres=request.args.get("byans")
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("SELECT point FROM users WHERE username='"+byres+"' ")
            result =cur.fetchall()
        data=''
        for item in result:
            point =item
            data=point
        def de(tex):
            text=str(tex)
            num=''
            numbers=['0','1','2','3','4','5','6','7','8','9']
            for x in range(len(text)):
                if text[x] in numbers:
                    num+=str(text[x])
            num=ints(num)
            return num
        points=de(data)
        point=points+10
        with sq.connect(DATABASE) as con:
            con.execute("UPDATE users SET point ='"+str(point)+"' WHERE username='"+byres+"' ")
            con.commit()
        with sq.connect(DATABASE) as con:
            con.execute("UPDATE asks SET get ='true' WHERE username='"+username+"' AND question='"+question+"' ")
            con.commit()
        return '<script>alert("OK,log in agian");window.location.href="/login";</script>'
    return '<script>window.location.href="/"</script>'
#create db:
@app.route("/mkdb")
def mkdb():
    with sq.connect(DATABASE) as con:
        #con.execute("CREATE TABLE asks(username TEXT,question TEXT,answer TEXT,get TEXT,byans TEXT)")
        #con.execute("CREATE TABLE users(username TEXT,password TEXT,point TEXT)")
        con.commit()
    return 'OK'
#last things:
if __name__=="__main__":
    app.run()
