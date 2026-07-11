import subprocess
import webbrowser

from PySide6.QtCore import QProcess, QTimer

from core.themes import THEMES

DEBUG_HUGO_OUTPUT = False


class HugoService:
    def __init__(self, parent):
        self.parent = parent
        self.process = QProcess(parent)
        
        # Hugo server state
        self.server_project = None
        self.pending_project = None
        self.server_running = False
     
        self.server_url = "http://localhost:1313"
        
        self.process.readyReadStandardOutput.connect(
        self.process_output
        )

        self.process.readyReadStandardError.connect(
        self.process_output
        )

    def preview(self, project):

        if project is None:
            return
            
        if (
            self.process.state() != QProcess.NotRunning
            and self.server_project != project
        ):
            self.process.kill()
            self.process.waitForFinished()

        if self.process.state() == QProcess.NotRunning:

            self.process.setWorkingDirectory(str(project))
            
            self.pending_project = project
            
            
            self.process.start(
                "hugo",
                [
                    "server",
                    "--disableFastRender",
                ],
            )

            self.parent.write("Starting Hugo server...")

            # QTimer.singleShot(
                # 2500,
                # lambda: webbrowser.open(self.server_url),
            # )

        else:

            if self.server_project == project:

                webbrowser.open(self.server_url)
                self.parent.write("Opened browser.")

    def build(self, project):

        if project is None:
            return

        subprocess.run(
            ["hugo"],
            cwd=project,
        )

        self.parent.write("Build complete.")
        
    def new_project(self, parent_folder, name):

        result = subprocess.run(
            ["hugo", "new", "site", name],
            cwd=parent_folder,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:

            self.parent.write(f"Created project: {name}")
            return True

        self.parent.write(result.stderr)
        return False
        
    def install_theme(self, project, theme):

        if project is None:

            self.parent.write("No project is open.")
            return

        self.parent.write(f"Installing theme: {theme}")
    


        repo = THEMES[theme]["repo"]
        self.parent.write(f"Repository: {repo}")

        
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

        self.parent.write("Theme installation finished.")
        
    def process_output(self):

        text = bytes(
            self.process.readAllStandardOutput()
        ).decode(errors="ignore")
        
        if "ERROR" in text:

            self.server_project = None
            self.server_running = False
            self.parent.write("Preview failed.")
            return

        if not text:
            text = bytes(
                self.process.readAllStandardError()
            ).decode(errors="ignore")

        if text:
            self.parent.write(text.strip())

        if DEBUG_HUGO_OUTPUT:
            self.parent.write(text.strip())
        
        if "Web Server is available at" in text:

            self.parent.write("Hugo server is ready.")
            
            self.server_project = self.pending_project
            self.pending_project = None
            self.server_running = True

       

            webbrowser.open(self.server_url)