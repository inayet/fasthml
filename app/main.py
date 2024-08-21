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
    live=true
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

@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir

@rt("/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = AX('edit', f'/edit/{self.id}', 'current-todo')
    dt = AX('✅ ' if self.done else '')

    cts = (dt, show, '|', edit, Hidden(id="id", value=self.id), Hidden(id="priority", value=0))

    return Li(*cts, id=f'todo-{self.id}')

@rt("/")
def get(auth):
    title = f"{auth}'s Todo List"
    top = Grid(H1(title), Div(A('logout', href='/logout'), sytle='text-align=right'))

    new_inp = Input(id="new-title", name="title", placeholder="New Todo") 
    add = Form(Group(new_inp, Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end")
    card = Card(Ul(frm), header=add, footer=Div(id='current-todo'))

    return Title(title), Container(top, card)

@rt("/reorder")
def post(id:list[int]):
    for i, id_ in enumerate(id): todos.update({'priority':i}, id_)
    return tuple(todos(order_by='priority'))

def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

serve()
