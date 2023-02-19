"""HACS Backup Test Suite."""
# pylint: disable=missing-docstring
import os

from custom_components.hacs.utils.backup import Backup, BackupNetDaemon


def test_file(hacs, tmpdir):
    with open(f"{tmpdir.dirname}/dummy_file", "w") as dummy:
        dummy.write("")

    backup = Backup(hacs=hacs, local_path=f"{tmpdir.dirname}/dummy_file")
    backup.create()

    assert not os.path.exists(backup.local_path)
    assert os.path.exists(backup.backup_path_full)

    backup.restore()
    assert os.path.exists(backup.local_path)

    backup.cleanup()
    assert not os.path.exists(backup.backup_path_full)


def test_directory(hacs, tmpdir):
    os.makedirs(f"{tmpdir.dirname}/dummy_directory", exist_ok=True)

    backup = Backup(hacs=hacs, local_path=f"{tmpdir.dirname}/dummy_directory")
    backup.create()

    assert not os.path.exists(backup.local_path)
    assert os.path.exists(backup.backup_path_full)

    backup.restore()
    assert os.path.exists(backup.local_path)

    backup.cleanup()
    assert not os.path.exists(backup.backup_path_full)


def test_muilti(hacs, tmpdir):
    backup = Backup(hacs=hacs, local_path=f"{tmpdir.dirname}/dummy_directory")
    backup.create()
    backup.create()


def test_netdaemon_backup(hacs, repository_netdaemon):
    repository = repository_netdaemon
    repository.content.path.local = repository.localpath
    os.makedirs(repository.content.path.local, exist_ok=True)
    backup = BackupNetDaemon(hacs=hacs, repository=repository)
    backup.cleanup()
    with open(f"{repository.content.path.local}/dummy_file.yaml", "w") as dummy:
        dummy.write("test: test")
    with open(f"{repository.content.path.local}/dummy_file.yaml") as dummy:
        content = dummy.read()
        assert content == "test: test"
    assert not os.path.exists(backup.backup_path)
    os.makedirs(backup.backup_path, exist_ok=True)
    backup.create()
    assert os.path.exists(backup.backup_path)
    with open(f"{repository.content.path.local}/dummy_file.yaml", "w") as dummy:
        dummy.write("tests: tests")
    with open(f"{repository.content.path.local}/dummy_file.yaml") as dummy:
        content = dummy.read()
        assert content == "tests: tests"
    backup.restore()
    backup.cleanup()
    assert not os.path.exists(backup.backup_path)
    with open(f"{repository.content.path.local}/dummy_file.yaml") as dummy:
        content = dummy.read()
        assert content == "test: test"
