from settings import server, is_set
from os import listdir, remove
from os.path import join
from databank.dbast import convert_code
#from databank.fragment import in_fragment

catalog = []
cfgs = []

apps_fn = [f for f in listdir('collection') if f.endswith('.py') and f != '__init__.py']

comps_fn = [f for f in listdir(join('collection', 'compiled')) if f.endswith('.py') and f != '__init__.py']

for comp_fn in comps_fn:
    remove(join('collection', 'compiled', comp_fn))

for app_fn in apps_fn:
    if is_set('passive'):
        app_name = app_fn.split('.')[0]
        print(f'Loading {app_name} (passive)...', end=" ")
        app_module = __import__(f'collection.{app_name}', globals(), locals(), [app_name])
        app = app_module.__dict__[app_name]
        catalog.append(app)
        cfgs.append(None)
        print('ok!')
    else:
        app_name = app_fn.split('.')[0]
        print(f'Compiling {app_name + ".py"}...', end=" ")
        with open(join('collection', app_fn)) as f:
            code = f.read()
        converted_code, cfg = convert_code(code, app_name)
        with open(join('collection', 'compiled', app_name + '.py'), 'w') as g:
            g.write(converted_code)
        print('ok!')
        print(f'Loading {app_name}...', end=" ")
        app_module = __import__(f'collection.compiled.{app_name}', globals(), locals(), [app_name])
        app = app_module.__dict__[app_name]
        cfgs.append(cfg)
        catalog.append(app)
        print('ok!')

server.start()

def user_catalog(u):
    my_catalog = []
    for app, cfg in zip(catalog, cfgs):
#        if is_set('passive') or in_fragment(u, cfg):
        my_catalog.append(app)
    return my_catalog
