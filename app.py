#export FLASK_APP=app
#export FLASK_ENV=development
#export FLASK_DEBUG=1

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import markdown
from turbo_flask import Turbo

app = Flask(__name__)

app.config['SECRET_KEY'] = '6d985d0e326d9617e27dcb0da1758bc3b19a66f16d6c053f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskManager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

turbo = Turbo(app)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text)
#     status = db.Column(db.String, default="toDo")
# 
#     #def __init__(self, content):
#     #    self.content = content
#     #    self.status = "todo" 
# 
#     #def __repr__(self):
#     #    return '<Content %s>' % self.content


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    content_md = db.Column(db.Text, default=None)
    section = db.Column(db.Text, default="Miscellaneous")
    status = db.Column(db.String, default="toDo")
    priority = db.Column(db.String, default="cool")
    stuck = db.Column(db.String, default="off")
    type = db.Column(db.String, default="noType")
    #def __init__(self, content):
    #    self.content = content
    #    self.status = "todo"

    #def __repr__(self):
    #    return '<Content %s>' % self.content


db.create_all()

# INIT fake db
#-------------------------------------------------#
# task1 = Task(content='Update task status toDo > Progress > Done', section='My TODO APPLICATION', status='done')
# task2 = Task(content='Edit: try with pop up ?', section='My TODO APPLICATION', status='done')
# task3 = Task(content='Add task: With pop up as well ??', section='My TODO APPLICATION', status='done')
# task4 = Task(content='Implement ability to add section', section='My TODO APPLICATION', status='done')
# task5 = Task(content='Reload only turbo frame specific section for **add**/**edit-status**/**edit**/**delete**', section='My TODO APPLICATION', status='done')
# task6 = Task(content='Reduce sizing(bit too big)', section='My TODO APPLICATION', status='done')
# task7 = Task(content='**Reset form input ** when hitting cancel button or adding new task', section='My TODO APPLICATION', status='done')
# task8 = Task(content='Add markdown management', section='My TODO APPLICATION', status='done')
# task9 = Task(content='`app.config[SECRET_KEY] = ... ` ?', section='My TODO APPLICATION', status='done')
# task10 = Task(content='Format markdown !!!', section='My TODO APPLICATION', status='done')
# task11 = Task(content='**BUG ** - Adding new section mess up with the turbo frame...', section='My TODO APPLICATION', status='done')
# task12 = Task(content='**Improvement ** - Update dynamically `< datalist id = "sectionList" >` for *Add Task * button ([Soluce ?](https: // stackoverflow.com/questions/50141756/datalist-from-python-list) with ```@ app.route("/add-image", methods=["POST", ]) def add_image():     sequence += 1     html = render_template("_image.html", seq=sequence)      return turbo.stream([turbo.append(html, target="images"),         turbo.update(sequence, target="counter"), ])``` from [here](https: // eduardovra.github.io/building-two-sample-apps-using-hotwire-and-flask /))', section='My TODO APPLICATION', status='done')
# task13 = Task(content='**Improvement ** - Make `inputs` in *Add Task * form required with javascript: `IF[  # section or #task] is empty -> prevent close Add form ELSE close`', section='My TODO APPLICATION', status='done')
# task14 = Task(content='Add * priority * flag for tasks',section='My TODO APPLICATION', status='done')
# task15 = Task(content='**ADD ** - Flash message to notify when new section created on the right', section='My TODO APPLICATION', status='done')
# task16 = Task(content='** ADD ** - block code(Soluce - replace `input` by `textarea`)[markdown formatting](https://daringfireball.net/projects/markdown/syntax  # code)', section='My TODO APPLICATION', status='done')
# task17 = Task(content='Add login', section='My TODO APPLICATION', status='done')
# task18 = Task(content='Containerize with **Docker**', section='My TODO APPLICATION', status='done')
# task19 = Task(content='Deploy(**Heroku ** or other ???)', section='My TODO APPLICATION', status='done')
# task20 = Task(content='Integrate ** Mosaix**', section='Netcdf Editor App', status='done')
# task21 = Task(content='Debug ** mosaix ** branch local deployment', section='Netcdf Editor App', status='done')
# task22 = Task(content='Try a simple config for **PISCES OFFLINE**', section='PISCES', status='done')
# task23 = Task(content='**ADD** - task classification ???', section='My TODO APPLICATION', status='done')
# task24 = Task(content='**ADD** - implement sessions for users (???)', section='My TODO APPLICATION', status='done')

