from fasthtml.common import *

from hmac import compare_digest

db = database("data/utodos.db")
todos, users = db.t.todos, db.t.users
if todos not in db.t:

    users.create(dict(name=str, pwd=str), pk="name")
    todos.create(
        id=int, title=str, done=bool, name=str, details=str, priority=int, pk="id"
    )

Todo, User = todos.dataclass(), users.dataclass()

login_redir = RedirectResponse("/login", status_code=303)


def before(req, sess):

    auth = req.scope["auth"] = sess.get("auth", None)

    if not auth:
        return login_redir

    todos.xtra(name=auth)


markdown_js = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { proc_htmx} from "https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
"""


def _not_found(req, exc):
    return Titled("VIN Decorder App", Div("we could not find page"))


bware = Beforeware(before, skip=[r"/favicon\.ico", r"/static/.*", r".*\.css", "/login"])

app = FastHTML(
    before=bware,
    exception_handlers={404: _not_found},
    hdrs=(
        picolink,
        Style(":root { --pico-font-size: 100%}"),
        SortableJS(".sortable"),
        Script(markdown_js, type="module"),
    ),
)
# db.execute('DROP TABLE users')

rt = app.route


@rt("/login")
def get():
    frm = Form(
        Input(id="name", placeholder="Name"),
        Input(id="pwd", type="password", placeholder="Password"),
        Button("login"),
        action="/login",
        method="post",
    )
    return Titled("Login", frm)


@dataclass
class Login:
    name: str
    pwd: str


@rt("/login")
def post(login: Login, sess):
    if not login.name or not login.pwd:
        return login_redir

    try:
        u = users[login.name]

    except NotFoundError:
        u = users.insert(login)

    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")):
        return login_redir

    sess["auth"] = u.name

    return RedirectResponse("/", status_code=303)

    #


# @rt('/')
# def get(): return Div(P('Hello World!'), hx_get="/change")
#
serve()
