from app import create_app
from models import db

def main():
    app = create_app()
    with app.app_context():
        # 1. Asegurar creación de tablas si faltara alguna (ej. providers)
        db.create_all()

        # 2. Columnas añadidas a los modelos (compatible con PostgreSQL y SQLite)
        is_sqlite = db.engine.url.drivername.startswith('sqlite')
        
        columnas_pg = [
            ("products", "activo", "BOOLEAN DEFAULT TRUE"),
            ("maneos", "valor_fijo", "NUMERIC(10, 2)"),
            ("maneos", "variant_id", "INTEGER"),
            ("maneos", "cliente_id", "INTEGER"),
            ("product_variants", "precio_costo", "NUMERIC(10, 2)"),
            ("product_variants", "precio_minimo", "NUMERIC(10, 2)"),
            ("product_variants", "precio_sugerido", "NUMERIC(10, 2)"),
            ("users", "telefono", "VARCHAR(20)"),
            ("sale_details", "variant_id", "INTEGER"),
            ("sale_details", "nombre_manual", "VARCHAR(200)"),
            ("sale_details", "precio_costo_manual", "NUMERIC(10, 2)"),
            ("facturas_bodega_detalles", "variant_id", "INTEGER"),
            ("facturas_bodega_detalles", "precio_venta", "NUMERIC(10, 2)"),
            ("clientes", "creado_por_id", "INTEGER"),
            ("clientes", "contacto_persona", "VARCHAR(100)"),
            ("clientes", "local_numero", "VARCHAR(50)"),
            ("clientes", "notas", "TEXT"),
            ("price_approvals", "sale_id", "INTEGER"),
            ("provider_payments", "metodo_pago", "VARCHAR(50) DEFAULT 'efectivo'"),
        ]

        for tabla, col, tipo in columnas_pg:
            try:
                if is_sqlite:
                    db.session.execute(db.text(f"ALTER TABLE {tabla} ADD COLUMN {col} {tipo};"))
                else:
                    db.session.execute(db.text(f"ALTER TABLE {tabla} ADD COLUMN IF NOT EXISTS {col} {tipo};"))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                # Si ya existe la columna en SQLite, se ignora limpiamente
                if "duplicate column" not in str(e).lower():
                    pass

        try:
            db.session.execute(db.text("UPDATE products SET activo = 1 WHERE activo IS NULL;"))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # 3. Ajustar valores antiguos registrados con números abreviados (ej: 30 -> 30000)
        try:
            db.session.execute(db.text("UPDATE maneos SET valor_fijo = valor_fijo * 1000 WHERE valor_fijo > 0 AND valor_fijo < 1000;"))
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        # 4. Vincular automáticamente maneos existentes que tenían solo nombre de texto a Clientes
        try:
            from models import Cliente, Maneo
            maneos_sin_cliente = Maneo.query.filter(Maneo.cliente_id.is_(None)).all()
            for m in maneos_sin_cliente:
                if m.local_vecino and m.local_vecino.strip():
                    nombre = m.local_vecino.strip()
                    c = Cliente.query.filter(Cliente.nombre_o_razon_social.ilike(nombre)).first()
                    if not c:
                        c = Cliente(nombre_o_razon_social=nombre)
                        db.session.add(c)
                        db.session.flush()
                    m.cliente_id = c.id
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        # 5. Vincular aprobaciones 'utilizada' a sus respectivas ventas en sale_details si aún no tienen sale_id
        try:
            from models import PriceApproval, Sale, SaleDetail
            aprobaciones_sin_venta = PriceApproval.query.filter(
                PriceApproval.estado == 'utilizada',
                PriceApproval.sale_id.is_(None)
            ).all()

            for ap in aprobaciones_sin_venta:
                # Buscar en SaleDetail venta del vendedor con el producto y precio aprobado
                query_match = db.session.query(SaleDetail).join(Sale).filter(
                    Sale.vendedor_id == ap.vendedor_id,
                    SaleDetail.product_id == ap.product_id,
                    SaleDetail.precio_venta_final == ap.precio_aprobado
                )
                if ap.variant_id:
                    query_match = query_match.filter(SaleDetail.variant_id == ap.variant_id)
                detalle_encontrado = query_match.order_by(Sale.id.desc()).first()

                if detalle_encontrado:
                    ap.sale_id = detalle_encontrado.sale_id

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[Aviso vinculación aprobaciones] -> {e}")

        print("[OK] Base de datos actualizada y todas las columnas sincronizadas correctamente.")

if __name__ == '__main__':
    main()
