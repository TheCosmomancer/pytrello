from peewee import *
db = SqliteDatabase('database.db')
import datetime
class User(Model):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    __password = CharField()
    department = CharField()
    @property
    def password (self):
        return self.__password
    @password.setter
    def password (self,password):
        self.__password = password
    class Meta:
        database = db
class Admin():
    def __init__(self):
        self.username = 'admin'
        self.__password = 'admin'
        self.__call_number = 'something' #no idea why this is even a thing
    @property
    def password(self):
        return self.__password
    @property
    def call_number(self):
        return self.__call_number
class Project(Model):
    name = CharField(unique=True)
    manager = ForeignKeyField(User, backref='projects')
    department = CharField()
    class Meta:
        database = db
class Task(Model):
    name = CharField(unique=True)
    created_date = DateTimeField()
    deadline = DateTimeField()
    status = CharField()
    description = CharField()
    project = ForeignKeyField(Project, backref='tasks')
    class Meta:
        database = db
class UserAndTasks(Model):
    user = ForeignKeyField(User, backref='tasks')
    task = ForeignKeyField(Task, backref='involved')
    class Meta:
        database = db
        indexes = (
            (('user', 'task'), True),
        )
class UserAndProjects(Model):
    user = ForeignKeyField(User, backref='projects')
    project = ForeignKeyField(Project, backref='involved')
    class Meta:
        database = db
        indexes = (
            (('user', 'project'), True),
        )

