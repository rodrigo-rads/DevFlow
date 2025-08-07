import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import customtkinter as ctk

from core.model_parser import CSharpModelParser
from core.template_generator import TemplateGenerator
from config.config_manager import ConfigManager


class CSharpGeneratorGUI:
    def __init__(self):
        self.parser = CSharpModelParser()
        self.template_generator = TemplateGenerator()
        self.config_manager = ConfigManager()
        self.model_info = None


        # Tkinter Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("devPy")
        self.root.geometry("1280x720")
        self.root.minsize(600, 500)
        self.root.resizable(True, True)

        # Variáveis principais
        self.file_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=self.config_manager.get("last_output_dir", os.getcwd()))
        
        self.setup_ui()

    # -------------------------
    # UI Layout
    # -------------------------
    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.side_menu = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.side_menu.grid(row=0, column=0, sticky="nswe")
        self.side_menu.grid_rowconfigure(5, weight=1)

        title_label = ctk.CTkLabel(self.side_menu, text="devPy", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=20)

        self.btn_generator = ctk.CTkButton(self.side_menu, text="Gerador de MVC C#", anchor="w", command=lambda: self.show_page("generator"))
        self.btn_generator.pack(fill="x", pady=5, padx=10)

        self.btn_config = ctk.CTkButton(self.side_menu, text="Configurações", anchor="w", command=lambda: self.show_page("config"))
        self.btn_config.pack(fill="x", pady=5, padx=10)

        # Espaço e rodapé
        ctk.CTkLabel(self.side_menu, text="Versão 1.0", font=ctk.CTkFont(size=12)).pack(side="bottom", pady=10)

        # Área de conteúdo
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Criar as páginas
        self.page_generator = ctk.CTkFrame(self.content_frame)
        self.page_config = ctk.CTkFrame(self.content_frame)

        # Adicionar conteúdo de cada página
        self.setup_generator_tab(self.page_generator)
        self.setup_config_tab(self.page_config)

        # Mostrar página inicial
        self.show_page("generator")

        # Painel de log fixo (abaixo do conteúdo)
        log_container = ctk.CTkFrame(self.root)
        log_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        self.setup_log_section(log_container)

    def show_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

        if page_name == "generator":
            self.page_generator.grid(row=0, column=0, sticky="nsew")
        elif page_name == "config":
            self.page_config.grid(row=0, column=0, sticky="nsew")

    # -------------------------
    # Componentes UI
    # -------------------------
    def setup_file_selection(self, parent):
        file_frame = ctk.CTkFrame(parent)
        file_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(file_frame, text="Selecionar Model C#:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))

        input_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.file_entry = ctk.CTkEntry(input_frame, textvariable=self.file_path_var, placeholder_text="Caminho para o arquivo .cs do model...", height=35)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_button = ctk.CTkButton(input_frame, text="Procurar", command=self.browse_model_file, width=100, height=35)
        browse_button.pack(side="right")

    def setup_generator_tab(self, parent):
        scroll_frame = ctk.CTkScrollableFrame(parent, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(scroll_frame, text="Gerador de MVC C#", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 30))

        self.setup_file_selection(scroll_frame)
        self.setup_model_info(scroll_frame)
        self.setup_generation_options(scroll_frame)
        self.setup_output_section(scroll_frame)
        self.setup_action_buttons(scroll_frame)

    def setup_config_tab(self, parent):
        title = ctk.CTkLabel(parent, text="Configurações", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        ctk.CTkLabel(parent, text="Diretório padrão de saída:").pack(anchor="w", padx=20, pady=(10, 5))
        self.default_output_var = tk.StringVar(value=self.config_manager.get("last_output_dir", ""))

        frame_output = ctk.CTkFrame(parent, fg_color="transparent")
        frame_output.pack(fill="x", padx=20, pady=(0, 15))

        entry_output = ctk.CTkEntry(frame_output, textvariable=self.default_output_var, height=35)
        entry_output.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browser = ctk.CTkButton(frame_output, text="Procurar", width=100, command=self.browse_default_output)
        btn_browser.pack(side="right")

        save_btn = ctk.CTkButton(parent, text="Salvar", height=40, command=self.save_config)
        save_btn.pack(pady=30)

    def browse_default_output(self):
        folder = filedialog.askdirectory(title="Selecionar padrão de saída")
        if(folder):
            self.default_output_var.set(folder)

    def save_config(self):
        self.config_manager.set("last_output_dir", self.default_output_var.get())
        self.config_manager.save()
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
        
    def setup_model_info(self, parent):
        self.info_frame = ctk.CTkFrame(parent)
        self.info_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.info_frame, text="Informações do Model:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        self.class_label = ctk.CTkLabel(self.info_frame, text="Classe: -", anchor="w")
        self.class_label.pack(anchor="w", padx=20, pady=2)

        self.namespace_label = ctk.CTkLabel(self.info_frame, text="Namespace: -", anchor="w")
        self.namespace_label.pack(anchor="w", padx=20, pady=2)

        self.props_label = ctk.CTkLabel(self.info_frame, text="Propriedades: -", anchor="w")
        self.props_label.pack(anchor="w", padx=20, pady=(2, 15))

        self.info_frame.pack_forget()

    def setup_generation_options(self, parent):
        self.options_frame = ctk.CTkFrame(parent)
        self.options_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.options_frame, text="Arquivos para Gerar:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        row1_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 5))

        self.controller_var = tk.BooleanVar(value=True)
        self.service_var = tk.BooleanVar(value=True)
        self.repository_var = tk.BooleanVar(value=True)

        ctk.CTkCheckBox(row1_frame, text="Controller", variable=self.controller_var).pack(side="left", padx=(0, 20))
        ctk.CTkCheckBox(row1_frame, text="Service", variable=self.service_var).pack(side="left", padx=(0, 20))
        ctk.CTkCheckBox(row1_frame, text="Repository", variable=self.repository_var).pack(side="left", padx=(0, 20))

        row2_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        row2_frame.pack(fill="x")

        self.service_interface_var = tk.BooleanVar(value=True)
        self.repository_interface_var = tk.BooleanVar(value=True)

        ctk.CTkCheckBox(row2_frame, text="Service Interface", variable=self.service_interface_var).pack(side="left", padx=(0, 20))
        ctk.CTkCheckBox(row2_frame, text="Repository Interface", variable=self.repository_interface_var).pack(side="left", padx=(0, 20))

        self.options_frame.pack_forget()

    def setup_output_section(self, parent):
        self.output_frame = ctk.CTkFrame(parent)
        self.output_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.output_frame, text="Diretório de Saída:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))

        output_input_frame = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        output_input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.output_entry = ctk.CTkEntry(output_input_frame, textvariable=self.output_path_var, placeholder_text="Diretório onde os arquivos serão salvos...", height=35)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        output_browse_button = ctk.CTkButton(output_input_frame, text="Procurar", command=self.browse_output_folder, width=100, height=35)
        output_browse_button.pack(side="right")

        self.output_frame.pack_forget()

    def setup_action_buttons(self, parent):
        self.action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=20, pady=20)

        self.generate_button = ctk.CTkButton(self.action_frame, text="Gerar Arquivos", command=self.generate_files_threaded, height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.generate_button.pack(side="right", padx=(10, 0))

        clear_button = ctk.CTkButton(self.action_frame, text="Limpar", command=self.clear_all, height=40, fg_color="gray", hover_color="darkgray")
        clear_button.pack(side="right")

        self.action_frame.pack_forget()

    def setup_log_section(self, parent):
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        ctk.CTkLabel(log_frame, text="Log de Saída:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))

        self.log_text = ctk.CTkTextbox(log_frame, height=120)
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.log("Selecione um arquivo de model para começar.")

    # -------------------------
    # Ações
    # -------------------------
    def browse_model_file(self):
        file_path = filedialog.askopenfilename(title="Selecionar Model C#", filetypes=[("C# files", "*.cs")])
        if file_path:
            self.file_path_var.set(file_path)
            self.analyze_model_file(file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Selecionar Diretório de Saída")
        if folder_path:
            self.output_path_var.set(folder_path)
            self.config_manager.set("last_output_dir", folder_path)
            self.config_manager.save()

    def analyze_model_file(self, file_path: str):
        try:
            self.log(f"Analisando arquivo: {os.path.basename(file_path)}")
            self.model_info = self.parser.parse_model_file(file_path)

            self.class_label.configure(text=f"Classe: {self.model_info['class_name']}")
            self.namespace_label.configure(text=f"Namespace: {self.model_info['namespace']}")
            self.props_label.configure(text=f"Propriedades: {len(self.model_info['properties'])}")

            self.info_frame.pack(fill="x", padx=20, pady=10)
            self.options_frame.pack(fill="x", padx=20, pady=10)
            self.output_frame.pack(fill="x", padx=20, pady=10)
            self.action_frame.pack(fill="x", padx=20, pady=20)

            self.log("Model analisado com sucesso!")
        except Exception as e:
            self.log(f"Erro ao analisar model: {str(e)}")
            messagebox.showerror("Erro", str(e))

    def get_selected_types(self):
        selected = []
        if self.controller_var.get(): selected.append("controller")
        if self.service_var.get(): selected.append("service")
        if self.repository_var.get(): selected.append("repository")
        if self.service_interface_var.get(): selected.append("service_interface")
        if self.repository_interface_var.get(): selected.append("repository_interface")
        return selected

    def generate_files_threaded(self):
        if not self.model_info:
            messagebox.showwarning("Aviso", "Selecione um arquivo de model primeiro!")
            return

        selected_types = self.get_selected_types()
        if not selected_types:
            messagebox.showwarning("Aviso", "Selecione pelo menos um tipo de arquivo!")
            return

        self.generate_button.configure(state="disabled", text="Gerando...")
        thread = threading.Thread(target=self.generate_files_worker, args=(selected_types,))
        thread.daemon = True
        thread.start()

    def generate_files_worker(self, selected_types):
        try:
            output_dir = self.output_path_var.get()
            for file_type in selected_types:
                type_dir = Path(output_dir)
                type_dir.mkdir(parents=True, exist_ok=True)

                #Transformar em função para salvar os arquivos INomeArquivo
                #Pensar em como fazer para criar arquivos .cshtml
                filename = f"{self.model_info['class_name']}{file_type.capitalize()}.cs"
                file_path = type_dir / filename

                if file_type in self.template_generator.templates:
                    content = self.template_generator.generate_code(file_type, self.model_info)
                else:
                    content = f"// {file_type} gerado para {self.model_info['class_name']}"

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log(f"{file_path}")

            messagebox.showinfo("Sucesso", "Arquivos gerados com sucesso!")
        except Exception as e:
            self.log(f"Erro: {str(e)}")
        finally:
            self.generate_button.configure(state="normal", text="Gerar Arquivos")

    def clear_all(self):
        self.file_path_var.set("")
        self.output_path_var.set(self.config_manager.get("last_output_dir", os.getcwd()))
        self.model_info = None
        self.info_frame.pack_forget()
        self.options_frame.pack_forget()
        self.output_frame.pack_forget()
        self.action_frame.pack_forget()
        self.log_text.delete("0.0", "end")
        self.log("Interface limpa. Selecione um novo arquivo de model.")

    def log(self, message: str):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def run(self):
        self.root.mainloop()
