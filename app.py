#export FLASK_APP=app
#export FLASK_ENV=development
#export FLASK_DEBUG=1

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import markdown
from turbo_flask import Turbo
import datetime
from init_db_data import tasks_class_lst_raw


# import jinja2
# env = jinja2.Environment()
# env.globals.update(zip=zip)
# app.jinja_env.filters['zip'] = zip


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
    id             = db.Column(db.Integer  , primary_key=True)
    date           = db.Column(db.DateTime , default=datetime.datetime.now())
    section        = db.Column(db.Text     , default="Miscellaneous")
    order          = db.Column(db.Integer)
    header         = db.Column(db.Text)
    description    = db.Column(db.Text     , default=None)
    status         = db.Column(db.String   , default="toDo")
    priority       = db.Column(db.String   , default="cool")
    stuck          = db.Column(db.Boolean  , default=False)
    extended_view  = db.Column(db.Boolean  , default=False)
    
class Section(db.Model):
    id             = db.Column(db.Integer  , primary_key=True)
    order          = db.Column(db.Integer)
    header         = db.Column(db.Text)
    order_by       = db.Column(db.Boolean  , default=False) # [last added]/[older added]/[custom order]
    extended_view  = db.Column(db.Boolean  , default=False)

    # type_ = db.Column(db.String, default="noType_")
    #def __init__(self, content):
    #    self.content = content
    #    self.status = "todo"

    #def __repr__(self):
    #    return '<Content %s>' % self.content


RELAUNCH_DB = False

if RELAUNCH_DB:
    db.drop_all()
    db.create_all()

    # Initiate data for db
    #------------------------------------------#
    task_class_lst = []

    for task in tasks_class_lst_raw:
        task_class_lst.append(Task(header=task.header, section=task.section, status=task.status))

    for task in task_class_lst:
        db.session.add(task)

    db.session.commit()
    #------------------------------------------#

status=["toDo","progress","done"]
priority=["cool","warm","hot"]


def getData_bckp():
    tasks = Task.query.all()
    # set var sections to get all the sections of tasks
    sections = []
    for task in tasks:
        sections.append(task.section)
    sections = list(dict.fromkeys(sections))

    #------------TASK ORDER---------------------------
    # organize tasks list by task.order ????
    # https://www.geeksforgeeks.org/python-program-to-swap-two-elements-in-a-list/
    #------------TASK ORDER---------------------------

    # Display content in markdown
    for task in tasks:
        task.header_md = markdown.markdown(task.header)
    return sections, tasks

#----------------NEW STRUCTURE TEST TO REPLACE get_data()-------------------
def getData():

    # set var sections to get all the sections of all the tasks
    sections_raw = list(map(lambda x: x.section, Task.query.all()))
    sections = sorted(set(sections_raw), key=sections_raw.index)
    # sections = list(set(map(lambda x: x.section, Task.query.all())))

    tasks =[]
    for section in sections:
        task_per_section = Task.query.filter_by(section=section).all()
        task_per_section.sort(key = lambda x:x.order)
        #------------------IMPLEMENT ORDER TO TASKS--------------
        # ind = 1
        # for task in task_per_section:
        #     task.order = ind
        #     ind += 1


        # db.session.commit()
        #------------------IMPLEMENT ORDER TO TASKS--------------
        tasks.append(task_per_section)

    # WILL NEED TO BE REMOVED LATER WHEN all tasks in db will have their .content_md not empty
    #--------------------------
    # for tasks_per_section in tasks:
    #     for task in tasks_per_section:
    #         task.header_md = markdown.markdown(task.header)

    return sections, tasks
    #--------------------------

    #--------------------------
    # tasks is a list containing lists of tasks:

    # tasks = [ [task_1_section1, task_2_section1, ...],
    #           [task_1_section2, task_2_section2, ...],
    #           [task_1_section3, task_2_section3, ...] ]

    # Then give this to the html and display elements with someting like
    # {{ for list_task_per_section in tasks }}
    # OR TRY 
    # {{ for list_task_per_section, section in zip(tasks, section) }}
    #       <h2>{{ list_task_per_section[0].section }} </h2>
    #       {{ for task in list_task_per_section }}
    #--------------------------
#----------------NEW STRUCTURE TEST TO REPLACE get_data()-------------------


def renderElems():
    # Render specific elements of taskManager.html
    sections, tasks = getData()
    htmlSectionList = render_template("sectionList.html", sections=sections)
    htmlContent = render_template("content.html", sections=sections, tasks=tasks, zip=zip, md=markdown)
    return htmlSectionList, htmlContent


@app.route('/')
def taskManager():
    sections, tasks = getData()
    return render_template('taskManager.html', sections=sections, tasks=tasks, zip=zip, md=markdown)


@app.route('/add', methods=['POST'])
def add_task():
    header = request.form.get('header_in')
    section = request.form.get('section_in')
    #------------TASK ORDER---------------------------
    tasks = Task.query.filter_by(section=section).all()
    order = len(tasks)+1
    task = Task(section=section, date=datetime.datetime.now(), header=header, order=order) 
    # IF you want LOCAL time, install pytz
    # newYorkTz = pytz.timezone("America/New_York") 
    # timeInNewYork = datetime.now(newYorkTz)
    #------------TASK ORDER---------------------------
    # task = Task(section=section, date=datetime.datetime.now(), header=header)
    db.session.add(task)
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/status/<int:task_id>', methods=('POST',))
def update_status(task_id):
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
def update_priority(task_id):
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
def update_stuck(task_id):
    task = Task.query.get(task_id)
    if not task.stuck:
        task.stuck = True
    elif task.stuck:
        task.stuck = False
    db.session.commit()
    
    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/delete/<int:task_id>', methods=('POST',))
def delete_task(task_id):
    task_to_rm = Task.query.get(task_id)
    tasks_above = Task.query.filter(Task.section == task_to_rm.section, Task.order > task_to_rm.order).all()
    # tasks_above = Task.query.filter_by(section=section).update(dict(order=task_order + int(value)))
    for task in tasks_above:
        setattr(task, 'order', task.order-1)
    db.session.delete(task_to_rm)
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])


@app.route('/edit_section/<section_name>', methods=['POST'])
def edit_section(section_name):
    new_section_name = request.form.get('section_in')
    # tasks_filetered = Task.query.filter_by(section=section_name).all()
    Task.query.filter_by(section=section_name).update(dict(section=new_section_name))
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])

#------------------------------------------------------------


@app.route('/up/<task_section>/<int:task_order>/<value>', methods=('POST',))
def update_order(task_order, task_section, value):

    Task.query.filter_by(section=task_section, order=task_order).update(dict(order=9999))
    Task.query.filter_by(section=task_section, order=task_order + int(value)).update(dict(order=task_order))
    Task.query.filter_by(section=task_section, order=9999).update(dict(order=task_order + int(value)))
    db.session.commit()

    # task = Task.query.get(task_id)
    # Task.query.filter_by(section=task.section,  order=task.order-1).update(dict(order=task.order))
    # task.order -= 1
    # db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])
# Icons
# CARET ICON
# <i class="fa-solid fa-caret-up"></i>
# <i class="fa-solid fa-caret-down"></i>

# CHEVRON ICON
# <i class = "fa-solid fa-chevron-up" > </i >
# <i class="fa-solid fa-chevron-down"></i>

# ANGLE ICON
# <i class = "fa-solid fa-angle-up" > </i >
# <i class="fa-solid fa-angle-down"></i>
#------------------------------------------------------------


@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    header = request.form.get('header_in')
    task = Task.query.get(task_id)
    task.header = header
    task.header_md = markdown.markdown(header)
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
