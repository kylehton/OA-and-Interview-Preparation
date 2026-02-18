import os
import tempfile
import time

from p11_file_cleanup.solution import list_old_files, delete_old_files


def _touch(path: str, mtime: float) -> None:
    with open(path, "w") as f:
        f.write("x")
    os.utime(path, (mtime, mtime))


def test_list_old_files_and_delete(tmp_path):
    root = tmp_path
    now = 10_000.0
    day = 86400.0

    oldf = root / "old.txt"
    newf = root / "new.txt"
    sub = root / "sub"
    sub.mkdir()
    oldsub = sub / "oldsub.txt"

    _touch(str(oldf), now - 10 * day)
    _touch(str(newf), now - 1 * day)
    _touch(str(oldsub), now - 20 * day)

    # older_than_days=5 => oldf and oldsub
    res = list_old_files(str(root), 5, now_ts=now)
    assert res == sorted([str(oldf.resolve()), str(oldsub.resolve())])

    # dry run does not delete
    would = delete_old_files(str(root), 5, dry_run=True, now_ts=now)
    assert would == res
    assert oldf.exists() and oldsub.exists()

    # actual delete
    deleted = delete_old_files(str(root), 5, dry_run=False, now_ts=now)
    assert deleted == res
    assert not oldf.exists()
    assert not oldsub.exists()
    assert newf.exists()


def test_ignores_symlinks(tmp_path):
    root = tmp_path
    now = 50_000.0
    day = 86400.0

    target = root / "target.txt"
    _touch(str(target), now - 10 * day)

    link = root / "link.txt"
    try:
        os.symlink(str(target), str(link))
    except (OSError, NotImplementedError):
        # Some environments may not allow symlinks; if so, skip this test gracefully.
        return

    res = list_old_files(str(root), 5, now_ts=now)
    # target is regular file, link is symlink => only target included
    assert res == [str(target.resolve())]
