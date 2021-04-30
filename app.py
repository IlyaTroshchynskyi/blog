from flask import Flask, redirect, url_for, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore # класс в котором хранятся все юзеры
from flask_security import Security, current_user


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)


migrate = Migrate(app, db) # выстраиавет корреляцию между приложением и базой данных
manager = Manager(app)
manager.add_command('db', MigrateCommand) #регистрируем команду для консоли когда будем делать миграцию

from myapp.models import Post, Tag, User, Role

class AdminMixin: # нужен чтоб не было копипаста
    def is_accessible(self):  # провеярет доступна ли вьюха пользователю тоесть шаблон. срабатывает автоматом
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):  # срабатывает если текущая вьюха не доступна пользователю
        return redirect(url_for('security.login', next=request.url))
 # next=request.url - определяет куда мы попадем когда залогинимся

class BaseModelView(ModelView): # нужен для правильно создания слогов через админ панель
    def on_model_change(self, form, model, is_created):
        # is_created - если тру то сформируй слаг
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)
# параметр next - определяет ту ссылку куда пользователь направлялся
class AdminView(AdminMixin, ModelView): # AdminMixin - идет первый потому что во 2 классе есть такие же методы а нам надо из 1
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
#index_view=HomeAdminView - говорит что при отображении начальной старницы будет эта вьюха учавствовать
admin.add_view(PostAdminView(Post, db.session)) # добавляем модели в админку чтоб их было видно из админки тоесть данные
admin.add_view(TagAdminView(Tag, db.session)) #db.session - занимается тем что вытягивает нам нужные данные

user_datastore = SQLAlchemyUserDatastore(db, User, Role) #SQLAlchemyUserDatastore(db, user_model, role_model)
security = Security(app, user_datastore) # подключаем фласк секурити  к нашему приложению


# user_datastore.create_role(name='admin', description='administrator')создагие роли в консоли
# user_datastore.add_role_to_user(user, role) = 'экземпляры классов юзер и роль. даем роль юзеру
# db.session.commit() - так завергшаем