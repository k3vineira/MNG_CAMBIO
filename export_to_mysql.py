#!/usr/bin/env python3
"""
=============================================================================
Exportador de SQLite a MySQL / MySQL Workbench
Proyecto: Monagua (MNG_WEB)
=============================================================================
Este script convierte la base de datos SQLite (db.sqlite3) a un archivo .sql
completamente compatible con MySQL y optimizado para generar diagramas EER
(Entidad-Relación) en MySQL Workbench.

Uso:
    python export_to_mysql.py
    python export_to_mysql.py --all-tables
    python export_to_mysql.py --with-data
    python export_to_mysql.py --output mi_diagrama.sql
=============================================================================
"""

import os
import sys
import sqlite3
import argparse
import re
from datetime import datetime

# Tablas del núcleo de negocio Monagua
BUSINESS_TABLE_PREFIXES = (
    'usuarios_',
    'catalogo_',
    'paquete_',
    'reservas_',
    'pagos_',
    'comunidad_',
    'promociones_',
    'notificaciones_',
    'seguros_',
    'plan_',
    'factura',
)

# Tablas del dominio completo (Negocio + Auth de Django)
DOMAIN_TABLE_PREFIXES = BUSINESS_TABLE_PREFIXES + (
    'auth_user',
    'auth_group',
    'auth_permission',
    'django_content_type',
)


def map_sqlite_type_to_mysql(col_name: str, col_type: str, is_pk: bool, is_autoincrement: bool) -> str:
    """Mapea tipos de datos de SQLite a tipos válidos y limpios de MySQL."""
    col_type_raw = col_type.strip().lower()

    if is_autoincrement or (is_pk and 'int' in col_type_raw):
        if 'bigint' in col_type_raw:
            return 'BIGINT NOT NULL AUTO_INCREMENT'
        return 'INT NOT NULL AUTO_INCREMENT'

    if col_type_raw == 'bool' or col_type_raw == 'boolean':
        return 'TINYINT(1)'

    if 'smallint unsigned' in col_type_raw:
        return 'SMALLINT UNSIGNED'
    if 'integer unsigned' in col_type_raw or 'int unsigned' in col_type_raw:
        return 'INT UNSIGNED'
    if 'bigint unsigned' in col_type_raw:
        return 'BIGINT UNSIGNED'
    if 'smallint' in col_type_raw:
        return 'SMALLINT'
    if 'bigint' in col_type_raw:
        return 'BIGINT'
    if 'int' in col_type_raw:
        return 'INT'

    if col_type_raw.startswith('varchar'):
        return col_type.upper()
    if col_type_raw == 'text':
        return 'LONGTEXT' if 'biografia' in col_name or 'contenido' in col_name or 'descripcion' in col_name else 'TEXT'
    if col_type_raw == 'datetime':
        return 'DATETIME'
    if col_type_raw == 'date':
        return 'DATE'
    if col_type_raw == 'time':
        return 'TIME'
    if col_type_raw.startswith('decimal') or col_type_raw == 'numeric':
        match = re.search(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', col_type_raw)
        if match:
            return f"DECIMAL({match.group(1)}, {match.group(2)})"
        return 'DECIMAL(12, 2)'
    if col_type_raw in ('real', 'float', 'double'):
        return 'DOUBLE'
    if col_type_raw == 'blob':
        return 'LONGBLOB'

    if not col_type:
        return 'VARCHAR(255)'

    return col_type.upper()


def get_table_metadata(conn, table_name):
    """Extrae columnas, PK, FK e índices únicos de una tabla SQLite."""
    cur = conn.cursor()

    # Obtener DDL original de sqlite_master
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    row = cur.fetchone()
    original_sql = row[0] if row else ""

    # Columnas: (cid, name, type, notnull, dflt_value, pk)
    cur.execute(f"PRAGMA table_info(`{table_name}`)")
    columns_info = cur.fetchall()

    # Foreign Keys: (id, seq, table, from, to, on_update, on_delete, match)
    cur.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
    fk_info = cur.fetchall()

    # Indexes: (seq, name, unique, origin, partial)
    cur.execute(f"PRAGMA index_list(`{table_name}`)")
    index_list = cur.fetchall()

    unique_indexes = []
    seen_unique_cols = set()
    for idx in index_list:
        idx_name = idx[1]
        is_unique = (idx[2] == 1)
        is_pk = (idx[3] == 'pk')
        if is_unique and not is_pk:
            cur.execute(f"PRAGMA index_info(`{idx_name}`)")
            idx_cols = tuple(c[2] for c in cur.fetchall())
            if idx_cols and idx_cols not in seen_unique_cols:
                seen_unique_cols.add(idx_cols)
                if idx_name.startswith('sqlite_autoindex'):
                    clean_name = f"uq_{table_name}_" + "_".join(idx_cols)
                else:
                    clean_name = idx_name
                unique_indexes.append((clean_name, list(idx_cols)))

    is_auto = 'AUTOINCREMENT' in original_sql.upper()

    return {
        'original_sql': original_sql,
        'columns': columns_info,
        'foreign_keys': fk_info,
        'unique_indexes': unique_indexes,
        'is_auto': is_auto
    }


def format_sql_value(val):
    """Formatea un valor de Python para una sentencia INSERT en SQL."""
    if val is None:
        return 'NULL'
    if isinstance(val, bool):
        return '1' if val else '0'
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (bytes, bytearray)):
        return f"X'{val.hex()}'"
    # String / Datetime / etc.
    escaped = str(val).replace('\\', '\\\\').replace("'", "''").replace('\r', '\\r').replace('\n', '\\n')
    return f"'{escaped}'"


