# File Renaming Script

Este script está diseñado para renombrar todos los archivos y directorios en el repositorio MarioIbago/math-aa-notes siguiendo reglas específicas de nomenclatura.

## Reglas de Renombrado

1. **Eliminar espacios**: Todos los espacios se reemplazan por guiones bajos (_)
2. **Formato Title Case**: Cada palabra comienza con mayúscula
3. **Preservar extensiones**: Las extensiones de archivo se mantienen sin cambios
4. **Procesamiento recursivo**: Se aplica a todos los archivos y directorios, incluyendo subcarpetas

## Ejemplos de Conversión

| Antes | Después |
|-------|---------|
| `area bajo la curva.pdf` | `Area_Bajo_La_Curva.pdf` |
| `resumen final.pdf` | `Resumen_Final.pdf` |
| `ejercicios de calculo.txt` | `Ejercicios_De_Calculo.txt` |
| `carpeta con espacios/` | `Carpeta_Con_Espacios/` |
| `archivo   con espacios  múltiples.doc` | `Archivo_Con_Espacios_Múltiples.doc` |

## Uso

### Sintaxis Básica

```bash
python rename_files.py [directorio]
```

### Ejemplos

```bash
# Renombrar archivos en el directorio actual
python rename_files.py

# Renombrar archivos en un directorio específico
python rename_files.py /ruta/al/directorio

# Renombrar archivos en el repositorio math-aa-notes
python rename_files.py /ruta/al/math-aa-notes
```

## Características

- ✅ **Confirmación interactiva**: Solicita confirmación antes de proceder
- ✅ **Procesamiento recursivo**: Maneja archivos en subdirectorios
- ✅ **Manejo de directorios**: Renombra tanto archivos como directorios
- ✅ **Manejo de espacios múltiples**: Convierte espacios consecutivos en un solo guión bajo
- ✅ **Espacios iniciales/finales**: Elimina espacios al inicio y final de nombres
- ✅ **Prevención de conflictos**: Detecta si el archivo de destino ya existe
- ✅ **Reporte detallado**: Muestra estadísticas del proceso
- ✅ **Manejo de errores**: Informa errores sin detener el proceso

## Archivos que se Omiten

El script automáticamente omite:

- Archivos y directorios ocultos (que comienzan con `.`)
- Directorios del sistema (`.git`, `.github`, `.vscode`, `__pycache__`, `node_modules`, `.streamlit`)
- Archivos que no contienen espacios (no necesitan renombrado)

## Salida del Script

El script proporciona:

- **Vista previa**: Lista cada archivo/directorio renombrado
- **Iconos visuales**: 📄 para archivos, 📁 para directorios
- **Advertencias**: ⚠️ para conflictos potenciales
- **Errores**: ❌ para problemas durante el renombrado
- **Resumen**: Estadísticas finales del proceso

### Ejemplo de Salida

```
File Renaming Script for MarioIbago/math-aa-notes
============================================================
Rules:
1. Replace spaces with underscores (_)
2. Convert to Title Case
3. Preserve file extensions
4. Process all files and directories in subdirectories

Do you want to rename files in '/path/to/directory'? (y/N): y

Processing directory: /path/to/directory
============================================================
📁 Renamed directory: carpeta con espacios -> Carpeta_Con_Espacios
📄 Renamed file: area bajo la curva.pdf -> Area_Bajo_La_Curva.pdf
📄 Renamed file: resumen final.pdf -> Resumen_Final.pdf

============================================================
SUMMARY:
Files renamed: 2
Directories renamed: 1
Items skipped: 0
Errors: 0
Total items processed: 3
```

## Consideraciones Importantes

1. **Backup recomendado**: Hacer una copia de seguridad antes de ejecutar el script
2. **Confirmación requerida**: El script siempre pide confirmación antes de proceder
3. **Proceso irreversible**: Una vez renombrados, los archivos no se pueden deshacer automáticamente
4. **Permisos**: Asegúrese de tener permisos de escritura en el directorio objetivo

## Requisitos

- Python 3.6 o superior
- Permisos de lectura y escritura en el directorio objetivo

## Instalación

No requiere instalación adicional. Solo ejecute el script directamente:

```bash
python rename_files.py
```