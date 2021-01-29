from flask import Flask, g, request, Response, make_response, render_template, Markup
from datetime import datetime, date

from werkzeug.utils import redirect

app = Flask(__name__)
app.debug = True




# ==== Routing ====
# @app.route('/test')
# def …

# @app.route('/test', methods=[ 'POST', 'PUT' ])
# def …

# @app.route('/test/<tid>')
# def test3(tid):
# 	return "tid is %s" % tid

# @app.route('/test', defaults={'page': 'index'})
# @app.route('/test/<page>')
# def xxx(page):

# @app.route('/test', host='abc.com')
# @app.route('/test', redirect_to='/new_test')


# ==== Request Event Handler ====
# @app.before_first_request
# def …

# @app.before_request
# def …

# @app.after_request
# def …(response)
# 	return response

# @app.teardown_request
# def …(exception)


@app.route("/reqenv")
def reqenv():
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
            'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
            'PATH_INFO: %(PATH_INFO) s <br>'
            'QUERY_STRING: %(QUERY_STRING) s <br>'
            'SERVER_NAME: %(SERVER_NAME) s <br>'
            'SERVER_PORT: %(SERVER_PORT) s <br>'
            'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
            'wsgi.version: %(wsgi.version) s <br>'
            'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
            'wsgi.input: %(wsgi.input) s <br>'
            'wsgi.errors: %(wsgi.errors) s <br>'
            'wsgi.multithread: %(wsgi.multithread) s <br>'
            'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
            'wsgi.run_once: %(wsgi.run_once) s') % request.environ


# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)

    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)


@app.route("/rq")
def rq():
    # q = request.args.get("q")
    w = request.args.get("w")
    q = request.args.getlist("q")
    return "q = %s" % str(q)


# Response Objects (Cont'd) : WSGI
@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        header = [('Content-Type', 'text/plain'), ('Content-Length', str(len(body)))]
        start_response('200 OK', header)
        return [body]

    return make_response(application)


# Response Objects
@app.route("/res1")
def res1():
    custom_res = Response("custom response", 200, {'test': '1111'})
    return make_response(custom_res)


# web filter
@app.before_request
def before_request():
    print("before_request")
    g.str = "한글"
    g.str2 = "한글2"


# Global Object : g
@app.route("/")
def hello():
    return "Hello World " + getattr(g, 'str', '1111')


# @app.route("/")
# def hello():
#     return "Hello World!!!!!"


@app.route("/tmpl")
def t():
    tit = Markup("<strong>testTitle</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print(">>>>>", type(tit))

    lst = [("만남1", "김건모", True), ("만남2", "노사연", False), ("만남3", "이승기", False), ("만남4", "홍길동", False)]

    return render_template("index.html", title=tit, titie2=h, lst=lst)


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')

    print("email : %s" % email)
    print("passwd : %s" % passwd)

    return redirect('/')

    # u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
    # if u is not None:
    #     session['loginUser'] = { 'userid': u.id, 'name': u.nickname }
    #     if session.get('next'):
    #         next = session.get('next')
    #         del session['next']
    #         return redirect(next)
    #     return redirect('/')
    # else:
    #     flash("해당 사용자가 없습니다!!")
    #     return render_template("login.html", email=email)


if __name__ == "__main__":
    app.run(host='0.0.0.0')