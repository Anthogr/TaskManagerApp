#export FLASK_APP=app
#export FLASK_ENV=development
#export FLASK_DEBUG=1

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
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
    # type_ = db.Column(db.String, default="noType_")
    #def __init__(self, content):
    #    self.content = content
    #    self.status = "todo"

    #def __repr__(self):
    #    return '<Content %s>' % self.content


db.create_all()

# INIT fake db
#-------------------------------------------------#
# task1  = Task(content='Update task status toDo > Progress > Done', section='My TODO APPLICATION', status='done')
# task2  = Task(content='Edit: try with pop up ?', section='My TODO APPLICATION', status='done')
# task3  = Task(content='Add task: With pop up as well', section='My TODO APPLICATION', status='done')
# task4  = Task(content='Reload only turbo frame specific section for **add**/**edit-status**/**edit**/**delete**', section='My TODO APPLICATION', status='done')
# task5  = Task(content='Reduce sizing(bit too big)', section='My TODO APPLICATION', status='done')
# task6  = Task(content='**Reset form input ** when hitting cancel button or adding new task', section='My TODO APPLICATION', status='done')
# task7  = Task(content='Add markdown management', section='My TODO APPLICATION', status='done')
# task8  = Task(content='`app.config[SECRET_KEY] = ... ` ?', section='My TODO APPLICATION', status='done')
# task9  = Task(content='Format markdown !!!', section='My TODO APPLICATION', status='done')
# task10 = Task(content='**BUG ** - Adding new section mess up with the turbo frame...', section='My TODO APPLICATION', status='done')
# task11 = Task(content='**Improvement ** - Update dynamically `< datalist id = "sectionList" >` for *Add Task * button ([Soluce ?](https: // stackoverflow.com/questions/50141756/datalist-from-python-list) with ```@ app.route("/add-image", methods=["POST", ]) def add_image():     sequence += 1     html = render_template("_image.html", seq=sequence)      return turbo.stream([turbo.append(html, target="images"),         turbo.update(sequence, target="counter"), ])``` from [here](https: // eduardovra.github.io/building-two-sample-apps-using-hotwire-and-flask /))', section='My TODO APPLICATION', status='done')
# task12 = Task(content='**Improvement ** - Make `inputs` in *Add Task* form required with javascript: `IF[  # section or #task] is empty -> prevent close Add form ELSE close`', section='My TODO APPLICATION', status='done')
# task13 = Task(content='Add * priority * flag for tasks', section='My TODO APPLICATION', status='done')
# task14 = Task(content='**ADD ** - Flash message to notify when new section created on the right', section='My TODO APPLICATION', status='toDo')
# task15 = Task(content='** ADD ** - block code for task entry to allow more flexibility (Soluce - replace `input` by `textarea`) [markdown formatting](https://daringfireball.net/projects/markdown/syntax  # code)', section='My TODO APPLICATION', status='toDo')
# task16 = Task(content='Deploy(**Heroku ** or other ???)', section='My TODO APPLICATION', status='toDo')
# task17 = Task(content='**v1** - Ability to create session with login + containerize with Docker + get real-time changes between several clients connected to the same session', section='My TODO APPLICATION', status='progress')
# task18 = Task(content='**v2** - Implement multiple users per session', section='My TODO APPLICATION', status='toDo')
# task19 = Task(content='**v3** - Messaging service for each task allowing users to discuss + user be attributed to tasks -  **CANCELLED ???**', section='My TODO APPLICATION', status='toDo')
# task20 = Task(content='**ADD** - Button at the end of each section to add task faster + *add task* button becomes *add section* => implement to ability to add section independently from tasks - **MAYBE NOT !!!** Cumbersome... Just add task at top remains add task with ability to *choose/create* new section and add button add task at bottom of each section to add task in that relative section', section='My TODO APPLICATION', status='progress')
# task21 = Task(content='**ADD** - Drag and drop list order (source [here](https://tutorial101.blogspot.com/2021/01/python-flask-dynamic-drag-and-drop.html) and [here](https://www.geeksforgeeks.org/how-to-create-a-drag-and-drop-feature-for-reordering-the-images-using-html-css-and-jqueryui/))', section='My TODO APPLICATION', status='toDo')
# task22 = Task(content='**ADD** - Make nav_bar + new task button stay on top of screen when scrolling down', section='My TODO APPLICATION', status='toDo')
# task23 = Task(content='**ADD** - Ability to rename section', section='My TODO APPLICATION', status='progress')
# task24 = Task(content='**ADD** - ability to handle variable number of sub basins (Jean-Baptiste) ', section='Diag_CM5A2', status='toDo')
# task25 = Task(content='**IMPROVEMENT** - Change structure: task name + task description', section='My TODO APPLICATION', status='progress')
# task26 = Task(content='**CREATE** - Store source code on **GitHub** (list all implementations of JB and Marie)', section='PISCES OFFLINE', status='progress')
# task27 = Task(content='**ADD** - Ability to change section or task order', section='My TODO APPLICATION', status='toDo')
# task28 = Task(content='**CHECK** - See if the JB/MARIE workflow for *adapting concentrations* and *damping* are "mandatory". [**Not very important for now**]', section='PISCES OFFLINE', status='done')
# task29 = Task(content='**Routing** - Comprendre les I/O de Wesley et comparer aux scripts de JB en f90', section='Netcdf_Editor_App', status='done')
# task30 = Task(content='**ADD** - Take in account integration of var *siconc* and *wocetr_eff* in with script `UpdateVariable.ksh`', section='PISCES OFFLINE', status='done')
# task31 = Task(content='**BUG** - At *Regrid* step, if input file has *coordinate* name different from *dim* name => `ERROR` (can be solved but not done because not supposed to be an issue)', section='Netcdf_Editor_App', status='toDo')
# task32 = Task(content='**MOSAIX** - Fix version with revision no *6245*', section='Netcdf_Editor_App', status='done')
# task33 = Task(content='**ADD** - Add Archive system (add entry in database `archive = True/False`) main page displays database entry with `archive = False` and New page named *Archive* displays database database entry with `archive = True`. Add archive button at section level close to *rename section name*', section='My TODO APPLICATION', status='toDo')
# task34 = Task(content='**REDESIGN** (**v3**) - Change display structure. *Sections* are displayed in a column table on left and selecting a section in this table display the *section table* with its tasks on the right. It will make de display cleaner (only 1 *section table* displayed at a time) + For each section on the *Section table* on the left colored patches showing nb of tasks no started, nb in progress and number done ! ![](static/images/Redesign_app.png)', section='My TODO APPLICATION', status='toDo')
# task35 = Task(content='**Add** - Ability to add figure from local computer ???', section='My TODO APPLICATION', status='toDo')
# task36 = Task(content='**BUG** - Code is not working anymore neither on frontal nor on calculation node - Try to make working at least `configure_paleo_pisces.py` and `init_paleo_pisces.py` and then maybe check for installing and compiling PISCES on *gen2212* and then replace `Install_paleo_pisces.py` by a simple script copying pisces installed on *gen2212* on user work space -', section='PISCES OFFLINE', status='done')
# task37 = Task(content='**configure_paleo_pisces.py** on *FRONTALE* - Bug when executing `./UpdateVariable_sic.ksh`: `ncks` and `ncrename` commands not found. Solving -> `ml load nco/4.9.2`', section='PISCES OFFLINE', status='done')
# task38 = Task(content='**configure_paleo_pisces.py** on *FRONTALE* - New bug at *Compiling weight tool...* step', section='PISCES OFFLINE', status='done')
# task39 = Task(content='**install_paleo_pisces.py** on *FRONTALE* - Bug when compiling *XIOS* -> `Loading mpi/openmpi/2.0.4 ERROR: cant read "errorCode": no such variable`. Solving -> in `/ccc/work/cont003/gen2212/gramoula/[PALEOPISCES_FOLDER]/modipsl/modeles/XIOS/arch/arch-X64_IRENE.env` replace *module load mpi/openmpi/2.0.4* by *module load mpi/openmpi/4.1.4* **FALSE !!!** - It doesnt solve issue... **SOLVE** - Use Stock IRENE env (no ml load in bashrc) OR use IPSL env !!! -> [here](https://forge.ipsl.jussieu.fr/igcmg_doc/wiki/Doc/ComputingCenters/TGCC/Irene#Generalenvironment)', section='PISCES OFFLINE', status='done')
# task40 = Task(content='**TIPS** - Modules conseillés avec `python3/3.8.10` : ` intel/20` et `mpi/openmpi/4.1.4`', section='PISCES OFFLINE', status='done')
# task41 = Task(content='**FIX** - Concernant linstallation/compilation du modèle : voir ce qui peut être effectué en amont au maximum (`install_paleo_pisces.py` et peut être une partie de `configure_paleo_pisces.py`)', section='PISCES OFFLINE', status='done')
# task42 = Task(content='**install_paleo_pisces.py** - Bug at *Compile NEMO* step. Ive checked the `modipsl/modeles/NEMOGCM/CONFIG/ORCA2_OFF_PISCES/cpp_ORCA2_OFF_PISCES.fcm` file after svn (It might have changed on svn repo) but no modifications made (Just need to add key_xios2 as mentioned in Maries doc)', section='PISCES OFFLINE', status='done')
# task43 = Task(content='**TIPS ** - Pour installer/compiler * NEMO * sur * IRENE * dans le terminal sans passer par `install_paleo_pisces.py` regarder début du script `pisces_modules/process.py`: les commandes bash y sont indiquées', section='PISCES OFFLINE', status='done')
# task44 = Task(content='**BUG ** - Build of MOSAIX docker image failed on Github', section='Netcdf_Editor_App', status='done')
# task45 = Task(content='**NEXT STEP ** - Scripts are running correctly. Next step is to check no error occurs during model run ! (doc has been updated for changes mades related to environment to load)', section='PISCES OFFLINE', status='done')
# task46 = Task(content='**UPDATE ** - Documentation separate loading env and running script(*RUN_Diag.sh * becomes * load_env.sh*) then use command `python3 Diag_CM5A2.py`', section='Diag_CM5A2', status='done')
# task47 = Task(content='**UPDATE ** - Code seems to work on frontale with *python 3.8.10 * (maybe test with *python 3.7.5 * as well). If it works, update doc if necessary - **UPDATE ** - Doesnt work with *python 3.8.10*. Used * Python 3.7.5 * instead.', section='Diag_CM5A2', status='progress')
# task48 = Task(content='**GITHUB ** - Clean local repository by keeping one version', section='PISCES OFFLINE', status='progress')
# task49 = Task(content='**ADD ** -  Ability to clone a workflow. With this, we can use a paleogeography generate all files and if we want to modify Bathy for example, we can duplicate workflow and modify it and original workflow is not modified(Request Yannick)', section='Netcdf_Editor_App', status='toDo')
# task50 = Task(content='**BUG ** - At * Passage Problem * step when saving sometime, *ahmcoef * data is saved in *heatflow * file and sometime it is reversed. **SOLVING ** - Add a `db.execute("BEGIN IMMEDIATE")` in `db.py` in function `save_file_to_db` *????*', section='Netcdf_Editor_App', status='done')




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
# db.session.add(task25)
# db.session.add(task26)
# db.session.add(task27)
# db.session.add(task28)
# db.session.add(task29)
# db.session.add(task30)
# db.session.add(task31)
# db.session.add(task32)
# db.session.add(task33)
# db.session.add(task34)
# db.session.add(task35)
# db.session.add(task36)
# db.session.add(task37)
# db.session.add(task38)
# db.session.add(task39)
# db.session.add(task40)
# db.session.add(task41)
# db.session.add(task42)
# db.session.add(task43)
# db.session.add(task44)
# db.session.add(task45)
# db.session.add(task46)
# db.session.add(task47)
# db.session.add(task48)
# db.session.add(task49)
# db.session.add(task50)
# db.session.commit()
#-------------------------------------------------#

status=["toDo","progress","done"]
priority=["cool","warm","hot"]
# type_=["noType", "addImprove", "bug", "genious"]
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


@app.route('/edit_section/<section_name>', methods=['POST'])
def edit_section(section_name):
    new_section_name = request.form.get('content')
    # tasks_filetered = Task.query.filter_by(section=section_name).all()
    Task.query.filter_by(section=section_name).update(dict(section=new_section_name))
    db.session.commit()

    # Update only specific parts of main html page
    htmlSectionList, htmlContent = renderElems()
    return turbo.stream([
        turbo.update(htmlSectionList, target="sectionList"),
        turbo.update(htmlContent, target="flex-row")
    ])

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
