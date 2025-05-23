import reflex as rx
from typing import Dict, Any, List, Optional
import json
import uuid
from datetime import datetime

class AppState(rx.State):
    user_id: str = ""
    session_id: str = ""
    api_keys: Dict[str, str] = {}
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    uploaded_files: List[str] = []
    execution_log: List[Dict[str, Any]] = []

    def __init__(self):
        super().__init__()
        self.session_id = str(uuid.uuid4())
        self.user_id = f"user_{self.session_id[:8]}"

    @rx.event
    def set_api_key(self, provider: str, key: str):
        self.api_keys[provider] = key
        self.success_message = f"API key set for {provider}"
        yield self.clear_messages_after_delay()

    @rx.event
    def clear_api_key(self, provider: str):
        if provider in self.api_keys:
            del self.api_keys[provider]
            self.success_message = f"API key cleared for {provider}"
            yield self.clear_messages_after_delay()

    @rx.event
    def set_loading(self, loading: bool):
        self.is_loading = loading

    @rx.event
    def set_error(self, message: str):
        self.error_message = message
        self.is_loading = False
        yield self.clear_messages_after_delay()

    @rx.event
    def set_success(self, message: str):
        self.success_message = message
        yield self.clear_messages_after_delay()

    @rx.event
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    @rx.event
    async def clear_messages_after_delay(self):
        import asyncio
        await asyncio.sleep(3)
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def add_to_log(self, message: str, level: str = "info", data: Optional[Dict[str, Any]] = None):
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "level": level,
            "data": data or {}
        }
        self.execution_log.append(entry)

        if len(self.execution_log) > 100:
            self.execution_log = self.execution_log[-100:]

    @rx.event
    def clear_log(self):
        self.execution_log = []

    @rx.event
    async def handle_file_upload(self, files: List[rx.UploadFile]):
        try:
            self.set_loading(True)
            uploaded_files = []

            for file in files:
                file_path = f"uploads/{self.user_id}_{file.filename}"
                with open(file_path, "wb") as f:
                    f.write(await file.read())

                uploaded_files.append(file_path)
                self.add_to_log(f"File uploaded: {file.filename}")

            self.uploaded_files.extend(uploaded_files)
            self.set_success(f"Uploaded {len(uploaded_files)} file(s)")

        except Exception as e:
            self.set_error(f"Upload failed: {str(e)}")
        finally:
            self.set_loading(False)

    @rx.event
    def export_project(self):
        self.add_to_log("Project exported")
        self.set_success("Project exported successfully")

    @rx.event
    def import_project(self, project_data: str):
        try:
            data = json.loads(project_data)
            self.add_to_log("Project imported")
            self.set_success("Project imported successfully")
        except Exception as e:
            self.set_error(f"Import failed: {str(e)}")
