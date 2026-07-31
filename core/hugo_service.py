import subprocess
import webbrowser
import platform
from pathlib import Path

from PySide6.QtCore import QProcess




from core.project_options import NewProjectOptions

DEBUG_HUGO_OUTPUT = False


class HugoService:
    def __init__(self, main_window):
        self.main_window = main_window
        self.server_process = QProcess(main_window)
        self.command_process = QProcess(main_window)
        self.build_process = QProcess(main_window)
        self.git_process = QProcess(main_window)
        self.content_process = QProcess(main_window)
        
        # Hugo server state
        self.server_project = None
        self.pending_project = None
        self.server_running = False
        self.build_error = False
        self.theme_dialog = None
     
        self.server_url = "http://localhost:1313"
        
        self.server_process.readyReadStandardOutput.connect(
        self.process_output
        )

        self.server_process.readyReadStandardError.connect(
        self.process_output
        )
        
        self.server_process.finished.connect(self.server_stopped)
        
        self.command_process.readyReadStandardOutput.connect(
        self.command_output
        )

        self.command_process.readyReadStandardError.connect(
            self.command_output
        )

        self.command_process.finished.connect(
            self.command_finished
        )
        
        
        self.build_process.readyReadStandardOutput.connect(
            self.build_stdout
        )

        self.build_process.readyReadStandardError.connect(
            self.build_stderr
        )

        self.build_process.finished.connect(
            self.build_finished    
        
        )
        
        self.git_process.readyReadStandardOutput.connect(
            self.git_stdout
        )

        self.git_process.readyReadStandardError.connect(
            self.git_stderr
        )

        self.git_process.finished.connect(
            self.git_finished
        )



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
            return False

        if self.build_process.state() != QProcess.NotRunning:
            self.main_window.write("Build is already running.")
            return False

        self.build_process.setWorkingDirectory(str(project))

        self.main_window.write("Starting build...")
        self.build_error = False
        self.build_process.start("hugo")
        return True
        
    def new_project(self, options: NewProjectOptions):

        if options.config_format not in {"toml", "yaml", "json"}:
            self.main_window.write("Invalid project configuration format.")
            return False

        result = subprocess.run(
            [
                "hugo",
                "new",
                "site",
                options.name,
                "--format",
                options.config_format,
            ],
            cwd=options.parent_folder,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.main_window.write(result.stderr)
            return False

        project_path = options.parent_folder / options.name

        if options.initialize_git:
            git = subprocess.run(
                ["git", "init"],
                cwd=project_path,
                capture_output=True,
                text=True,
            )

            if git.returncode != 0:
                self.main_window.write(git.stderr)
                return False

        self.main_window.write(f"Created project: {options.name}")
        return True

    def new_content(self, project, content_path):
        
        
        
        
        if project is None:
            self.main_window.write("No project is open.")
            return False

        content_path = Path(content_path)
        if content_path.is_absolute() or ".." in content_path.parts:
            self.main_window.write("Invalid Hugo content path.")
            return False

        if self.content_process.state() != QProcess.NotRunning:
            self.main_window.write("Another content operation is already running.")
            return False

        self.content_process.setWorkingDirectory(str(project))

        if platform.system() == "Windows":
            self.content_process.start(
                "cmd",
                ["/c", f"hugo new content {content_path.as_posix()}"],
            )
        else:
            self.content_process.start(
                "hugo",
                ["new", "content", content_path.as_posix()],
            )

        if not self.content_process.waitForFinished(-1):
            self.main_window.write("Content creation timed out.")
            return False

        if self.content_process.exitCode() != 0:
            error = bytes(
                self.content_process.readAllStandardError()
            ).decode(errors="ignore").strip()

            output = bytes(
                self.content_process.readAllStandardOutput()
            ).decode(errors="ignore").strip()

            self.main_window.write(
                error or output or "Hugo could not create the content file."
            )
            return False

     
        return True
        
    def install_theme(self, project, repo_url, theme_name, dialog):

        if project is None:
            self.main_window.write("No project is open.")
            return

        self.main_window.write(f"Installing theme: {theme_name}")
        self.main_window.write(f"Repository: {repo_url}")
        
        self.theme_dialog = dialog
       
        
        
        destination = project / "themes" / theme_name

        if destination.exists():
            self.main_window.write(
                f"Theme '{theme_name}' is already installed."
            )

            dialog.set_installing(False)
            return

        if self.git_process.state() != QProcess.NotRunning:
            self.main_window.write("Another Git operation is already running.")

            dialog.set_installing(False)
            return

        self.git_process.setWorkingDirectory(str(project))

        self.git_process.start(
            "git",
            [
                "clone",
                repo_url,
                f"themes/{theme_name}",
            ],
        )
        
        
        
    def command_output(self):

        text = bytes(
            self.command_process.readAllStandardOutput()
        ).decode(errors="ignore")

        if not text:
            text = bytes(
                self.command_process.readAllStandardError()
            ).decode(errors="ignore")

        if text:
            self.main_window.write(text.rstrip())
            
    def command_finished(self):
        self.main_window.write("Command finished.")
        
    def process_output(self):

        text = bytes(
            self.server_process.readAllStandardOutput()
        ).decode(errors="ignore")

        if not text:
            text = bytes(
                self.server_process.readAllStandardError()
            ).decode(errors="ignore")

        if "ERROR" in text:

            self.server_project = None
            self.server_running = False

            self.main_window.write(text.strip())
            self.main_window.write("Preview failed.")

            return

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
            
        if self.command_process.state() != QProcess.NotRunning:
            self.main_window.write(
                f"Command already running. State={self.command_process.state()}"
            )
            return

        self.main_window.write(f"> {command}")

        # self.command_process = QProcess(self.main_window)

        self.command_process.setWorkingDirectory(
            str(self.main_window.project)
        )

        # self.command_process.readyReadStandardOutput.connect(
            # lambda: self.main_window.write(
                # bytes(
                    # self.command_process.readAllStandardOutput()
                # ).decode(errors="ignore")
            # )
        # )

        # self.command_process.readyReadStandardError.connect(
            # lambda: self.main_window.write(
                # bytes(
                    # self.command_process.readAllStandardError()
                # ).decode(errors="ignore")
            # )
        # )

        if platform.system() == "Windows":
            self.command_process.start("cmd", ["/c", command])
        else:
            self.command_process.start("/bin/sh", ["-c", command])
            
    def build_stdout(self):

        text = bytes(
            self.build_process.readAllStandardOutput()
        ).decode(errors="ignore")

        if text:
            self.main_window.write(text.rstrip())
            
    def build_stderr(self):

        text = bytes(
            self.build_process.readAllStandardError()
        ).decode(errors="ignore")

        if text:
           
            self.main_window.write(text.rstrip())
            
    def build_finished(self, exit_code, exit_status):

        if exit_code == 0:
            self.main_window.write("Build complete.")
        else:
            self.main_window.write("Build failed.")
            
            
    def git_stdout(self):

        text = bytes(
            self.git_process.readAllStandardOutput()
        ).decode(errors="ignore")

        if text:
            self.main_window.write(text.rstrip())
            
    def git_stderr(self):

        text = bytes(
            self.git_process.readAllStandardError()
        ).decode(errors="ignore")

        if text:
            self.main_window.write(text.rstrip())
            
    def git_finished(self, exit_code, exit_status):

        self.git_stdout()
        self.git_stderr()

        if self.theme_dialog:
            self.theme_dialog.set_installing(False)
            self.theme_dialog = None

        if exit_code == 0:
            self.main_window.write("Theme installation finished.")
        else:
            self.main_window.write("Theme installation failed.")


