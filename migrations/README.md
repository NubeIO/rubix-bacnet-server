### Commands

1. Initializes migration support for the application (only for the first time):
   > python manage.py db init

2. Create migration script of schema change (The generated script should to be reviewed and edited as not all types of
   changes can be detected automatically. [For more details](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)):
   > python manage.py db migrate

3. Create empty migration script:
   > python manage.py db revision

4. Apply the latest migration to the DB:
   > python manage.py db upgrade

5. Apply the specific revision migration to the DB:
   > python manage.py db upgrade `<revision>`

6. Revert the single migration to the DB:
   > python manage.py db downgrade

7. Revert the specific revision migration to the DB:
   > python manage.py db downgrade `<revision>`

8. Migration command-line help:
   > python manage.py db --help

#### [For more details](https://flask-migrate.readthedocs.io/en/latest/)


### Generated script should be edited to:

1. Rename a table:
   ```bash
   def upgrade():
    op.rename_table('old_table_name', 'new_table_name')

   def downgrade():
    op.rename_table('new_table_name', 'old_table_name')
   ```

2. Rename a table having relationship:
   ```bash
   naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
   }
   def upgrade():
    op.rename_table('old_table_name', 'new_table_name')
    with op.batch_alter_table('referred_table_name', schema=None, naming_convention= naming_convention) as batch_op:
      batch_op.drop_constraint('old_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('new_constraint_name', 'source_table_name',
                                ['local_cols'], ['remote_cols'])

   def downgrade():
    op.rename_table('new_table_name', 'old_table_name')
    with op.batch_alter_table('referred_table_name', schema=None, naming_convention= naming_convention) as batch_op:
      batch_op.drop_constraint('new_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('old_constraint_name', 'source_table_name',
                                ['local_cols'], ['remote_cols'])
   ```

3. Rename a column:
   ```bash
   def upgrade():
    batch_op.alter_column('old_column_name', new_column_name='new_column_name')


   def downgrade():
    batch_op.alter_column('new_column_name', new_column_name='old_column_name')
   ```

4. Rename primary key column having relationship:
   ```bash
   naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
   }

   def upgrade():
    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.alter_column('old_column_name', new_column_name='new_column_name')

    with op.batch_alter_table('referred_table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.drop_constraint('old_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('new_constraint_name', 'source_table_name', ['local_cols']
                                    , ['remote_cols'])
   def downgrade():
    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.alter_column('new_column_name', new_column_name='old_column_name')

    with op.batch_alter_table('referred_table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.drop_constraint('new_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('old_constraint_name', 'source_table_name', ['local_cols']
                                    , ['remote_cols'])
   ```

5. Rename a foreign key column:
   ```bash
   naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
   }

   def upgrade():
    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.alter_column('old_column_name', new_column_name='new_column_name')

    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.drop_constraint('old_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('new_constraint_name', 'source_table_name',
                                    ['local_cols'], ['remote_cols'])
   def downgrade():
    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.alter_column('new_column_name', new_column_name='old_column_name')

    with op.batch_alter_table('table_name', schema=None, naming_convention=naming_convention) as batch_op:
      batch_op.drop_constraint('new_constraint_name', type_='foreignkey')
      batch_op.create_foreign_key('old_constraint_name', 'source_table_name',
                                    ['local_cols'], ['remote_cols'])
   ```

6. To make batch migration works for inheritance (or when altering (drop & transform in real) table shows error)

- Include below block at first, which turns off foreign key

    ```bash
    session = Session(bind=op.get_bind())
    session.execute('PRAGMA foreign_keys = OFF;')
    session.commit()
    ```

#### [For more details](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations)
