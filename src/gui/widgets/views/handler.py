import logging
import os
import git
import hashlib
import datetime
import json
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit,
    QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class FirmwareEncoder(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Default Deployment Directory variable
        self.default_deploy_dir = ""

        # Repository path variable
        self.repo_path = None

        # Window utils
        self.logger = logging.getLogger('NeveBit')

        # ------------------------
        # Directory Group (Default Deployment Directory)
        # ------------------------
        self.default_dir_input = QLineEdit()
        self.default_dir_input.setObjectName("basic")
        self.default_dir_input.setPlaceholderText("Select Default Deployment Directory")
        self.default_dir_btn = QPushButton("Browse")
        self.default_dir_btn.setObjectName("basic")
        self.default_dir_btn.clicked.connect(self.browse_default_directory)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.default_dir_input)
        dir_layout.addWidget(self.default_dir_btn)
        self.directory_group = QWidget()
        self.directory_group.setObjectName("group_container")
        dir_group_layout = QVBoxLayout(self.directory_group)
        dir_title = QLabel("Default Deployment Directory")
        dir_title.setObjectName("group_label")
        dir_group_layout.addWidget(dir_title)
        dir_group_layout.addLayout(dir_layout)

        # ------------------------
        # AES Inputs
        # ------------------------
        self.aes_key_input = QLineEdit()
        self.aes_key_input.setObjectName("basic")
        self.aes_key_input.setPlaceholderText("AES-256 Key (32 hex chars)")

        self.aes_iv_input = QLineEdit()
        self.aes_iv_input.setObjectName("basic")
        self.aes_iv_input.setPlaceholderText("AES IV (16 hex chars)")

        # ------------------------
        # Firmware File Selection (Encryption)
        # ------------------------
        self.firmware_path_input = QLineEdit()
        self.firmware_path_input.setObjectName("basic")
        self.firmware_path_input.setPlaceholderText("Select Firmware File")

        self.select_fw_btn = QPushButton("Browse")
        self.select_fw_btn.setObjectName("basic")
        self.select_fw_btn.clicked.connect(self.browse_firmware)

        self.encrypt_fw_btn = QPushButton("Encrypt Firmware")
        self.encrypt_fw_btn.setObjectName("basic")
        self.encrypt_fw_btn.clicked.connect(self.encrypt_firmware)

        fw_layout = QHBoxLayout()
        fw_layout.addWidget(self.firmware_path_input)
        fw_layout.addWidget(self.select_fw_btn)
        encryptor_content = QVBoxLayout()
        encryptor_info_label = QLabel("Select a firmware file and use the provided key/IV to encrypt it. The encrypted firmware is saved locally or updated in a repository.")
        encryptor_info_label.setObjectName("group_label")
        encryptor_info_label.setWordWrap(True)
        encryptor_content.addWidget(encryptor_info_label)
        encryptor_content.addLayout(fw_layout)
        encryptor_content.addWidget(self.encrypt_fw_btn)
        self.encryptor_group = QWidget()
        self.encryptor_group.setObjectName("group_container")
        encryptor_group_layout = QVBoxLayout(self.encryptor_group)
        encryptor_title = QLabel("Firmware Encryptor")
        encryptor_title.setObjectName("group_label")
        encryptor_group_layout.addWidget(encryptor_title)
        encryptor_group_layout.addLayout(encryptor_content)

        # ------------------------
        # Firmware File Selection (Decryption)
        # ------------------------
        self.encrypted_fw_path_input = QLineEdit()
        self.encrypted_fw_path_input.setObjectName("basic")
        self.encrypted_fw_path_input.setPlaceholderText("Select Encrypted Firmware File")

        self.select_enc_fw_btn = QPushButton("Browse")
        self.select_enc_fw_btn.setObjectName("basic")
        self.select_enc_fw_btn.clicked.connect(self.browse_encrypted_firmware)

        self.decrypt_fw_btn = QPushButton("Decrypt Firmware")
        self.decrypt_fw_btn.setObjectName("basic")
        self.decrypt_fw_btn.clicked.connect(self.decrypt_firmware)

        dec_file_layout = QHBoxLayout()
        dec_file_layout.addWidget(self.encrypted_fw_path_input)
        dec_file_layout.addWidget(self.select_enc_fw_btn)
        decryptor_content = QVBoxLayout()
        decryptor_info_label = QLabel("Select an encrypted firmware file and use the same key/IV to decrypt it. A decrypted backup will be created.")
        decryptor_info_label.setObjectName("group_label")
        decryptor_info_label.setWordWrap(True)
        decryptor_content.addWidget(decryptor_info_label)
        decryptor_content.addLayout(dec_file_layout)
        decryptor_content.addWidget(self.decrypt_fw_btn)
        self.decryptor_group = QWidget()
        self.decryptor_group.setObjectName("group_container")
        decryptor_group_layout = QVBoxLayout(self.decryptor_group)
        decryptor_title = QLabel("Firmware Decryptor")
        decryptor_title.setObjectName("group_label")
        decryptor_group_layout.addWidget(decryptor_title)
        decryptor_group_layout.addLayout(decryptor_content)

        # ------------------------
        # Git / Deploy Repository Section
        # ------------------------
        self.repo_link_input = QLineEdit()
        self.repo_link_input.setObjectName("basic")
        self.repo_link_input.setPlaceholderText("Git Repository Link")

        self.branch_selector = QComboBox()
        self.branch_selector.setObjectName("basic")

        self.clone_btn = QPushButton("Clone Repo")
        self.clone_btn.setObjectName("basic")
        self.clone_btn.clicked.connect(self.clone_repo)

        self.deploy_btn = QPushButton("Deploy")
        self.deploy_btn.setObjectName("basic")
        self.deploy_btn.clicked.connect(self.deploy_repo)

        self.test_repo_btn = QPushButton("Test Repo URL")
        self.test_repo_btn.setObjectName("basic")
        self.test_repo_btn.clicked.connect(self.test_repo_url)

        self.open_local_repo_btn = QPushButton("Open Local Repo")
        self.open_local_repo_btn.setObjectName("basic")
        self.open_local_repo_btn.clicked.connect(self.open_local_repo)

        repo_layout = QHBoxLayout()
        repo_layout.addWidget(self.repo_link_input)
        repo_layout.addWidget(self.test_repo_btn)

        branch_layout = QHBoxLayout()
        branch_label = QLabel("Branch:")
        branch_layout.addWidget(branch_label)
        branch_layout.addWidget(self.branch_selector)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clone_btn)
        button_layout.addWidget(self.open_local_repo_btn)
        button_layout.addWidget(self.deploy_btn)

        deploy_content = QVBoxLayout()
        deploy_info_label = QLabel("This block allows you to clone, open, deploy, and test the repository URL.")
        deploy_info_label.setObjectName("group_label")
        deploy_info_label.setWordWrap(True)
        deploy_content.addWidget(deploy_info_label)
        deploy_content.addLayout(repo_layout)
        deploy_content.addLayout(branch_layout)
        deploy_content.addLayout(button_layout)

        self.deploy_group = QWidget()
        self.deploy_group.setObjectName("group_container")
        deploy_group_layout = QVBoxLayout(self.deploy_group)
        deploy_title = QLabel("Deploy Repository")
        deploy_title.setObjectName("group_label")
        deploy_group_layout.addWidget(deploy_title)
        deploy_group_layout.addLayout(deploy_content)

        # ------------------------
        # Encryption Keys Section
        # ------------------------
        keys_content = QVBoxLayout()
        keys_info_label = QLabel("Enter your AES-256 key (32 hex characters) and IV (16 hex characters) for both encryption and decryption.")
        keys_info_label.setObjectName("group_label")
        keys_info_label.setWordWrap(True)
        keys_content.addWidget(keys_info_label)
        keys_content.addWidget(self.aes_key_input)
        keys_content.addWidget(self.aes_iv_input)

        self.keys_group = QWidget()
        self.keys_group.setObjectName("group_container")
        keys_group_layout = QVBoxLayout(self.keys_group)
        keys_title = QLabel("Encryption Keys")
        keys_title.setObjectName("group_label")
        keys_group_layout.addWidget(keys_title)
        keys_group_layout.addLayout(keys_content)

        # ------------------------
        # Firmware Meta Section
        # ------------------------
        self.version_input = QLineEdit()
        self.version_input.setObjectName("basic")
        self.version_input.setPlaceholderText("Firmware Version")

        self.update_version_btn = QPushButton("Update Version")
        self.update_version_btn.setObjectName("basic")
        self.update_version_btn.clicked.connect(self.update_version)

        version_layout = QHBoxLayout()
        version_layout.addWidget(self.version_input)
        version_layout.addWidget(self.update_version_btn)

        self.meta_url_input = QLineEdit()
        self.meta_url_input.setObjectName("basic")
        self.meta_url_input.setPlaceholderText("Repository URL")
        self.meta_url_input.setReadOnly(True)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.meta_url_input)

        self.meta_hash_input = QLineEdit()
        self.meta_hash_input.setObjectName("basic")
        self.meta_hash_input.setPlaceholderText("Firmware Hash")
        self.meta_hash_input.setReadOnly(True)
        hash_layout = QHBoxLayout()
        hash_layout.addWidget(self.meta_hash_input)

        self.meta_date_input = QLineEdit()
        self.meta_date_input.setObjectName("basic")
        self.meta_date_input.setPlaceholderText("Date Generated")
        self.meta_date_input.setReadOnly(True)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.meta_date_input)

        self.meta_size_input = QLineEdit()
        self.meta_size_input.setObjectName("basic")
        self.meta_size_input.setPlaceholderText("Size (bytes)")
        self.meta_size_input.setReadOnly(True)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.meta_size_input)

        meta_content = QVBoxLayout()
        meta_info_label = QLabel("Displays metadata such as firmware hash, generation date, file size, and repository URL after encryption.")
        meta_info_label.setObjectName("group_label")
        meta_info_label.setWordWrap(True)
        meta_content.addWidget(meta_info_label)
        meta_content.addLayout(version_layout)
        meta_content.addLayout(url_layout)
        meta_content.addLayout(hash_layout)
        meta_content.addLayout(date_layout)
        meta_content.addLayout(size_layout)

        self.meta_group = QWidget()
        self.meta_group.setObjectName("group_container")
        meta_group_layout = QVBoxLayout(self.meta_group)
        meta_title = QLabel("Firmware Meta")
        meta_title.setObjectName("group_label")
        meta_group_layout.addWidget(meta_title)
        meta_group_layout.addLayout(meta_content)

        # ------------------------
        # Main Layout
        # ------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addWidget(self.directory_group)
        main_layout.addWidget(self.deploy_group)
        main_layout.addWidget(self.keys_group)
        main_layout.addWidget(self.encryptor_group)
        main_layout.addWidget(self.decryptor_group)
        main_layout.addWidget(self.meta_group)

    def browse_default_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Default Deployment Directory")
        if dir_path:
            self.default_deploy_dir = dir_path
            self.default_dir_input.setText(dir_path)

    def browse_firmware(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Firmware")
        if file_path:
            self.firmware_path_input.setText(file_path)

    def browse_encrypted_firmware(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Firmware")
        if file_path:
            self.encrypted_fw_path_input.setText(file_path)

    def encrypt_firmware(self):
        key_input = self.aes_key_input.text().strip()
        iv_input = self.aes_iv_input.text().strip()
        try:
            key = bytes.fromhex(key_input)
            iv = bytes.fromhex(iv_input)
        except ValueError:
            self.logger.info("Invalid hex format for key or IV.")
            return

        if len(key) != 32 or len(iv) != 16:
            self.logger.info("Invalid AES key or IV length.")
            return

        file_path = self.firmware_path_input.text()
        if not os.path.exists(file_path):
            self.logger.info("Firmware file does not exist.")
            return

        with open(file_path, 'rb') as fw_file:
            firmware_data = fw_file.read()

        cipher = AES.new(key, AES.MODE_CFB, iv)
        encrypted_data = cipher.encrypt(firmware_data)
        encrypted_local_path = file_path + '.enc'
        with open(encrypted_local_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)
        self.logger.info(f"Firmware encrypted locally: {encrypted_local_path}")

        firmware_hash = hashlib.sha256(encrypted_data).hexdigest()
        file_size = len(encrypted_data)
        date_generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.repo_path:
            firmware_repo_path = os.path.join(self.repo_path, "firmware.bin")
            with open(firmware_repo_path, 'wb') as repo_fw_file:
                repo_fw_file.write(encrypted_data)
            self.logger.info(f"Firmware updated in repo at: {firmware_repo_path}")

            repo_url = ""
            try:
                repo_obj = git.Repo(self.repo_path)
                if repo_obj.remotes and repo_obj.remotes.origin:
                    repo_url = repo_obj.remotes.origin.url
            except Exception:
                repo_url = "Unknown"

            meta_data = {
                "repository_url": repo_url,
                "firmware_hash": firmware_hash,
                "date_generated": date_generated,
                "file_size": file_size
            }
            meta_repo_path = os.path.join(self.repo_path, "meta.json")
            with open(meta_repo_path, 'w') as meta_file:
                json.dump(meta_data, meta_file, indent=4)
            self.logger.info(f"Meta information written to: {meta_repo_path}")
            self.load_meta_info(meta_repo_path)
        else:
            # If no repository is loaded, prompt for a directory unless a default is set
            if self.default_deploy_dir:
                dest_folder = self.default_deploy_dir
            else:
                dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
            if dest_folder:
                firmware_dest_path = os.path.join(dest_folder, "firmware.bin")
                with open(firmware_dest_path, 'wb') as fw_dest:
                    fw_dest.write(encrypted_data)
                self.logger.info(f"Encrypted firmware saved at: {firmware_dest_path}")

                meta_data = {
                    "firmware_hash": firmware_hash,
                    "date_generated": date_generated,
                    "file_size": file_size
                }
                meta_dest_path = os.path.join(dest_folder, "meta.json")
                with open(meta_dest_path, 'w') as meta_file:
                    json.dump(meta_data, meta_file, indent=4)
                self.logger.info(f"Meta information written to: {meta_dest_path}")

                default_version = "v0.1.0"
                version_dest_path = os.path.join(dest_folder, "version.txt")
                with open(version_dest_path, 'w') as ver_file:
                    ver_file.write(default_version)
                self.version_input.setText(default_version)
                self.logger.info(f"Default version.txt created with version {default_version} at: {version_dest_path}")
                self.meta_url_input.setText("")
                self.load_meta_info(meta_dest_path)
            else:
                self.logger.info("No destination folder selected. Encrypted file remains only as backup.")

        self.meta_hash_input.setText(firmware_hash)
        self.meta_date_input.setText(date_generated)
        self.meta_size_input.setText(str(file_size))

    def decrypt_firmware(self):
        key_input = self.aes_key_input.text().strip()
        iv_input = self.aes_iv_input.text().strip()
        try:
            key = bytes.fromhex(key_input)
            iv = bytes.fromhex(iv_input)
        except ValueError:
            self.logger.info("Invalid hex format for key or IV.")
            return

        if len(key) != 32 or len(iv) != 16:
            self.logger.info("Invalid AES key or IV length.")
            return

        file_path = self.encrypted_fw_path_input.text()
        if not os.path.exists(file_path):
            self.logger.info("Encrypted firmware file does not exist.")
            return

        with open(file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        cipher = AES.new(key, AES.MODE_CFB, iv)
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
        except ValueError:
            self.logger.info("Decryption failed. Possibly wrong key, IV or corrupted file.")
            return

        decrypted_local_path = file_path + '.dec'
        with open(decrypted_local_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)
        self.logger.info(f"Firmware decrypted locally: {decrypted_local_path}")

    def get_branches(self, repo):
        try:
            if repo.remotes and repo.remotes.origin:
                branches = [ref.name.split('/')[-1] for ref in repo.remotes.origin.refs]
                branches = list(dict.fromkeys(branches))
                return branches
            else:
                return [head.name for head in repo.heads]
        except Exception as e:
            self.logger.info(f"Error retrieving branches: {e}")
            return []

    def clone_repo(self):
        repo_url = self.repo_link_input.text().strip()
        if not repo_url:
            self.logger.info("Repository URL missing!")
            return

        # Extract repository name from URL
        repo_name = os.path.basename(repo_url)
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        # If a default directory is set, clone inside a subfolder with the repo's name
        if self.default_deploy_dir:
            clone_path = os.path.join(self.default_deploy_dir, repo_name)
        else:
            base_path = QFileDialog.getExistingDirectory(self, "Select Clone Directory")
            if not base_path:
                self.logger.info("No clone directory selected.")
                return
            clone_path = os.path.join(base_path, repo_name)

        try:
            repo = git.Repo.clone_from(repo_url, clone_path)
            branches = self.get_branches(repo)
            self.branch_selector.clear()
            self.branch_selector.addItems(branches)
            self.repo_path = clone_path
            self.logger.info(f"Repository cloned at {clone_path}")

            # Load version.txt if it exists
            version_path = os.path.join(clone_path, "version.txt")
            if os.path.exists(version_path):
                with open(version_path, 'r') as ver_file:
                    version = ver_file.read().strip()
                    self.version_input.setText(version)
                self.logger.info("Version loaded from version.txt.")
            else:
                self.logger.info("version.txt not found in repository.")

            # Load meta.json if it exists
            meta_json_path = os.path.join(clone_path, "meta.json")
            if os.path.exists(meta_json_path):
                self.load_meta_info(meta_json_path)
            else:
                self.logger.info("meta.json not found in repository.")
        except Exception as e:
            self.logger.info(f"Error cloning repository: {e}")

    def deploy_repo(self):
        if not self.repo_path:
            self.logger.info("No repository loaded. Please clone or open a local repo first.")
            return

        try:
            repo = git.Repo(self.repo_path)
            selected_branch = self.branch_selector.currentText().strip()
            repo.git.checkout(selected_branch)
            origin = repo.remotes.origin
            origin.pull()
            self.logger.info(f"Checked out branch '{selected_branch}' at {self.repo_path}")

            version_path = os.path.join(self.repo_path, "version.txt")
            if os.path.exists(version_path):
                with open(version_path, 'r') as ver_file:
                    version = ver_file.read().strip()
                    self.version_input.setText(version)
                self.logger.info("Version loaded from version.txt.")
            else:
                self.logger.info("version.txt not found in repository.")

            version_value = self.version_input.text().strip()
            commit_message = f"Firmware update version: {version_value}" if version_value else "Firmware update"

            if repo.is_dirty(untracked_files=True):
                repo.git.add(A=True)
                repo.index.commit(commit_message)
                origin.push()
                self.logger.info(f"Changes pushed with commit message: '{commit_message}'")
            else:
                self.logger.info("No changes to push.")

            meta_json_path = os.path.join(self.repo_path, "meta.json")
            if os.path.exists(meta_json_path):
                self.load_meta_info(meta_json_path)
            else:
                self.logger.info("meta.json not found in repository.")
        except Exception as e:
            self.logger.info(f"Error deploying repository: {e}")

    def open_local_repo(self):
        repo_path = QFileDialog.getExistingDirectory(self, "Select Local Repository")
        if repo_path:
            try:
                repo = git.Repo(repo_path)
                self.repo_path = repo_path
                branches = self.get_branches(repo)
                self.branch_selector.clear()
                self.branch_selector.addItems(branches)
                self.logger.info(f"Local repository opened at {repo_path}")

                version_path = os.path.join(repo_path, "version.txt")
                if os.path.exists(version_path):
                    with open(version_path, 'r') as ver_file:
                        version = ver_file.read().strip()
                        self.version_input.setText(version)
                    self.logger.info("Version loaded from version.txt.")
                else:
                    self.logger.info("version.txt not found in repository.")

                meta_json_path = os.path.join(self.repo_path, "meta.json")
                if os.path.exists(meta_json_path):
                    self.load_meta_info(meta_json_path)
                else:
                    self.logger.info("meta.json not found in repository.")
            except Exception as e:
                self.logger.info(f"Error opening repository: {e}")

    def update_version(self):
        if self.repo_path:
            version = self.version_input.text().strip()
            version_path = os.path.join(self.repo_path, "version.txt")
            try:
                with open(version_path, 'w') as ver_file:
                    ver_file.write(version)
                self.logger.info(f"Version updated to: {version}")
            except Exception as e:
                self.logger.info(f"Error updating version: {e}")
        else:
            self.logger.info("No repository selected. Clone, deploy, or open a repository first.")

    def load_meta_info(self, meta_path):
        try:
            with open(meta_path, 'r') as meta_file:
                meta_data = json.load(meta_file)
            self.meta_url_input.setText(meta_data.get("repository_url", ""))
            self.repo_link_input.setText(meta_data.get("repository_url", ""))
            self.meta_hash_input.setText(meta_data.get("firmware_hash", ""))
            self.meta_date_input.setText(meta_data.get("date_generated", ""))
            self.meta_size_input.setText(str(meta_data.get("file_size", "")))
            self.logger.info("Meta information loaded successfully.")
        except Exception as e:
            self.logger.info(f"Error loading meta info: {e}")

    def test_repo_url(self):
        url = self.repo_link_input.text().strip()
        if not url:
            self.logger.info("No repository URL provided to test.")
            return
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                self.logger.info(f"Repository URL is reachable: {url}")
            else:
                self.logger.info(f"Repository URL responded with status code: {response.status_code}")
        except Exception as e:
            self.logger.info(f"Error testing repository URL: {e}")
