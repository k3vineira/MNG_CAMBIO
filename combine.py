import os
import ast

excluded_models = {
    'Usuario', 'Temporada', 'Categoria', 'Actividades', 'Paquete', 
    'Tarifa', 'PaqueteActividad', 'Blog', 'PQRS', 'Seguimiento', 'Reserva'
}

project_dirs = [
    'auditoria', 'autenticacion', 'catalogo', 'comunidad', 
    'guias', 'IA', 'pagos', 'promociones', 'reservas', 'seguros', 'usuarios'
]

combined_code = []

def add_id_field(class_node):
    for node in class_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'id':
                    return
    
    id_assign = ast.Assign(
        targets=[ast.Name(id='id', ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='models', ctx=ast.Load()),
                attr='AutoField',
                ctx=ast.Load()
            ),
            args=[],
            keywords=[ast.keyword(arg='primary_key', value=ast.Constant(value=True))]
        )
    )
    
    if (len(class_node.body) > 0 and 
        isinstance(class_node.body[0], ast.Expr) and 
        isinstance(class_node.body[0].value, ast.Constant) and 
        isinstance(class_node.body[0].value.value, str)):
        class_node.body.insert(1, id_assign)
    else:
        class_node.body.insert(0, id_assign)


for d in project_dirs:
    model_path = os.path.join(d, 'models.py')
    if os.path.exists(model_path):
        with open(model_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        try:
            tree = ast.parse(source)
            filtered_body = []
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    if node.name in excluded_models:
                        continue
                    add_id_field(node)
                filtered_body.append(node)
            
            tree.body = filtered_body
            ast.fix_missing_locations(tree)
            
            app_name = d.upper()
            header = f"# {'='*78}\n# {app_name}\n# {'='*78}"
            combined_code.append(header)
            combined_code.append(ast.unparse(tree))
            combined_code.append('\n')
        except Exception as e:
            print(f'Error parsing {model_path}: {e}')

with open('modelos_combinados.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(combined_code))

print('Done. Saved to modelos_combinados.py')
