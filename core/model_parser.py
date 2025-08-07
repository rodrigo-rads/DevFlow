import re

class CSharpModelParser:
    def parse_model_file(self, model_path: str):
        try:
            with open(model_path, 'r', encoding='utf-8') as file:
                content = file.read()

            namespace_match = re.search(r'namespace\s+([^\s{]+)', content)
            namespace = namespace_match.group(1) if namespace_match else "MyApp"

            class_match = re.search(r'public\s+class\s+(\w+)Model', content)
            if not class_match:
                raise Exception("Classe não encontrada no arquivo")
            
            class_name = class_match.group(1)

            property_pattern = r'public\s+(\w+(?:\?)?)\s+(\w+)\s*{\s*get;\s*set;\s*}'
            property_matches =  re.findall(property_pattern, content)
            properties = [{'name': p[1], 'type': p[0]} for p in property_matches]

            return {
                'file_path': model_path,
                'namespace': namespace,
                'class_name': class_name,
                'properties': properties,
                'file_content': content
            }
        except Exception as e:
            raise Exception(f"Erro ao ler o model: {e}")