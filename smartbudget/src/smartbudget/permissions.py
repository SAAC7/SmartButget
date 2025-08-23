from jnius import autoclass
from android.permissions import request_permissions, Permission
import android


def ensure_storage_permission():
    """
    Verifica permisos de almacenamiento y los pide si no están concedidos.
    """
    activity = android.activity

    # Clases necesarias
    ContextCompat = autoclass("androidx.core.content.ContextCompat")
    PackageManager = autoclass("android.content.pm.PackageManager")
    Manifest = autoclass("android.Manifest")
    Environment = autoclass("android.os.Environment")

    # Revisar permisos básicos (READ/WRITE)
    granted = ContextCompat.checkSelfPermission(
        activity,
        Manifest.permission.WRITE_EXTERNAL_STORAGE
    ) == PackageManager.PERMISSION_GRANTED

    if not granted:
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])

    # Para Android 11+ MANAGE_EXTERNAL_STORAGE
    if not Environment.isExternalStorageManager():
        Intent = autoclass("android.content.Intent")
        Settings = autoclass("android.provider.Settings")
        Uri = autoclass("android.net.Uri")

        intent = Intent(
            Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION,
            Uri.fromParts("package", activity.getPackageName(), None)
        )
        activity.startActivity(intent)