class Funcs():
    @staticmethod
    def getinp(stdscr, question = '',times = 0,space = True,inp =''):
        if times <= 0:
            while True:
                stdscr.clear()
                stdscr.addstr(question + '\n' + inp)
                stdscr.refresh()
                key = stdscr.getch()
                if key == 10:
                    break
                elif 33<= key <= 127 :
                    inp += chr(key)
                elif key == 263:
                    temp = ''
                    for i in range(len(inp)-1):
                        temp += inp[i]
                    inp = temp
                elif space == True and chr(key) == ' ':
                    inp += ' '
        else:
            for i in range(times):
                stdscr.clear()
                stdscr.addstr(question + '\n' + inp)
                stdscr.refresh()
                key = stdscr.getch()
                if 33<= key <= 127 or chr(key) == ' ':
                    inp += chr(key)
        return inp
    @staticmethod
    def selectProject(stdscr,user):
        validprojects = []
        for _ in list(UserAndProjects.select().where(UserAndProjects.user == user)):
            validprojects.append(_.project)
        for _ in list(Project.select().where(Project.department == user.department)):
            if _ not in validprojects:
                validprojects.append(_)
        if len(validprojects) == 0:
            return None
        else:
            current = 0
            while True:
                question = ''
                if current > 0 :
                    question += f'{validprojects[current-1].name}\n'
                question += f'>> {validprojects[current].name}\n'
                if current < len(validprojects) - 1:
                    question += f'{validprojects[current+1].name}\n'
                question += '[P] previous / [N] next / [C] confirm'
                key = Funcs.getinp(stdscr,question,1)
                if key == 'C' or key == 'c':
                    return validprojects[current]
                elif key == 'P' or key == 'p':
                    if current > 0:
                        current -= 1
                elif key == 'N' or key == 'n':
                    if current < len(validprojects)-1:
                        current += 1
    @staticmethod
    def selectTask(stdscr,user):#TODO add ordering and filtering
        vaildtasks = []
        for _ in list(UserAndTasks.select().where(UserAndTasks.user == user)):
            vaildtasks.append(_.task)
        for _ in list(Task.select()):
            if _ not in vaildtasks and _.project.department == user.department:
                vaildtasks.append(_)
        if len(vaildtasks) == 0:
            return None
        else:
            current = 0
            while True:
                question = ''
                if current > 0 :
                    question += f'{vaildtasks[current-1].name}\n'
                question += f'>> {vaildtasks[current].name}\n'
                if current < len(vaildtasks) - 1:
                    question += f'{vaildtasks[current+1].name}\n'
                question += '[P] previous / [N] next / [C] confirm'
                key = Funcs.getinp(stdscr,question,1)
                if key == 'C' or key == 'c':
                    return vaildtasks[current]
                elif key == 'P' or key == 'p':
                    if current > 0:
                        current -= 1
                elif key == 'N' or key == 'n':
                    if current < len(vaildtasks)-1:
                        current += 1
    @staticmethod
    def addProject(stdscr,user):
        name = Funcs.getinp(stdscr,'project name: ')
        department = Funcs.getinp(stdscr,'project department (press enter to use default): ')
        if user.username == 'admin':
            while True:
                owner = Funcs.getinp(stdscr,'project owner: ')
                try:
                    owner = User.get(User.username == owner)
                    break
                except:
                    pass
        else:
            owner = user
        if department == '':
            department = name
        try:
            project = Project.create(name=name,manager=owner,department=department)
            UserAndProjects.create(user=owner,project=project)
        except:
            pass
    @staticmethod
    def editProject(stdscr,user,project):
        while True:
            if user.username == 'admin' or project.manager.username == user.username:
                key = Funcs.getinp(stdscr,'[T] add task / [A] add user / [R] remove user / [N] change name / [C] change department / [D] delete project / [B] go back',1)
            else:
                key = key = Funcs.getinp(stdscr,'[T] add task / [B] go back',1)
            if key == 'T' or key == 't':
                try:
                    UserAndProjects.get(UserAndProjects.user == user)
                    name = Funcs.getinp(stdscr,'new task name: ')
                    created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    deadline = Funcs.getinp(stdscr,'task deadline (formated as YYYY-mm-dd HH:MM:SS): ')
                    date, time = deadline.split(' ')
                    date = date.split('-')
                    time = time.split(':')
                    for i in range(3):
                        date[i] = int(date[i])
                        time[i] = int(time[i])
                    deadline = datetime.datetime(date[0],date[1],date[2],time[0],time[1],time[2])
                    status = Funcs.getinp(stdscr,'task status: ')
                    description = Funcs.getinp(stdscr,'task description: ')
                    task = Task.create(name=name,created_date=created_date,deadline=deadline,status=status,description=description,project=project)
                    UserAndTasks.create(user=user,task=task)
                except:
                    pass
            if key == 'B' or key == 'b':
                break
            if user.username == 'admin' or project.manager.username == user.username:
                if key == 'A' or key == 'a':
                    inp = Funcs.getinp(stdscr,'username of user to add: ')
                    try:
                        inp = User.get(User.username == inp)
                        UserAndProjects.create(user=inp,project=project)
                    except:
                        pass
                elif key == 'R' or key == 'r':
                    inp = Funcs.getinp(stdscr,'username of user to delete: ')
                    try:
                        inp = User.get(User.username == inp)
                        target = UserAndProjects.get(user=inp,project=project)
                        target.delete_instance()
                    except:
                        pass
                elif key == 'N' or key == 'n':
                    try:
                        project.name = Funcs.getinp(stdscr,'new project name: ')
                        project.save()
                    except:
                        pass
                elif key == 'C' or key == 'c':
                    try:
                        project.department = Funcs.getinp(stdscr,'new project department: ')
                        project.save()
                    except:
                        pass
                elif key == 'D' or key == 'd':
                    while True :
                        key = Funcs.getinp(stdscr,f'delete project {project.name} ? [y/n]',1)
                        if key == 'Y' or key == 'y' or key == 'N' or key == 'n':
                            break
                    if key == 'Y' or key == 'y':
                        todelete = list(UserAndProjects.select().where(UserAndProjects.project == project))
                        for _ in todelete:
                            _.delete_instance()
                        project.delete_instance()
    @staticmethod
    def editTask(stdscr,task,user):
        while True:
            validusers = []
            for _ in list(UserAndTasks.select().where(UserAndTasks.task == task)):
                validusers.append(_.user)
            for _ in list(User.select()):
                if _ not in validusers and task.project.department == _.department:
                    validusers.append(_)
            if user.username == 'admin' or task.project.manager.username == user.username:
                key = Funcs.getinp(stdscr,'[N] name / [L] deadline / [S] status / [D] description / [P] project / [A] add user / [R] remove task / [B] back',1)
            elif user in validusers:
                key = Funcs.getinp(stdscr,'[N] name / [L] deadline / [S] status / [D] description / [A] add yourself / [B] back',1)
            else:
                key = Funcs.getinp(stdscr,'[B] back',1)
            if key == 'B' or key == 'b':
                break
            if user in validusers or user.username == 'admin':
                if key == 'N' or key == 'n':
                    task.name = Funcs.getinp(stdscr,'new name: ')
                elif key == 'L' or key == 'l':
                    task.name = Funcs.getinp(stdscr,'new deadline: ')
                elif key == 'S' or key == 's':
                    task.name = Funcs.getinp(stdscr,'new status: ')
                elif key == 'D' or key == 'd':
                    task.name = Funcs.getinp(stdscr,'new description: ')
                if user.username == 'admin' or task.project.manager.username == user.username:
                    if key == 'A' or key == 'a':
                        inp = Funcs.getinp(stdscr,'username of user to add: ')
                        try:
                            inp = User.get(User.username == inp)
                            UserAndTasks.create(user=inp,task=task)
                        except:
                            pass
                    elif key == 'R' or key == 'r':
                        while True :
                            key = Funcs.getinp(stdscr,f'delete project {task.name} ? [y/n]',1)
                            if key == 'Y' or key == 'y' or key == 'N' or key == 'n':
                                    break
                        if key == 'Y' or key == 'y':
                            todelete = list(UserAndTasks.select().where(UserAndTasks.task == task))
                            for _ in todelete:
                                _.delete_instance()
                        task.delete_instance()
                    elif key == 'P' or key == 'p':
                        task.project = Funcs.selectProject(stdscr,user)
                elif key == 'A' or key == 'a':
                    try:
                        UserAndProjects.create(user=user,task=task)
                    except:
                        pass
        # Task
        # me = CharField(unique=True)
        # created_date = DateTimeField()
        # deadline = DateTimeField()
        # status = CharField()
        # description = CharField()
        # project = ForeignKeyField(Proj