def convert_sqlite_to_mysql(
    db_path: str,
    output_path: str,
    schema_name: str = 'monagua_db',
    mode: str = 'domain',
    include_data: bool = False
):
    """Lee SQLite y genera el archivo SQL compatible con MySQL Workbench."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"No se encontró el archivo de base de datos: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    all_table_names = [r[0] for r in cur.fetchall()]

    if mode == 'all':
        selected_tables = [t for t in all_table_names if t != 'sqlite_sequence']
    elif mode == 'business':
        selected_tables = [
            t for t in all_table_names
            if any(t.startswith(prefix) for prefix in BUSINESS_TABLE_PREFIXES)
            and not t.startswith('usuarios_usuario_groups')
            and not t.startswith('usuarios_usuario_user_permissions')
        ]
    else:  # domain (default)
        selected_tables = [
            t for t in all_table_names
            if any(t.startswith(prefix) for prefix in DOMAIN_TABLE_PREFIXES)
        ]

    # Reordenar o asegurar que tablas dependientes funcionen (FOREIGN_KEY_CHECKS=0 lo protege de todos modos)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql_lines = []
    sql_lines.append("-- =============================================================================")
    sql_lines.append(f"-- Script de Base de Datos generado para MySQL Workbench")
    sql_lines.append(f"-- Proyecto: Monagua (MNG_WEB)")
    sql_lines.append(f"-- Modo: {mode.upper()} ({len(selected_tables)} tablas)")
    sql_lines.append(f"-- Fecha de generación: {now_str}")
    sql_lines.append("-- =============================================================================")
    sql_lines.append("")
    sql_lines.append("SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;")
    sql_lines.append("SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;")
    sql_lines.append("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';")
    sql_lines.append("")
    sql_lines.append(f"-- -----------------------------------------------------")
    sql_lines.append(f"-- Schema `{schema_name}`")
    sql_lines.append(f"-- -----------------------------------------------------")
    sql_lines.append(f"CREATE SCHEMA IF NOT EXISTS `{schema_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    sql_lines.append(f"USE `{schema_name}`;")
    sql_lines.append("")

    for table_name in selected_tables:
        meta = get_table_metadata(conn, table_name)
        cols_info = meta['columns']
        fks_info = meta['foreign_keys']
        unique_idxs = meta['unique_indexes']
        is_auto = meta['is_auto']

        sql_lines.append(f"-- -----------------------------------------------------")
        sql_lines.append(f"-- Tabla `{schema_name}`.`{table_name}`")
        sql_lines.append(f"-- -----------------------------------------------------")
        sql_lines.append(f"DROP TABLE IF EXISTS `{table_name}`;")
        sql_lines.append(f"CREATE TABLE IF NOT EXISTS `{table_name}` (")

        pk_cols = [c[1] for c in cols_info if c[5] > 0]
        col_definitions = []

        for c in cols_info:
            cid, name, col_type, notnull, dflt_value, pk_pos = c
            is_pk = (pk_pos > 0)
            is_autoincrement = is_pk and (is_auto or len(pk_cols) == 1 and ('int' in col_type.lower() or name == 'id'))

            mysql_type = map_sqlite_type_to_mysql(name, col_type, is_pk, is_autoincrement)

            null_clause = " NOT NULL" if notnull and not is_autoincrement else ("" if is_autoincrement else " NULL")

            dflt_clause = ""
            if dflt_value is not None:
                # Normalizar valor por defecto
                dflt_clean = dflt_value.strip()
                if dflt_clean.upper() not in ('NULL', "''", ""):
                    dflt_clause = f" DEFAULT {dflt_clean}"

            col_def = f"  `{name}` {mysql_type}{null_clause}{dflt_clause}"
            col_definitions.append(col_def)

        # Restricción PRIMARY KEY
        if pk_cols:
            pk_list = ", ".join([f"`{c}`" for c in pk_cols])
            col_definitions.append(f"  PRIMARY KEY ({pk_list})")

        # Restricciones UNIQUE adicionales del DDL original o índices
        unique_matches = re.findall(r'CONSTRAINT\s+["`]?(\w+)["`]?\s+UNIQUE\s*\(([^)]+)\)', meta['original_sql'], re.IGNORECASE)
        added_unique_tuples = set()
        for u_name, u_cols in unique_matches:
            cols_tuple = tuple(col.strip(' "\'`') for col in u_cols.split(','))
            added_unique_tuples.add(cols_tuple)
            cleaned_cols = ", ".join([f"`{col}`" for col in cols_tuple])
            col_definitions.append(f"  UNIQUE INDEX `{u_name}_UNIQUE` ({cleaned_cols} ASC)")

        # Unique indexes de sqlite
        for u_name, u_cols in unique_idxs:
            cols_tuple = tuple(u_cols)
            if cols_tuple not in added_unique_tuples:
                added_unique_tuples.add(cols_tuple)
                cols_str = ", ".join([f"`{c}`" for c in u_cols])
                col_definitions.append(f"  UNIQUE INDEX `{u_name}` ({cols_str} ASC)")

        # Restricciones FOREIGN KEY explícitas para MySQL Workbench
        for fk in fks_info:
            _, _, ref_table, from_col, to_col, on_update, on_delete, _ = fk
            # Solo agregar la relación si la tabla referenciada está seleccionada
            if ref_table not in selected_tables:
                continue

            fk_name = f"fk_{table_name}_{from_col}"[:64]
            on_del_clause = f" ON DELETE {on_delete}" if on_delete and on_delete.upper() not in ('NONE', 'NO ACTION') else " ON DELETE NO ACTION"
            on_upd_clause = f" ON UPDATE {on_update}" if on_update and on_update.upper() not in ('NONE', 'NO ACTION') else " ON UPDATE NO ACTION"

            fk_def = (
                f"  CONSTRAINT `{fk_name}`\n"
                f"    FOREIGN KEY (`{from_col}`)\n"
                f"    REFERENCES `{ref_table}` (`{to_col}`)"
                f"{on_del_clause}{on_upd_clause}"
            )
            col_definitions.append(fk_def)

        # Unir todas las definiciones
        sql_lines.append(",\n".join(col_definitions))
        sql_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
        sql_lines.append("")

        # Exportar datos si se solicitó
        if include_data:
            cur.execute(f"SELECT * FROM `{table_name}`")
            rows = cur.fetchall()
            if rows:
                col_names = [f"`{c[1]}`" for c in cols_info]
                cols_header = ", ".join(col_names)
                sql_lines.append(f"-- Datos para `{table_name}` ({len(rows)} registros)")
                for row in rows:
                    vals = [format_sql_value(v) for v in row]
                    vals_str = ", ".join(vals)
                    sql_lines.append(f"INSERT INTO `{table_name}` ({cols_header}) VALUES ({vals_str});")
                sql_lines.append("")

    sql_lines.append("SET SQL_MODE=@OLD_SQL_MODE;")
    sql_lines.append("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
    sql_lines.append("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")
    sql_lines.append("")
    sql_lines.append("-- =============================================================================")
    sql_lines.append("-- Fin del Script")
    sql_lines.append("-- =============================================================================")

    output_content = "\n".join(sql_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

    conn.close()
    return len(selected_tables)


def main():
    parser = argparse.ArgumentParser(
        description="Convierte base de datos SQLite (Monagua) a script SQL compatible con MySQL Workbench para diagramas EER."
    )
    parser.add_argument(
        '--db',
        default='db.sqlite3',
        help="Ruta al archivo SQLite (por defecto: db.sqlite3)"
    )
    parser.add_argument(
        '--output', '-o',
        default='monagua_mysql.sql',
        help="Ruta del archivo SQL de salida (por defecto: monagua_mysql.sql)"
    )
    parser.add_argument(
        '--schema',
        default='monagua_db',
        help="Nombre del esquema/base de datos MySQL (por defecto: monagua_db)"
    )
    parser.add_argument(
        '--mode',
        choices=['business', 'domain', 'all'],
        default='business',
        help="Modo de exportación: 'business' (20 tablas del modelo Monagua - recomendado para diagrama limpio), 'domain' (25 tablas con auth), 'all' (todas las tablas)"
    )
    parser.add_argument(
        '--all-tables',
        action='store_true',
        help="Alias para --mode all (exportar todas las tablas incluyendo django_migrations, etc.)"
    )
    parser.add_argument(
        '--with-data',
        action='store_true',
        help="Incluir los registros (INSERT INTO) además de las definiciones de tablas"
    )

    args = parser.parse_args()

    mode = 'all' if args.all_tables else args.mode

    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    mode_labels = {
        'business': 'Tablas del Negocio Monagua (Recomendado para Diagrama EER limpio)',
        'domain': 'Tablas de Dominio + Autenticacion Django',
        'all': 'Todas las tablas (Estructura completa de Django)'
    }

    print("==================================================================")
    print("  CONVERSOR MONAGUA: SQLite -> MySQL Workbench ")
    print("==================================================================")
    print(f"[*] Base de datos origen : {args.db}")
    print(f"[*] Archivo destino      : {args.output}")
    print(f"[*] Esquema MySQL        : {args.schema}")
    print(f"[*] Modo de tablas       : {mode_labels.get(mode, mode)}")
    print(f"[*] Incluir datos        : {'Si' if args.with_data else 'Solo estructura/esquema (DDL)'}")
    print("------------------------------------------------------------------")

    try:
        count = convert_sqlite_to_mysql(
            db_path=args.db,
            output_path=args.output,
            schema_name=args.schema,
            mode=mode,
            include_data=args.with_data
        )
        print(f"[+] Conversion exitosa! Se exportaron {count} tablas.")
        print(f"[+] Archivo generado: {os.path.abspath(args.output)}")
        print("\n" + "="*66)
        print("  INSTRUCCIONES PARA VER EL DIAGRAMA EN MYSQL WORKBENCH:")
        print("="*66)
        print("1. Abre MySQL Workbench.")
        print("2. En el menu superior, selecciona:")
        print("   -> File  >  Create EER Model from SQL Script...")
        print("   (o presiona el atajo Ctrl + Shift + R)")
        print(f"3. Selecciona el archivo generado:")
        print(f"   '{os.path.abspath(args.output)}'")
        print("4. Deja marcada la casilla 'Place imported objects on a new diagram'.")
        print("5. Haz clic en 'Execute' y luego en 'Next' -> 'Finish'.")
        print("6. Listo! Veras el diagrama EER con todas las tablas y sus relaciones conectadas.")
        print("="*66 + "\n")
    except Exception as e:
        print(f"[X] Error durante la conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

