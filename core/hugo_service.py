import subprocess
import webbrowser
import platform


from PySide6.QtCore import QProcess


from core.themes import THEMES
from pathlib import Path



DEBUG_HUGO_OUTPUT = False


class HugoService:
    def __init__(self, main_window):
        self.main_window = main_window
        self.server_process = QProcess(main_window)
        
        # Hugo server state
        self.server_project = None
        self.pending_project = None
        self.server_running = False
     
        self.server_url = "http://localhost:1313"
        
        self.server_process.readyReadStandardOutput.connect(
        self.process_output
        )

        self.server_process.readyReadStandardError.connect(
        self.process_output
        )
        
        self.server_process.finished.connect(self.server_stopped)

    def preview(self, project):

        if project is None:
            return
            
        if (
            self.server_process.state() != QProcess.NotRunning
            and self.server_project != project
        ):
            self.stop_server()

        if self.server_process.state() == QProcess.NotRunning:

            self.server_process.setWorkingDirectory(str(project))
            
            self.pending_project = project
            
            
            self.server_process.start(
                "hugo",
                [
                    "server",
                    "--disableFastRender",
                ],
            )

            self.main_window.write("Starting Hugo server...")

        

        else:

            if self.server_project == project:

                webbrowser.open(self.server_url)
                self.main_window.write("Opened browser.")

    def build(self, project):

        if project is None:
            return

        subprocess.run(
            ["hugo"],
            cwd=project,
        )

        self.main_window.write("Build complete.")
        
    def new_project(self, parent_folder, name):
        result = subprocess.run(
            ["hugo", "new", "site", name],
            cwd=parent_folder,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.main_window.write(result.stderr)
            return False
            
        project_path = Path(parent_folder) / name
      
        
        git = subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )

        if git.returncode != 0:
            self.main_window.write(git.stderr)
            return False

        self.main_window.write(f"Created project: {name}")
        return True
        
    def install_theme(self, project, theme):

        if project is None:

            self.main_window.write("No project is open.")
            return

        self.main_window.write(f"Installing theme: {theme}")
    


        repo = THEMES[theme]["repo"]
        self.main_window.write(f"Repository: {repo}")

        
        result = subprocess.run(
            [
                "git",
                "clone",
                repo,
                f"themes/{theme}",
            ],
            cwd=project,
            capture_output=True,
            text=True,
        )

        self.main_window.write("Theme installation finished.")
        
    def process_output(self):

        text = bytes(
            self.server_process.readAllStandardOutput()
        ).decode(errors="ignore")
        
        if "ERROR" in text:

            self.server_project = None
            self.server_running = False
            self.main_window.write("Preview failed.")
            return

        if not text:
            text = bytes(
                self.server_process.readAllStandardError()
            ).decode(errors="ignore")

        if text:
            self.main_window.write(text.strip())

        if DEBUG_HUGO_OUTPUT:
            self.main_window.write(text.strip())
        
        if "Web Server is available at" in text:

            if not self.server_running:

                self.server_project = self.pending_project
                self.pending_project = None
                self.server_running = True

                self.main_window.write("Hugo server is ready.")
                webbrowser.open(self.server_url)
                
    def server_stopped(self):

        self.server_running = False
        self.server_project = None
        self.pending_project = None

        self.main_window.write("Hugo server stopped.")
        
    def stop_server(self):

        if self.server_process.state() == QProcess.NotRunning:
            return

        self.server_process.kill()
        self.server_process.waitForFinished()

        self.server_running = False
        self.server_project = None
        self.pending_project = None
        
    def run_command(self, command):

        if not self.main_window.project:
            return

        self.main_window.write(f"> {command}")

        self.command_process = QProcess(self.main_window)

        self.command_process.setWorkingDirectory(
            str(self.main_window.project)
        )

        self.command_process.readyReadStandardOutput.connect(
            lambda: self.main_window.write(
                bytes(
                    self.command_process.readAllStandardOutput()
                ).decode(errors="ignore")
            )
        )

        self.command_process.readyReadStandardError.connect(
            lambda: self.main_window.write(
                bytes(
                    self.command_process.readAllStandardError()
                ).decode(errors="ignore")
            )
        )

        if platform.system() == "Windows":
            self.command_process.start("cmd", ["/c", command])
        else:
            self.command_process.start("/bin/sh", ["-c", command])