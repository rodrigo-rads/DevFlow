from pathlib import Path

class TemplateGenerator:
    def __init__(self, templates_path: str = "templates"):
        self.templates_path = Path(templates_path)
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        if not self.templates_path.exists():
            self.templates_path.mkdir(parents=True, exist_ok=True)
        for template_file in self.templates_path.glob("*.txt"):
            self.templates[template_file.stem] = template_file.read_text(encoding="utf-8")

    def get_available_templates(self):
        return list(self.templates.keys())
    
    def generate_code(self, template_type: str, model_info:dict):
        if(template_type not in self.templates):
            raise Exception(f"Template '{template_type}' não foi encontrado")
        
        template = self.templates[template_type]
        
        class_name = model_info['class_name']
        namespace = model_info['namespace']
        
        service_var = class_name.lower() + 'Service'
        repository_var = class_name.lower() + 'Repository'
        items_var = class_name.lower() + 's'
        item_var = class_name.lower()
        table_name = class_name + 's'
        permission_name = class_name.upper()
        model_name = class_name + 'Model'
        id_model = 'ID_' + class_name.upper()

        return template.format(
            namespace=namespace,
            class_name=class_name,
            service_var=service_var,
            repository_var=repository_var,
            items_var=items_var,
            item_var=item_var,
            table_name=table_name,
            permission_name=permission_name,
            model_name = model_name,
            id_model = id_model
        )
    
