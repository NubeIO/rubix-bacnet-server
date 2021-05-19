from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from src import db, AppSetting, create_app

setting: AppSetting = AppSetting().reload(AppSetting.default_setting_file)
app = create_app(setting)

migrate = Migrate(app, db, compare_type=True, render_as_batch=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
