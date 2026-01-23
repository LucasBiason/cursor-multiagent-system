#!/usr/bin/env python3
"""
Generic SSH utility functions for remote server operations.

This module provides reusable SSH functions that load credentials from
environment variables, following the pattern defined in config/.env.example.

Usage:
    from core.scripts.infrastructure.ssh_utils import SSHConnection

    with SSHConnection(project="myproject") as ssh:
        result = ssh.execute_command("docker ps")
        print(result.stdout)
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict
from contextlib import contextmanager

try:
    import paramiko
except ImportError:
    print("❌ ERRO: paramiko não está instalado.")
    print("Instale com: pip install paramiko")
    sys.exit(1)

# Try to load environment variables
try:
    from dotenv import load_dotenv
    
    # Get project root
    PROJECT_ROOT = Path(__file__).parent.parent
    env_paths = [
        PROJECT_ROOT / "core" / "config" / ".env.passwords",
        PROJECT_ROOT / ".env.passwords",
        Path.cwd() / ".env.passwords",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            break
except ImportError:
    pass


class SSHConnection:
    """Generic SSH connection manager."""
    
    def __init__(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 22,
        project: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize SSH connection.
        
        Args:
            host: SSH host (IP or hostname). If None, loads from DEPLOYMENT_{PROJECT}_SSH_HOST
            username: SSH username. If None, loads from DEPLOYMENT_{PROJECT}_SSH_USER (default: root)
            password: SSH password. If None, loads from DEPLOYMENT_{PROJECT}_PASSWORD
            port: SSH port (default: 22)
            project: Project name to load credentials from environment (e.g., "myproject")
            timeout: Connection timeout in seconds (default: 30)
        """
        if project:
            project_upper = project.upper()
            self.host = host or os.getenv(f"DEPLOYMENT_{project_upper}_SSH_HOST")
            self.username = username or os.getenv(f"DEPLOYMENT_{project_upper}_SSH_USER", "root")
            self.password = password or os.getenv(f"DEPLOYMENT_{project_upper}_PASSWORD")
        else:
            self.host = host
            self.username = username or "root"
            self.password = password
        
        self.port = port
        self.timeout = timeout
        self.ssh_client: Optional[paramiko.SSHClient] = None
        
        if not self.host:
            raise ValueError("SSH host is required (provide host or project parameter)")
        if not self.password:
            raise ValueError("SSH password is required (provide password or set DEPLOYMENT_{PROJECT}_PASSWORD)")
    
    def connect(self) -> None:
        """Establish SSH connection."""
        if self.ssh_client:
            return
        
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.ssh_client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                look_for_keys=False,
                allow_agent=False,
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.username}@{self.host}:{self.port}: {e}")
    
    def execute_command(
        self,
        command: str,
        get_pty: bool = False,
        timeout: Optional[int] = None,
    ) -> Tuple[int, str, str]:
        """
        Execute a command on the remote server.
        
        Args:
            command: Command to execute
            get_pty: Request a pseudo-terminal (useful for interactive commands)
            timeout: Command timeout (uses connection timeout if None)
        
        Returns:
            Tuple of (exit_status, stdout, stderr)
        """
        if not self.ssh_client:
            self.connect()
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(
                command,
                get_pty=get_pty,
                timeout=timeout or self.timeout,
            )
            
            exit_status = stdout.channel.recv_exit_status()
            stdout_text = stdout.read().decode('utf-8')
            stderr_text = stderr.read().decode('utf-8')
            
            return exit_status, stdout_text, stderr_text
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {e}")
    
    def execute_docker_command(
        self,
        container: str,
        command: str,
        project_dir: Optional[str] = None,
        compose_file: Optional[str] = None,
    ) -> Tuple[int, str, str]:
        """
        Execute a command inside a Docker container.
        
        Args:
            container: Container name or ID
            command: Command to execute inside container
            project_dir: Project directory (for docker compose)
            compose_file: Docker compose file path (optional)
        
        Returns:
            Tuple of (exit_status, stdout, stderr)
        """
        if compose_file and project_dir:
            full_command = f"cd {project_dir} && docker compose -f {compose_file} exec -T {container} {command}"
        else:
            full_command = f"docker exec {container} {command}"
        
        return self.execute_command(full_command, get_pty=True)
    
    def close(self) -> None:
        """Close SSH connection."""
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False


def find_docker_container(ssh: SSHConnection, pattern: str) -> Optional[str]:
    """
    Find Docker container by name pattern.
    
    Args:
        ssh: SSHConnection instance
        pattern: Container name pattern (e.g., "postgres", "backend")
    
    Returns:
        Container name if found, None otherwise
    """
    exit_status, stdout, stderr = ssh.execute_command(
        f"docker ps --format '{{{{.Names}}}}\\t{{{{.Image}}}}' | grep -i {pattern}"
    )
    
    if exit_status == 0 and stdout:
        lines = stdout.strip().split('\n')
        for line in lines:
            if pattern.lower() in line.lower():
                container_name = line.split('\t')[0].strip()
                return container_name
    
    return None


def test_ssh_connection(project: str) -> bool:
    """
    Test SSH connection to a project server.
    
    Args:
        project: Project name to load credentials
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        with SSHConnection(project=project) as ssh:
            exit_status, stdout, stderr = ssh.execute_command("echo 'Connection test successful'")
            return exit_status == 0
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test SSH connection")
    parser.add_argument("--project", help="Project name to load credentials")
    parser.add_argument("--host", help="SSH host")
    parser.add_argument("--username", help="SSH username")
    parser.add_argument("--password", help="SSH password")
    
    args = parser.parse_args()
    
    if args.project:
        success = test_ssh_connection(args.project)
        sys.exit(0 if success else 1)
    elif args.host:
        try:
            with SSHConnection(host=args.host, username=args.username, password=args.password) as ssh:
                exit_status, stdout, stderr = ssh.execute_command("hostname")
                print(f"Connected to: {stdout.strip()}")
                sys.exit(0)
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

