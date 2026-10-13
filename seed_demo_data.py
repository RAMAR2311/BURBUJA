import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
from app import create_app
from models import (
    db, User, Product, ProductVariant, Sale, SaleDetail, SalePayment,
    Expense, Provider, ProviderInvoice, ProviderPayment, ArqueoCaja, PriceApproval
)

def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Iniciando población de datos de ejemplo para My Case...")

        # 1. Obtener o crear usuarios
        admin = User.query.filter_by(rol='admin').first()
        if not admin:
            admin = User(
                nombre="Administrador Principal",
                email="admin@mycase.com",
                telefono="3001234567",
                password_hash=generate_password_hash("admin123"),
                rol="admin"
            )
            db.session.add(admin)
            db.session.flush()

        vendedor = User.query.filter_by(email="valentina@mycase.com").first()
        if not vendedor:
            vendedor = User(
                nombre="Valentina Gómez",
                email="valentina@mycase.com",
                telefono="3125550192",
                password_hash=generate_password_hash("123"),
                rol="vendedor"
            )
            db.session.add(vendedor)
            db.session.flush()

        print(f"👤 Usuarios listos: {admin.nombre} (Admin) y {vendedor.nombre} (Vendedora)")

        # 2. Crear Productos y Variantes si no existen
        productos_def = [
            {
                "nombre": "Case Silicona Matte Shockproof iPhone 15 Pro",
                "sku": "CASE-IP15P-SIL",
                "precio_costo": 22000,
                "precio_minimo": 38000,
                "precio_sugerido": 45000,
                "observacion": "Silicona suave con forro de microfibra interno y protección antigolpe.",
                "variantes": [
                    {"nombre": "Rosa Neón", "stock": 14, "costo": 22000, "minimo": 38000, "sugerido": 45000},
                    {"nombre": "Negro Mate", "stock": 12, "costo": 22000, "minimo": 38000, "sugerido": 45000},
                    {"nombre": "Lavanda Soft", "stock": 9, "costo": 22000, "minimo": 38000, "sugerido": 45000},
                ]
            },
            {
                "nombre": "Case Magnético MagSafe Clear iPhone 14/15",
                "sku": "CASE-MAGSAFE-CLR",
                "precio_costo": 26000,
                "precio_minimo": 45000,
                "precio_sugerido": 55000,
                "observacion": "Policarbonato anti-amarilleo con anillo magnético de alta potencia.",
                "variantes": [
                    {"nombre": "Transparente Silver", "stock": 16, "costo": 26000, "minimo": 45000, "sugerido": 55000},
                    {"nombre": "Pink Glow Ring", "stock": 15, "costo": 26000, "minimo": 45000, "sugerido": 55000},
                ]
            },
            {
                "nombre": "Funda Armor Shockproof Samsung S24 Ultra",
                "sku": "CASE-S24U-ARM",
                "precio_costo": 25000,
                "precio_minimo": 42000,
                "precio_sugerido": 50000,
                "observacion": "Doble capa reforzada con soporte de anillo 360 integrado.",
                "variantes": [
                    {"nombre": "Titanio Grafito", "stock": 11, "costo": 25000, "minimo": 42000, "sugerido": 50000},
                    {"nombre": "Azul Metálico", "stock": 8, "costo": 25000, "minimo": 42000, "sugerido": 50000},
                ]
            },
            {
                "nombre": "Protector Lente Cámara Diamond Crystal Glam",
                "sku": "PROT-CAM-DIAM",
                "precio_costo": 10000,
                "precio_minimo": 18000,
                "precio_sugerido": 25000,
                "observacion": "Cristal templado 9H con marco brillante diamantado glam.",
                "variantes": [
                    {"nombre": "Diamond Pink", "stock": 18, "costo": 10000, "minimo": 18000, "sugerido": 25000},
                    {"nombre": "Diamond Silver", "stock": 20, "costo": 10000, "minimo": 18000, "sugerido": 25000},
                ]
            },
            {
                "nombre": "Vidrio Cerámico 9D Mate Anti-Huella",
                "sku": "VID-CER-9D-MAT",
                "precio_costo": 6000,
                "precio_minimo": 12000,
                "precio_sugerido": 18000,
                "cantidad_stock": 35,
                "observacion": "Acabado mate especial para gaming y evitar manchas de dedos.",
                "variantes": []
            },
            {
                "nombre": "Vidrio Privacidad Anti-Espía Premium",
                "sku": "VID-PRIV-ESP",
                "precio_costo": 8000,
                "precio_minimo": 16000,
                "precio_sugerido": 22000,
                "cantidad_stock": 28,
                "observacion": "Filtro polarizado que bloquea la visión lateral a 28 grados.",
                "variantes": []
            },
            {
                "nombre": "Cargador Rápido 25W Type-C Power Delivery",
                "sku": "CARG-25W-PD",
                "precio_costo": 30000,
                "precio_minimo": 50000,
                "precio_sugerido": 65000,
                "cantidad_stock": 18,
                "observacion": "Carga ultra rápida certificada con protección térmica.",
                "variantes": []
            },
            {
                "nombre": "Cable Carga Rápida Trenzado 1.5m Reforzado",
                "sku": "CAB-TREN-15M",
                "precio_costo": 12000,
                "precio_minimo": 20000,
                "precio_sugerido": 28000,
                "observacion": "Nylon balístico indestructible de alta resistencia a tirones.",
                "variantes": [
                    {"nombre": "Rosa Glam", "stock": 15, "costo": 12000, "minimo": 20000, "sugerido": 28000},
                    {"nombre": "Blanco Polar", "stock": 14, "costo": 12000, "minimo": 20000, "sugerido": 28000},
                ]
            },
            {
                "nombre": "Soporte Magnético PopSocket Glitter",
                "sku": "POP-MAG-GLIT",
                "precio_costo": 5000,
                "precio_minimo": 10000,
                "precio_sugerido": 15000,
                "observacion": "Agarre ergonómico con destellos brillantes holográficos.",
                "variantes": [
                    {"nombre": "Rosa Neón", "stock": 22, "costo": 5000, "minimo": 10000, "sugerido": 15000},
                    {"nombre": "Oro Rosa", "stock": 16, "costo": 5000, "minimo": 10000, "sugerido": 15000},
                ]
            },
            {
                "nombre": "Correa Lanyard Luxury de Cuello para Celular",
                "sku": "LANYARD-LUX",
                "precio_costo": 7000,
                "precio_minimo": 14000,
                "precio_sugerido": 20000,
                "cantidad_stock": 19,
                "observacion": "Cordón premium trenzado con mosquetón metálico dorado/rosado.",
                "variantes": []
            },
            {
                "nombre": "Audífonos Bluetooth In-Ear TWS Pro Sound",
                "sku": "AUD-TWS-PRO",
                "precio_costo": 38000,
                "precio_minimo": 60000,
                "precio_sugerido": 75000,
                "cantidad_stock": 3, # Stock Crítico para Alerta de Dashboard
                "observacion": "Cancelación de ruido pasiva y estuche con carga inalámbrica. (Stock Crítico)",
                "variantes": []
            }
        ]

        prods_creados = {}
        vars_creadas = {}
        for pdata in productos_def:
            p = Product.query.filter_by(sku=pdata["sku"]).first()
            if not p:
                p = Product(
                    nombre=pdata["nombre"],
                    sku=pdata["sku"],
                    precio_costo=pdata["precio_costo"],
                    precio_minimo=pdata["precio_minimo"],
                    precio_sugerido=pdata["precio_sugerido"],
                    cantidad_stock=pdata.get("cantidad_stock", 0),
                    observacion=pdata.get("observacion", ""),
                    tipo_inventario='tienda',
                    activo=True,
                    fecha_creacion=datetime(2026, 10, 1, 9, 0, 0)
                )
                db.session.add(p)
                db.session.flush()

                for vdata in pdata.get("variantes", []):
                    var = ProductVariant(
                        product_id=p.id,
                        nombre_variante=vdata["nombre"],
                        cantidad_stock=vdata["stock"],
                        precio_costo=vdata["costo"],
                        precio_minimo=vdata["minimo"],
                        precio_sugerido=vdata["sugerido"]
                    )
                    db.session.add(var)
                    db.session.flush()
                    vars_creadas[f"{p.sku}_{vdata['nombre']}"] = var
            prods_creados[p.sku] = p

        db.session.commit()
        print(f"📦 Inventario poblado con {len(prods_creados)} productos de telefonía móvil.")

        # 3. Ventas de Demostración en Octubre 2026
        ventas_existentes = Sale.query.filter(Sale.fecha_venta >= datetime(2026, 10, 1)).count()
        if ventas_existentes == 0:
            print("🛍️ Generando ventas de ejemplo para Octubre 2026...")

            def crear_venta(vendedor_obj, fecha_dt, monto_tot, metodo_prin, detalles_list, pagos_list=None):
                v = Sale(
                    vendedor_id=vendedor_obj.id,
                    fecha_venta=fecha_dt,
                    monto_total=monto_tot,
                    metodo_pago=metodo_prin
                )
                db.session.add(v)
                db.session.flush()

                for det in detalles_list:
                    sd = SaleDetail(
                        sale_id=v.id,
                        product_id=det.get("product_id"),
                        variant_id=det.get("variant_id"),
                        cantidad_vendida=det.get("cantidad", 1),
                        precio_venta_final=det.get("precio")
                    )
                    db.session.add(sd)

                if pagos_list:
                    for pag in pagos_list:
                        sp = SalePayment(
                            sale_id=v.id,
                            metodo_pago=pag["metodo"],
                            monto=pag["monto"]
                        )
                        db.session.add(sp)
                else:
                    sp = SalePayment(
                        sale_id=v.id,
                        metodo_pago=metodo_prin,
                        monto=monto_tot
                    )
                    db.session.add(sp)
                return v

            p_case_sil = prods_creados["CASE-IP15P-SIL"]
            p_case_mag = prods_creados["CASE-MAGSAFE-CLR"]
            p_case_arm = prods_creados["CASE-S24U-ARM"]
            p_prot_diam = prods_creados["PROT-CAM-DIAM"]
            p_vid_cer = prods_creados["VID-CER-9D-MAT"]
            p_vid_priv = prods_creados["VID-PRIV-ESP"]
            p_carg_25w = prods_creados["CARG-25W-PD"]
            p_cab_tren = prods_creados["CAB-TREN-15M"]
            p_pop_mag = prods_creados["POP-MAG-GLIT"]
            p_lanyard = prods_creados["LANYARD-LUX"]
            p_tws_pro = prods_creados["AUD-TWS-PRO"]

            # Venta 1 (Efectivo): 2x Case Silicona
            crear_venta(
                vendedor,
                datetime(2026, 10, 2, 10, 30),
                90000,
                "efectivo",
                [{"product_id": p_case_sil.id, "cantidad": 2, "precio": 45000}]
            )

            # Venta 2 (Nequi): 1x Case MagSafe + 1x Protector Diamante
            crear_venta(
                vendedor,
                datetime(2026, 10, 3, 14, 15),
                80000,
                "nequi",
                [
                    {"product_id": p_case_mag.id, "cantidad": 1, "precio": 55000},
                    {"product_id": p_prot_diam.id, "cantidad": 1, "precio": 25000}
                ]
            )

            # Venta 3 (Bold): 1x Cargador 25W + 1x Cable Trenzado
            crear_venta(
                admin,
                datetime(2026, 10, 4, 16, 45),
                93000,
                "bolt",
                [
                    {"product_id": p_carg_25w.id, "cantidad": 1, "precio": 65000},
                    {"product_id": p_cab_tren.id, "cantidad": 1, "precio": 28000}
                ]
            )

            # Venta 4 (Efectivo): 1x Armor S24U + 1x Vidrio Cerámico
            crear_venta(
                vendedor,
                datetime(2026, 10, 6, 11, 20),
                68000,
                "efectivo",
                [
                    {"product_id": p_case_arm.id, "cantidad": 1, "precio": 50000},
                    {"product_id": p_vid_cer.id, "cantidad": 1, "precio": 18000}
                ]
            )

            # Venta 5 (Mixto: Efectivo $50k + Nequi $40k): Audífonos TWS + PopSocket
            crear_venta(
                vendedor,
                datetime(2026, 10, 8, 15, 10),
                90000,
                "mixto",
                [
                    {"product_id": p_tws_pro.id, "cantidad": 1, "precio": 75000},
                    {"product_id": p_pop_mag.id, "cantidad": 1, "precio": 15000}
                ],
                [
                    {"metodo": "efectivo", "monto": 50000},
                    {"metodo": "nequi", "monto": 40000}
                ]
            )

            # Venta 6 (Bold): 2x Vidrio Privacidad + 1x PopSocket
            crear_venta(
                admin,
                datetime(2026, 10, 9, 17, 30),
                59000,
                "bolt",
                [
                    {"product_id": p_vid_priv.id, "cantidad": 2, "precio": 22000},
                    {"product_id": p_pop_mag.id, "cantidad": 1, "precio": 15000}
                ]
            )

            # Venta 7 (Nequi): 1x Case Clear MagSafe
            crear_venta(
                vendedor,
                datetime(2026, 10, 10, 12, 0),
                55000,
                "nequi",
                [{"product_id": p_case_mag.id, "cantidad": 1, "precio": 55000}]
            )

            # Venta 8 (Mixto: Efectivo $40k + Bold $33k): Case Silicona + Cable
            crear_venta(
                vendedor,
                datetime(2026, 10, 11, 16, 20),
                73000,
                "mixto",
                [
                    {"product_id": p_case_sil.id, "cantidad": 1, "precio": 45000},
                    {"product_id": p_cab_tren.id, "cantidad": 1, "precio": 28000}
                ],
                [
                    {"metodo": "efectivo", "monto": 40000},
                    {"metodo": "bolt", "monto": 33000}
                ]
            )

            # Venta 9 (Efectivo): 1x Cargador 25W
            crear_venta(
                vendedor,
                datetime(2026, 10, 12, 13, 40),
                65000,
                "efectivo",
                [{"product_id": p_carg_25w.id, "cantidad": 1, "precio": 65000}]
            )

            # Venta 10 (Nequi): 2x Lanyard Luxury + 1x Protector Diamante
            crear_venta(
                admin,
                datetime(2026, 10, 13, 11, 15),
                65000,
                "nequi",
                [
                    {"product_id": p_lanyard.id, "cantidad": 2, "precio": 20000},
                    {"product_id": p_prot_diam.id, "cantidad": 1, "precio": 25000}
                ]
            )

            db.session.commit()
            print("✅ 10 Ventas de ejemplo creadas con éxito.")

        # 4. Gastos Operativos de Demostración en Octubre 2026
        gastos_existentes = Expense.query.filter(Expense.fecha_gasto >= datetime(2026, 10, 1)).count()
        if gastos_existentes == 0:
            print("💸 Registrando gastos operativos de demostración...")
            gastos_def = [
                {
                    "tipo": "Gasto Diario",
                    "categoria": "Alimentación / Refrigerios",
                    "descripcion": "Refrigerios y café equipo de apertura",
                    "monto": 35000,
                    "metodo": "efectivo",
                    "fecha": datetime(2026, 10, 2, 11, 0)
                },
                {
                    "tipo": "Gasto Diario",
                    "categoria": "Empaques y Bolsas",
                    "descripcion": "Lote x100 bolsas boutique My Case rosa neón",
                    "monto": 120000,
                    "metodo": "nequi",
                    "fecha": datetime(2026, 10, 5, 14, 30)
                },
                {
                    "tipo": "Costo Indirecto",
                    "categoria": "Servicios Públicos",
                    "descripcion": "Plan comercial internet fibra óptica y telefonía",
                    "monto": 115000,
                    "metodo": "bolt",
                    "fecha": datetime(2026, 10, 7, 10, 0)
                },
                {
                    "tipo": "Gasto Diario",
                    "categoria": "Aseo y Mantenimiento",
                    "descripcion": "Insumos de limpieza y ambientador floral tienda",
                    "monto": 45000,
                    "metodo": "efectivo",
                    "fecha": datetime(2026, 10, 9, 16, 0)
                },
                {
                    "tipo": "Costo Indirecto",
                    "categoria": "Publicidad y Marketing",
                    "descripcion": "Campaña publicitaria Instagram Reels y TikTok",
                    "monto": 80000,
                    "metodo": "bolt",
                    "fecha": datetime(2026, 10, 11, 15, 0)
                }
            ]

            for gdata in gastos_def:
                g = Expense(
                    usuario_id=admin.id,
                    tipo_gasto=gdata["tipo"],
                    categoria=gdata["categoria"],
                    descripcion=gdata["descripcion"],
                    monto=gdata["monto"],
                    metodo_pago=gdata["metodo"],
                    fecha_gasto=gdata["fecha"]
                )
                db.session.add(g)

            db.session.commit()
            print("✅ 5 Gastos operativos creados con métodos Efectivo, Nequi y Bold.")

        # 5. Proveedores, Facturas y Abonos
        provs_existentes = Provider.query.count()
        if provs_existentes == 0:
            print("🚚 Creando proveedores con facturas y abonos...")

            # Proveedor 1
            p1 = Provider(
                nombre="Distribuidora Tech & Cases S.A.S.",
                empresa="Tech & Cases Mayoristas",
                telefono="3108889900",
                fecha_creacion=datetime(2026, 10, 1, 9, 0)
            )
            db.session.add(p1)
            db.session.flush()

            inv1 = ProviderInvoice(
                provider_id=p1.id,
                monto_total=1200000,
                numero_factura="FAC-10294",
                descripcion="Lote de Cases Silicona y MagSafe iPhone 15",
                fecha_factura=datetime(2026, 10, 2, 10, 0)
            )
            db.session.add(inv1)
            db.session.flush()

            # Abono en Bold y en Nequi
            pay1 = ProviderPayment(
                provider_id=p1.id,
                monto_abonado=400000,
                metodo_pago="bolt",
                observacion="Abono inicial contraentrega vía Datáfono Bold",
                fecha_pago=datetime(2026, 10, 5, 15, 0)
            )
            pay2 = ProviderPayment(
                provider_id=p1.id,
                monto_abonado=300000,
                metodo_pago="nequi",
                observacion="Segundo abono transferencia Nequi",
                fecha_pago=datetime(2026, 10, 10, 11, 30)
            )
            db.session.add_all([pay1, pay2])

            # Proveedor 2
            p2 = Provider(
                nombre="Importaciones Glam Cell Bogotá",
                empresa="Glam Cell Mayorista",
                telefono="3204445566",
                fecha_creacion=datetime(2026, 10, 1, 9, 0)
            )
            db.session.add(p2)
            db.session.flush()

            inv2 = ProviderInvoice(
                provider_id=p2.id,
                monto_total=850000,
                numero_factura="GC-8832",
                descripcion="Protectores de cámara y cargadores rápidos 25W",
                fecha_factura=datetime(2026, 10, 3, 11, 0)
            )
            db.session.add(inv2)
            db.session.flush()

            pay3 = ProviderPayment(
                provider_id=p2.id,
                monto_abonado=500000,
                metodo_pago="efectivo",
                observacion="Pago en efectivo retirado de caja menor",
                fecha_pago=datetime(2026, 10, 7, 16, 0)
            )
            db.session.add(pay3)

            # Proveedor 3
            p3 = Provider(
                nombre="Vidrios Templados El Diamante",
                empresa="El Diamante Accesorios",
                telefono="3152223344",
                fecha_creacion=datetime(2026, 10, 1, 9, 0)
            )
            db.session.add(p3)
            db.session.flush()

            inv3 = ProviderInvoice(
                provider_id=p3.id,
                monto_total=620000,
                numero_factura="DIA-5401",
                descripcion="Vidrios Cerámicos 9D y Vidrios Privacidad",
                fecha_factura=datetime(2026, 10, 6, 12, 0)
            )
            db.session.add(inv3)
            db.session.flush()

            pay4 = ProviderPayment(
                provider_id=p3.id,
                monto_abonado=200000,
                metodo_pago="bolt",
                observacion="Abono datáfono Bold comprobante #94821",
                fecha_pago=datetime(2026, 10, 11, 14, 0)
            )
            db.session.add(pay4)

            db.session.commit()
            print("✅ 3 Proveedores creados con facturas y abonos en Efectivo, Nequi y Bold.")

        # 6. Aprobaciones de Precios de Demostración
        aprob_existentes = PriceApproval.query.count()
        if aprob_existentes == 0:
            print("🏷️ Creando solicitudes de aprobación de precios de demostración...")
            p_case_sil = prods_creados["CASE-IP15P-SIL"]
            p_tws_pro = prods_creados["AUD-TWS-PRO"]

            aprob1 = PriceApproval(
                vendedor_id=vendedor.id,
                product_id=p_case_sil.id,
                nombre_producto=p_case_sil.nombre,
                precio_original=45000,
                precio_solicitado=38000,
                precio_aprobado=38000,
                estado="aprobado",
                admin_id=admin.id,
                motivo="Cliente frecuente compra combo de 3 unidades",
                fecha_solicitud=datetime(2026, 10, 10, 15, 30),
                fecha_resolucion=datetime(2026, 10, 10, 15, 32)
            )
            aprob2 = PriceApproval(
                vendedor_id=vendedor.id,
                product_id=p_tws_pro.id,
                nombre_producto=p_tws_pro.nombre,
                precio_original=75000,
                precio_solicitado=65000,
                estado="pendiente",
                motivo="Promoción especial solicitada en mostrador",
                fecha_solicitud=datetime(2026, 10, 13, 16, 0)
            )
            db.session.add_all([aprob1, aprob2])
            db.session.commit()
            print("✅ 2 Aprobaciones de precio creadas (1 aprobada, 1 pendiente).")

        # 7. Arqueo de Caja de Demostración
        arqueo_fecha = date(2026, 10, 12)
        arq = ArqueoCaja.query.filter_by(fecha_arqueo=arqueo_fecha).first()
        if not arq:
            print("📊 Registrando arqueo de caja cuadrado para demostración...")
            arq = ArqueoCaja(
                vendedor_id=vendedor.id,
                fecha_arqueo=arqueo_fecha,
                base_inicial=150000,
                total_efectivo_sistema=240000,
                total_transferencia_sistema=310000,
                gastos_del_dia=35000,
                efectivo_fisico_contado=355000,
                diferencia=0,
                observaciones="Cuadre perfecto de caja en turno tarde. Sin novedades en efectivo ni transferencias.",
                fecha_cierre=datetime(2026, 10, 12, 20, 0)
            )
            db.session.add(arq)
            db.session.commit()
            print("✅ Arqueo de caja registrado exitosamente.")

        print("🎉 ¡Población de datos completada con éxito!")

if __name__ == '__main__':
    seed()
