# https://blog.csdn.net/foruok/article/details/101678953
# https://blog.csdn.net/用户名/article/details/不知道啥id
# 主机/index            --> 所有的文章
# 主机/blog/博客id  --> 查看某篇文章
#         -------404 界面
# 主机/newblog/      --> 新建文章
#
# 主机/editblog/<博客编号id>
#                                 --> 修改文章
#
# 主机/delblog/<博客编号id>
#                                  --> 删除文章
#
# 数据库
#           文章标题title,100, 作者author 20,内容content  最多5000字
from flask import Flask, render_template, redirect, request, flash, session, escape, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:wodeniang71md@localhost/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'hahahahahaha'


# app.register_blueprint(login.bp)
class User(db.Model):
    __tablename__ = 'userall'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Integer, unique=True)
    password = db.Column(db.Integer, unique=True)
    titles = db.relationship('Usecontent', backref='blog_message')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "{'user:%s,pawd:%s'} " % (self.username, self.password)


class Usecontent(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    blog_mes = db.Column(db.Integer, db.ForeignKey('userall.id'))

    def __init__(self, title, content, blog_mes):
        self.title = title
        self.content = content
        self.blog_mes = blog_mes


db.create_all()  # 创建数据库


@app.route('/zhuye', methods=['GET', 'POST'])  # 跳到主页的界面
def zhuye():
    return render_template('主页.html')


@app.route('/blogzc.html', methods=['GET', 'POST'])  # 跳到注册的界面
def blogzc():
    return render_template('blogzc.html')


@app.route('/blogxg.html', methods=['GET', 'POST'])  # 跳到修改的界面
def blogxg():
    return render_template('blogxg.html')


@app.route('/blogsc.html', methods=['GET', 'POST'])  # 跳到删除的界面
def blogsc():
    return render_template('blogsc.html')


@app.route('/blogck.html', methods=['GET', 'POST'])  # 跳到查看的界面
def blogck():
    return render_template('blogck.html')


@app.route('/blogxj.html', methods=['GET', 'POST'])  # 跳到新建的界面
def blogxj():
    return render_template('blogxj.html')


# @app.route('/xj')
# def bolgmyxj():

@app.route('/dl', methods=['GET', 'POST'])  # 登陆界面点击立即登陆之后
def blogaction():
    name1 = request.form['name1']
    pwd1 = request.form['pwd1']
    name2 = User.query.filter(User.username).all()
    pwd2 = User.query.filter(User.password).all()
    for name in name2:
        for pwd in pwd2:
            if name1 != pwd1 and name1 == name and pwd == pwd1:
                return render_template('主页.html')


@app.route('/', methods=['GET', 'POST'])
def logintop():
    if request.method == 'GET':
        return render_template('blogdl.html')
    else:  # 这是点击登陆按钮之后的代码,如果有且仅有一个相同的username和password,则peo=Ture
        name1 = request.form['name1']
        pwd1 = request.form['pwd1']
        peo = User.query.filter_by(username=name1, password=pwd1).first()
        if peo:
            a = peo.id
            session['id'] = a
            # session['id'] = peo.id
            return render_template('主页.html')
        else:
            return render_template('blogdl.html')


@app.route('/zc', methods=['GET', 'POST'])  # 注册界面点击提交之后跳转过来
def blogjop():
    if request.method == 'POST':
        name1 = request.form['name1']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        if name1 != pwd1 and pwd1 == pwd2:
            content1 = User(name1, pwd1)
            db.session.add(content1)
            db.session.commit()
            return render_template('blogdl.html')
        else:
            return render_template('blogzc.html')
    else:
        render_template('blogzc.html')


# po = Usecontent(标题, 内容, escape(session['id']))
# db.session.add(po)
# db.session.commit()

@app.route('/writeblog', methods=['GET', 'POST'])
def writeblog():  # 这是新建博客的代码,写博客
    if request.method == 'POST':
        title1 = request.form.get('blogname')
        blogcentent1 = request.form.get('blogcontent')
        blog_new = Usecontent(title1, blogcentent1, escape(session['id']))
        db.session.add(blog_new)
        db.session.commit()
        return redirect(url_for('zhuye'))
    return redirect(url_for('blogxj'))


if __name__ == '__main__':
    app.run(debug=True)