# db.session.add(task1)
# db.session.add(task2)
# db.session.add(task3)
# db.session.add(task4)
# db.session.add(task5)
# db.session.add(task6)
# db.session.add(task7)
# db.session.add(task8)
# db.session.add(task9)
# db.session.add(task10)
# db.session.add(task11)
# db.session.add(task12)
# db.session.add(task13)
# db.session.add(task14)
# db.session.add(task15)
# db.session.add(task16)
# db.session.add(task17)
# db.session.add(task18)
# db.session.add(task19)
# db.session.add(task20)
# db.session.add(task21)
# db.session.add(task22)
# db.session.add(task23)
# db.session.add(task24)
# db.session.commit()
#-------------------------------------------------#

status=["toDo","progress","done"]
priority=["cool","warm","hot"]
type=["noType", "addImprove", "bug", "genious"]
# addImprove
# <i class="fa-solid fa-plus"></i>
# <i class="fa-solid/regular fa-square-plus"></i>
# <i class="fa-solid fa-chart-line"></i>
# Bug
# <i class="fa-solid fa-bug"></i>
# genious
# <i class="fa-solid/regular fa-lightbulb"></i>

def getData():
    tasks = Task.query.all()
    # set var sections to get all the sections of tasks
    sections = []
    for task in tasks:
        sections.append(task.section)
    sections = list(dict.fromkeys(sections))
    # Display content in markdown
    for task in tasks:
        task.content_md = markdown.markdown(task.content)
    return sections, tasks

def renderElems():
    sections, tasks = getData()
    htmlSectionList = render_template("sectionList.html", sections=sections)
    htmlContent = render_template("content.html", sections=sections, tasks=tasks)
    return htmlSectionList, htmlContent


@app.route('/')
def taskManager():
    sections, tasks = getData()
    return render_template('taskManager.html', tasks=tasks, sections=sections)


@app.route('/add', methods=['POST'])
def add_task():
    content = request.form.get('content')
    section = request.form.get('section')
    task = Task(content=content, section=section)
    db.session.add(task)
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/update/<int:task_id>', methods=('POST',))
def update_task_status(task_id):
    task = Task.query.get(task_id)
    task.status = status[(status.index(task.status)+1) % 3] # update task status
    db.session.commit()
    
    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/priority/<int:task_id>', methods=('POST',))
def update_priority_status(task_id):
    task = Task.query.get(task_id)
    task.priority = priority[(priority.index(task.priority)+1) % 3]
    db.session.commit()
    
    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/stuck/<int:task_id>', methods=('POST',))
def update_stuck_status(task_id):
    task = Task.query.get(task_id)
    if task.stuck == "off":
        task.stuck = "on"
    elif task.stuck == "on":
        task.stuck = "off"
    db.session.commit()
    
    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/delete/<int:task_id>', methods=('POST',))
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])

#-------------------------EDIT SECTION - TO DO------------------------#
@app.route('/edit_section/<int:task_id>', methods=['POST'])
def edit_section(task_id):
    content = request.form.get('content')
    task = Task.query.get(task_id)
    task.content = content
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])
#--------------------------------------------------------------------#

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    content = request.form.get('content')
    task = Task.query.get(task_id)
    task.content = content
    db.session.commit()
    
    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])

@app.route('/doc/')
def doc():
    return render_template('doc.html')


@app.route('/about/')
def about():
    return render_template('about.html')
