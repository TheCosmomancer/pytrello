from os import truncate
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
class Project(Model):
    name = CharField(unique=True)
    manager = ForeignKeyField(User, backref='projects')
    department = CharField()
    class Meta:
        database = db
class Task(Model):
    name = CharField(unique=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    deadline = DateTimeField()
    status = CharField()
    description = CharField()
    project = ForeignKeyField(Project, backref='tasks')
    class Meta:
        database = db
class UserAndTasks(Model):
    user = ForeignKeyField(User, backref='tasks')
    task = ForeignKeyField(User, backref='involved')
    class Meta:
        database = db
        indexes = (
            (('user', 'task'), True),
        )
class UserAndProjects(Model):
    user = ForeignKeyField(User, backref='projects')
    project = ForeignKeyField(User, backref='involved')
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
        for _ in UserAndProjects.select():
            if _.user == user:
                validprojects.append(_.name)
        if len(validprojects) == 0:
            return None
        else:
            current = 0
            while True:
                key = Funcs.getinp(stdscr,f'{validprojects[current]}\n[P] previous / [N] next / [C] confirm',1)
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
        for _ in UserAndTasks.select():
            if _.user == user:
                vaildtasks.append(_.name)
        if len(vaildtasks) == 0:
            return None
        else:
            current = 0
            while True:
                key = Funcs.getinp(stdscr,f'{vaildtasks[current]}\n[P] previous / [N] next / [C] confirm',1)
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
        name = Funcs.getinp(stdscr,'project name :')
        department = Funcs.getinp(stdscr,'project department (press enter to use default) :')
        if user.username == 'admin':
            while True:
                owner = Funcs.getinp(stdscr,'project owner :')
                try:
                    owner = User.get(User.username == owner)
                    break
                except:
                    pass
        else:
            owner = user
        if department == '':
            department = name
        project = Project.create(name=name,manager=owner,department=department)
        UserAndProjects.create(user=owner,project=project)
    @staticmethod
    def editProject(stdscr,user,project):
        while True:
            key = Funcs.getinp(stdscr,'[T] add task / [A] add user / [R] remove user / [N] change name / [C] change department / [D] delete project',1)
            if key == 'T' or key == 't':
                try:
                    UserAndProjects.get(UserAndProjects.user == user)
                    name = Funcs.getinp(stdscr,'new task name :')
                    created_date = Funcs.getinp(stdscr,'creation date :')
                    deadline = Funcs.getinp(stdscr,'task deadline :')
                    status = Funcs.getinp(stdscr,'project status :')
                    description = Funcs.getinp(stdscr,'project description :')
                    task = Task.create(name=name,created_date=created_date,deadline=deadline,status=status,description=description,project=project)
                    UserAndTasks.create(user=user,task=task)
                except:
                    pass
            elif user.username == 'admin' or project.manager == user.username:
                if key == 'A' or key == 'a':
                    inp = Funcs.getinp(stdscr,'username of user to add :')
                    try:
                        inp = User.get(User.username == inp)
                        UserAndProjects.create(user=inp,project=project)
                    except:
                        pass
                elif key == 'R' or key == 'r':
                    inp = Funcs.getinp(stdscr,'username of user to delete :')
                    try:
                        inp = User.get(User.username == inp)
                        target = UserAndProjects.get(inp,project)
                        target.delete_instance()
                    except:
                        pass
                elif key == 'N' or key == 'n':
                    try:
                        project.name = Funcs.getinp(stdscr,'new project name :')
                        project.save()
                    except:
                        pass
                elif key == 'C' or key == 'C':
                    try:
                        project.department = Funcs.getinp(stdscr,'new project department :')
                        project.save()
                    except:
                        pass
                elif key == 'D' or key == 'd':
                    while True :
                        key = Funcs.getinp(stdscr,f'delete project {project.name} ? [y/n]',1)
                        if key == 'Y' or key == 'y' or key == 'N' or key == 'n':
                            break
                    if key == 'Y' or key == 'y':
                        #TODO remove all instances of UserAndProject
                        project.delete_instance()
    @staticmethod
    def editTask():
        ...
    @staticmethod
    def deletTask():
        ...